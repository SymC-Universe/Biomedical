#!/usr/bin/env Rscript

args <- commandArgs(trailingOnly = TRUE)
if (length(args) != 3) {
  stop("usage: export_stage_c1a_annotation.R <annotation.tar.gz> <chen.csv> <outdir>")
}
ann_tar <- normalizePath(args[[1]], mustWork = TRUE)
chen_csv <- normalizePath(args[[2]], mustWork = TRUE)
outdir <- args[[3]]
dir.create(outdir, recursive = TRUE, showWarnings = FALSE)

suppressPackageStartupMessages(library(S4Vectors))

pkg <- "IlluminaHumanMethylation450kanno.ilmn12.hg19"
extract_dir <- file.path(outdir, "_ann_extract")
unlink(extract_dir, recursive = TRUE, force = TRUE)
dir.create(extract_dir, recursive = TRUE, showWarnings = FALSE)
untar(ann_tar, exdir = extract_dir)

# Validate the exact frozen package identity directly from its source tarball.
desc_paths <- list.files(extract_dir, pattern = "^DESCRIPTION$", recursive = TRUE, full.names = TRUE)
if (length(desc_paths) != 1) stop(paste("expected exactly one DESCRIPTION, found", length(desc_paths)))
desc <- read.dcf(desc_paths[[1]])
if (desc[1, "Package"] != pkg) stop(paste("package mismatch:", desc[1, "Package"]))
if (desc[1, "Version"] != "0.6.0") stop(paste("version mismatch:", desc[1, "Version"]))

# Load only frozen DataFrame objects needed by C1A. We intentionally do not
# install/load the package itself, avoiding its historical minfi dependency.
data_files <- list.files(extract_dir, pattern = "\\.(rda|RData)$", recursive = TRUE, full.names = TRUE)
base <- basename(data_files)
keep <- grepl("^(Other|Locations|SNPs\\.[0-9]+CommonSingle)\\.(rda|RData)$", base)
needed_files <- data_files[keep]
if (length(needed_files) < 3) {
  stop(paste("could not locate required frozen DataFrame objects; available data files:", paste(base, collapse = ",")))
}

env <- new.env(parent = emptyenv())
loaded <- character()
for (f in needed_files) loaded <- c(loaded, load(f, envir = env))
loaded <- unique(loaded)
if (!("Other" %in% loaded) || !("Locations" %in% loaded)) {
  stop(paste("required Other/Locations objects not loaded; loaded:", paste(loaded, collapse = ",")))
}

other <- as.data.frame(get("Other", envir = env, inherits = FALSE), stringsAsFactors = FALSE)
locations <- as.data.frame(get("Locations", envir = env, inherits = FALSE), stringsAsFactors = FALSE)

snp_candidates <- grep("^SNPs\\.[0-9]+CommonSingle$", loaded, value = TRUE)
if (length(snp_candidates) == 0) stop("no SNPs.<build>CommonSingle object found in pinned annotation tarball")
builds <- as.integer(sub("^SNPs\\.([0-9]+)CommonSingle$", "\\1", snp_candidates))
selected_snp_name <- snp_candidates[[which.max(builds)]]
selected_snp <- as.data.frame(get(selected_snp_name, envir = env, inherits = FALSE), stringsAsFactors = FALSE)

required_other <- c("UCSC_RefGene_Name", "UCSC_RefGene_Accession", "UCSC_RefGene_Group")
missing_other <- setdiff(required_other, colnames(other))
if (length(missing_other) > 0) stop(paste("missing required Other columns:", paste(missing_other, collapse = ",")))
required_snp <- c("CpG_rs", "CpG_maf", "SBE_rs", "SBE_maf")
missing_snp <- setdiff(required_snp, colnames(selected_snp))
if (length(missing_snp) > 0) stop(paste("missing required SNP columns:", paste(missing_snp, collapse = ",")))

ids <- sort(unique(c(rownames(other), rownames(locations), rownames(selected_snp))))
out <- data.frame(probe_id = ids, stringsAsFactors = FALSE)
lookup <- function(df, col) {
  ans <- rep(NA_character_, length(ids)); idx <- match(ids, rownames(df)); ok <- !is.na(idx)
  if (col %in% colnames(df)) ans[ok] <- as.character(df[idx[ok], col])
  ans
}
lookup_num <- function(df, col) {
  ans <- rep(NA_real_, length(ids)); idx <- match(ids, rownames(df)); ok <- !is.na(idx)
  if (col %in% colnames(df)) ans[ok] <- suppressWarnings(as.numeric(df[idx[ok], col]))
  ans
}

out$chr <- lookup(locations, "chr")
out$pos <- lookup_num(locations, "pos")
out$strand <- lookup(locations, "strand")
out$UCSC_RefGene_Name <- lookup(other, "UCSC_RefGene_Name")
out$UCSC_RefGene_Accession <- lookup(other, "UCSC_RefGene_Accession")
out$UCSC_RefGene_Group <- lookup(other, "UCSC_RefGene_Group")
out$CpG_rs <- lookup(selected_snp, "CpG_rs")
out$CpG_maf <- lookup_num(selected_snp, "CpG_maf")
out$SBE_rs <- lookup(selected_snp, "SBE_rs")
out$SBE_maf <- lookup_num(selected_snp, "SBE_maf")
for (nm in colnames(out)) if (is.character(out[[nm]])) out[[nm]][is.na(out[[nm]])] <- ""

ann_out <- gzfile(file.path(outdir, "stage_c1a_annotation_export.tsv.gz"), open = "wt")
write.table(out, ann_out, sep = "\t", row.names = FALSE, col.names = TRUE, quote = TRUE, na = "")
close(ann_out)

chen <- read.csv(chen_csv, stringsAsFactors = FALSE, check.names = FALSE)
if (!("TargetID" %in% colnames(chen))) stop("Chen source missing TargetID")
chen_ids <- unique(trimws(as.character(chen$TargetID)))
chen_ids <- sort(chen_ids[nzchar(chen_ids)])
writeLines(chen_ids, file.path(outdir, "stage_c1a_chen_crossreactive_probe_ids.txt"), useBytes = TRUE)

inventory <- c(
  paste0("package=", pkg),
  "package_version=0.6.0",
  "extraction_mode=direct_frozen_tarball_dataframes_no_package_install",
  paste0("selected_common_snp_object=", selected_snp_name),
  paste0("annotation_export_rows=", nrow(out)),
  paste0("annotation_export_unique_probe_ids=", length(unique(out$probe_id))),
  paste0("other_rows=", nrow(other)),
  paste0("locations_rows=", nrow(locations)),
  paste0("selected_snp_rows=", nrow(selected_snp)),
  paste0("chen_unique_target_ids=", length(chen_ids)),
  paste0("available_common_snp_objects=", paste(sort(snp_candidates), collapse = ";"))
)
writeLines(inventory, file.path(outdir, "stage_c1a_annotation_object_inventory.txt"), useBytes = TRUE)
cat(paste(inventory, collapse = "\n"), "\n")
