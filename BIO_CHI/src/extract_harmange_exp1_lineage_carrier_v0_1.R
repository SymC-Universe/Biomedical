args <- commandArgs(trailingOnly=TRUE)
if (length(args) != 3) stop("usage: extract_harmange_exp1_lineage_carrier_v0_1.R <rds> <json> <csv>")
rds_path <- args[[1]]
json_path <- args[[2]]
csv_path <- args[[3]]

suppressPackageStartupMessages(library(SeuratObject))
suppressPackageStartupMessages(library(jsonlite))

obj <- readRDS(rds_path)
obj_class <- class(obj)
meta_cols <- colnames(obj[[]])
required <- c("lin","startID","well","rep")
missing <- setdiff(required, meta_cols)
if (length(missing) > 0) stop(paste("missing required metadata columns:", paste(missing, collapse=",")))

md <- obj[[]][, required, drop=FALSE]
md$cell_id <- rownames(md)

# Do not access assays, reductions, cluster/state fields, or any other metadata values.
if (any(is.na(md$lin)) || any(md$lin == "")) stop("missing lineage assignments in retained cells")
if (any(is.na(md$startID)) || any(md$startID == "")) stop("missing startID assignments")

lineage_ids <- sort(unique(as.character(md$lin)))
rows <- lapply(lineage_ids, function(lin) {
  x <- md[as.character(md$lin) == lin, , drop=FALSE]
  starts <- sort(unique(as.character(x$startID)))
  data.frame(
    Lineage=lin,
    StartID=paste(starts, collapse="|"),
    n_cells=nrow(x),
    n_wells=length(unique(as.character(x$well))),
    n_reps=length(unique(as.character(x$rep))),
    stringsAsFactors=FALSE
  )
})
lin_df <- do.call(rbind, rows)

q <- list(
  minimum_unique_lineages = nrow(lin_df) >= 100,
  all_lineages_min_cells = all(lin_df$n_cells >= 4),
  all_lineages_max_cells = all(lin_df$n_cells <= 128),
  one_startID_per_lineage = all(!grepl("\\|", lin_df$StartID)),
  at_least_two_startID_classes = length(unique(lin_df$StartID)) >= 2
)
qualified <- all(unlist(q))

write.csv(lin_df, csv_path, row.names=FALSE, quote=TRUE)

result <- list(
  schema_version="0.1",
  status=if (qualified) "PASS_CARRIER_QUALIFICATION" else "FAIL_CARRIER_QUALIFICATION",
  object_class=obj_class,
  metadata_column_names=meta_cols,
  prohibited_metadata_values_read=FALSE,
  assay_values_read=FALSE,
  reduction_values_read=FALSE,
  retained_cell_count=nrow(md),
  unique_lineage_count=nrow(lin_df),
  lineage_size=list(
    min=min(lin_df$n_cells),
    median=as.numeric(median(lin_df$n_cells)),
    max=max(lin_df$n_cells),
    q25=as.numeric(quantile(lin_df$n_cells,0.25,names=FALSE)),
    q75=as.numeric(quantile(lin_df$n_cells,0.75,names=FALSE))
  ),
  startID_cell_counts=as.list(table(as.character(md$startID))),
  startID_lineage_counts=as.list(table(lin_df$StartID)),
  well_count=length(unique(as.character(md$well))),
  rep_count=length(unique(as.character(md$rep))),
  qualification_checks=q,
  carrier_defined=qualified,
  causal_inheritance="NOT_ESTABLISHED",
  lineage_table_sha256=NA_character_
)

rm(obj); gc()
write_json(result, json_path, pretty=TRUE, auto_unbox=TRUE, digits=16)
cat(toJSON(result, pretty=TRUE, auto_unbox=TRUE, digits=16))
cat("\nBIO_CHI_HARMANGE_EXP1_CARRIER_EXTRACTION_DONE\n")
