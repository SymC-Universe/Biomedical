args <- commandArgs(trailingOnly = TRUE)
if (length(args) < 2) {
  stop("usage: Rscript run_tool_feasibility_f3_divas.R <inputs_dir> <out_dir>")
}

inputs_dir <- normalizePath(args[[1]], mustWork = TRUE)
out_dir <- args[[2]]
dir.create(out_dir, recursive = TRUE, showWarnings = FALSE)

suppressPackageStartupMessages(library(DIVAS))
suppressPackageStartupMessages(library(jsonlite))

NSIM <- 50L
DIVAS_COMMIT <- "294986fac88bdeea1071902aa360b19e820c85de"
DIVAS_VERSION <- as.character(packageVersion("DIVAS"))
DIVAS_DIAGNOSTIC_REPAIR <- paste(
  "failure instrumentation only: captures condition call, active call stack, and input dimensions",
  "without changing DIVAS inputs, orientation, nsim, centering, seed, ReturnDetail, or mathematics"
)

stable_seed <- function(scenario, representation, replicate) {
  token <- paste("F3_DIVAS", scenario, representation, replicate, sep = "|")
  vals <- utf8ToInt(token)
  weights <- seq_along(vals)
  as.integer((sum((vals * weights) %% 2147483000) %% 2147483000) + 1)
}

load_matrix <- function(path) {
  as.matrix(read.csv(gzfile(path, open = "rt"), header = FALSE, check.names = FALSE))
}

rank_from_cols <- function(scores, pattern) {
  if (is.null(scores) || is.null(colnames(scores)) || ncol(scores) == 0) return(0L)
  as.integer(sum(grepl(pattern, colnames(scores), fixed = TRUE)))
}

collapse_call <- function(cl) {
  if (is.null(cl)) return("")
  paste(deparse(cl, width.cutoff = 500L), collapse = " ")
}

manifest <- fromJSON(file.path(inputs_dir, "manifest.json"), simplifyDataFrame = TRUE)
records <- manifest$records
rows <- vector("list", nrow(records))
failures <- list()

for (i in seq_len(nrow(records))) {
  scenario <- as.character(records$scenario[[i]])
  representation <- as.character(records$representation[[i]])
  replicate <- as.integer(records$replicate[[i]])
  source <- load_matrix(file.path(inputs_dir, as.character(records$source_file[[i]])))
  target <- load_matrix(file.path(inputs_dir, as.character(records$target_file[[i]])))

  row <- data.frame(
    scenario = scenario,
    representation = representation,
    replicate = replicate,
    divas_status = "OK",
    divas_joint_rank = NA_integer_,
    divas_source_indiv_rank = NA_integer_,
    divas_target_indiv_rank = NA_integer_,
    divas_source_signal_rank = NA_integer_,
    divas_target_signal_rank = NA_integer_,
    divas_error = "",
    divas_error_call = "",
    divas_error_trace = "",
    source_input_nrow = nrow(source),
    source_input_ncol = ncol(source),
    target_input_nrow = nrow(target),
    target_input_ncol = ncol(target),
    stringsAsFactors = FALSE
  )

  captured_call <- ""
  captured_calls <- character(0)
  result <- tryCatch(
    withCallingHandlers({
      datablock <- list(SOURCE = t(source), TARGET = t(target))
      if (ncol(datablock$SOURCE) != ncol(datablock$TARGET)) {
        stop(sprintf(
          "frozen-input sample mismatch before DIVAS: SOURCE ncol=%d TARGET ncol=%d",
          ncol(datablock$SOURCE), ncol(datablock$TARGET)
        ))
      }
      colnames(datablock$SOURCE) <- paste0("S", seq_len(ncol(datablock$SOURCE)))
      colnames(datablock$TARGET) <- colnames(datablock$SOURCE)
      DIVASmain(
        datablock = datablock,
        nsim = NSIM,
        iprint = FALSE,
        colCent = FALSE,
        rowCent = TRUE,
        seed = stable_seed(scenario, representation, replicate),
        ReturnDetail = TRUE
      )
    }, error = function(e) {
      captured_call <<- collapse_call(conditionCall(e))
      captured_calls <<- vapply(sys.calls(), collapse_call, character(1))
    }),
    error = function(e) e
  )

  if (inherits(result, "error")) {
    row$divas_status <- "ERROR"
    row$divas_error <- conditionMessage(result)
    row$divas_error_call <- captured_call
    row$divas_error_trace <- paste(captured_calls, collapse = " <- ")
    failures[[length(failures) + 1L]] <- list(
      method = "DIVAS",
      scenario = scenario,
      representation = representation,
      replicate = replicate,
      error = conditionMessage(result),
      error_call = captured_call,
      error_trace = captured_calls,
      input_dimensions = list(
        source = c(nrow(source), ncol(source)),
        target = c(nrow(target), ncol(target)),
        divas_source = c(ncol(source), nrow(source)),
        divas_target = c(ncol(target), nrow(target))
      )
    )
  } else {
    scores <- result$sampleScoreMatrix
    if (is.null(scores) && !is.null(result$Scores)) scores <- result$Scores
    row$divas_joint_rank <- rank_from_cols(scores, "SOURCE+TARGET-") + rank_from_cols(scores, "TARGET+SOURCE-")
    row$divas_source_indiv_rank <- rank_from_cols(scores, "SOURCE-Individual-")
    row$divas_target_indiv_rank <- rank_from_cols(scores, "TARGET-Individual-")
    if (!is.null(result$rBars) && length(result$rBars) >= 2) {
      row$divas_source_signal_rank <- as.integer(result$rBars[[1]])
      row$divas_target_signal_rank <- as.integer(result$rBars[[2]])
    }
  }

  rows[[i]] <- row
  cat(sprintf("%s %s rep=%d DIVAS=%s\n", scenario, representation, replicate, row$divas_status))
  if (row$divas_status == "ERROR") {
    cat(sprintf("DIVAS_ERROR_CALL %s\n", row$divas_error_call))
    cat(sprintf("DIVAS_ERROR_TRACE %s\n", row$divas_error_trace))
  }
  flush.console()
}

replicates <- do.call(rbind, rows)
write.csv(replicates, file.path(out_dir, "f3_divas_replicates.csv"), row.names = FALSE)

ok <- replicates[replicates$divas_status == "OK", , drop = FALSE]
metrics <- c(
  "divas_joint_rank",
  "divas_source_indiv_rank",
  "divas_target_indiv_rank",
  "divas_source_signal_rank",
  "divas_target_signal_rank"
)
summary_rows <- list()
if (nrow(ok) > 0) {
  groups <- unique(ok[, c("scenario", "representation")])
  for (g in seq_len(nrow(groups))) {
    subset_rows <- ok[ok$scenario == groups$scenario[[g]] & ok$representation == groups$representation[[g]], , drop = FALSE]
    rec <- list(scenario = groups$scenario[[g]], representation = groups$representation[[g]], n = nrow(subset_rows))
    for (metric in metrics) {
      vals <- subset_rows[[metric]]
      vals <- vals[is.finite(vals)]
      if (length(vals) > 0) {
        rec[[paste0("median_", metric)]] <- median(vals)
        rec[[paste0("q25_", metric)]] <- as.numeric(quantile(vals, 0.25, names = FALSE))
        rec[[paste0("q75_", metric)]] <- as.numeric(quantile(vals, 0.75, names = FALSE))
      }
    }
    summary_rows[[length(summary_rows) + 1L]] <- as.data.frame(rec, stringsAsFactors = FALSE)
  }
}
if (length(summary_rows) > 0) {
  all_names <- unique(unlist(lapply(summary_rows, names)))
  summary_rows <- lapply(summary_rows, function(df) {
    missing <- setdiff(all_names, names(df))
    for (nm in missing) df[[nm]] <- NA
    df[, all_names, drop = FALSE]
  })
  write.csv(do.call(rbind, summary_rows), file.path(out_dir, "f3_divas_summary.csv"), row.names = FALSE)
} else {
  write.csv(data.frame(), file.path(out_dir, "f3_divas_summary.csv"), row.names = FALSE)
}

payload <- list(
  status = if (length(failures) == 0) "F3_DIVAS_COMPLETE" else "F3_DIVAS_MECHANICAL_FAILURE",
  records = nrow(replicates),
  failures = failures,
  divas = list(
    version = DIVAS_VERSION,
    commit = DIVAS_COMMIT,
    nsim = NSIM,
    rowCent = TRUE,
    colCent = FALSE,
    ReturnDetail = TRUE,
    diagnostic_repair = DIVAS_DIAGNOSTIC_REPAIR
  ),
  claim_ceiling = "synthetic established-method comparison only",
  c1_beta_value_biology_read = FALSE,
  biological_chi_used = FALSE
)
write(toJSON(payload, auto_unbox = TRUE, pretty = TRUE, null = "null"), file.path(out_dir, "F3_DIVAS_SUMMARY.json"))
cat(toJSON(payload, auto_unbox = TRUE, pretty = TRUE, null = "null"), "\n")

if (length(failures) > 0) quit(status = 2)
