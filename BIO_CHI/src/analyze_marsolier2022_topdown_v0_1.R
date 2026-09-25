#!/usr/bin/env Rscript
suppressPackageStartupMessages(library(jsonlite))

root <- getwd()
cfg <- fromJSON(file.path(root,"BIO_CHI","config","MARSOLIER2022_TOPDOWN_EVENT_FREEZE_v0_1.json"), simplifyVector=FALSE)
outdir <- file.path(root,"BIO_CHI","artifacts","generated")
dir.create(outdir,recursive=TRUE,showWarnings=FALSE)

repo <- "vallotlab/ChemoPersistance"
commit <- "2c546ef7293f9dd58e0acf1c5d16e7616cf6789a"
defs <- list(
  pm=list(path="output/scRNAseq/MM468/Persister/Unsupervised/RData/persister_gene_cell_annot.RData",sha="83666f8d75965cf215a306278f71d03adbfa96fa688a6c4f36a70f6569b3e2fe",obj="annot_int"),
  pp=list(path="output/scRNAseq/MM468/Persister/Unsupervised/RData/pca_persister.RData",sha="79a244bae180a9fc9ad7663a9faaf93c0cb1c3b1e960a7cbdd9426ee9570f00d",obj="pca_object"),
  um=list(path="output/scRNAseq/MM468/UNC_5FU/Unsupervised/RData/annot_int.RData",sha="c92e431a717d88b154d6b39f09ddcc63ade2cab9165c35f2ad2c638efb9917dc",obj="annot_int"),
  up=list(path="output/scRNAseq/MM468/UNC_5FU/Unsupervised/RData/pca_UNC_5FU.RData",sha="21ce11bc0fa188f6f6e6fce2862c52c4587b41dce664413495d2fbae2d307b70",obj="pca_object")
)

sha256_file <- function(path){
  z <- system2("sha256sum",path,stdout=TRUE)
  strsplit(z,"  ",fixed=TRUE)[[1]][1]
}
get_obj <- function(d,key){
  dest <- file.path(outdir,paste0(key,".RData"))
  url <- paste0("https://raw.githubusercontent.com/",repo,"/",commit,"/",d$path)
  download.file(url,dest,mode="wb",quiet=TRUE)
  if(sha256_file(dest) != d$sha) stop(paste("SHA mismatch",key))
  e <- new.env(parent=emptyenv())
  n <- load(dest,envir=e)
  if(!(d$obj %in% n)) stop(paste("missing object",d$obj))
  get(d$obj,envir=e)
}
valid_bc <- function(x){
  !is.na(x) & trimws(as.character(x)) != "" & trimws(as.character(x)) != "NA"
}
align_pca <- function(meta,pca){
  ii <- match(as.character(meta$cell_id),rownames(pca))
  if(any(is.na(ii))) stop(paste("PCA alignment missing",sum(is.na(ii)),"cells"))
  pca[ii,,drop=FALSE]
}
retain80 <- function(x){
  v <- apply(x,2,var,na.rm=TRUE)
  v[!is.finite(v)] <- 0
  r <- v/sum(v)
  k <- which(cumsum(r)>=0.80)[1]
  list(k=as.integer(k),ratio=r,cum=cumsum(r))
}
zscale <- function(x){
  m <- colMeans(x)
  s <- apply(x,2,sd)
  keep <- is.finite(s) & s>0
  sweep(sweep(x[,keep,drop=FALSE],2,m[keep],"-"),2,s[keep],"/")
}
centroid_dist <- function(z,y){
  a <- colMeans(z[y,,drop=FALSE])
  b <- colMeans(z[!y,,drop=FALSE])
  sqrt(sum((a-b)^2))
}
balacc_loo <- function(z,y){
  n <- nrow(z)
  pr <- rep(NA,n)
  for(i in seq_len(n)){
    tr <- setdiff(seq_len(n),i)
    yy <- y[tr]
    if(sum(yy)<1 || sum(!yy)<1) next
    c1 <- colMeans(z[tr[yy],,drop=FALSE])
    c0 <- colMeans(z[tr[!yy],,drop=FALSE])
    pr[i] <- sum((z[i,]-c1)^2) < sum((z[i,]-c0)^2)
  }
  ok <- !is.na(pr)
  if(sum(ok & y)==0 || sum(ok & !y)==0) return(NA_real_)
  (mean(pr[ok & y]) + mean(!pr[ok & !y]))/2
}
permute_modal <- function(z,y,B=10000,seed=20260924){
  set.seed(seed)
  od <- centroid_dist(z,y)
  ob <- balacc_loo(z,y)
  pd <- numeric(B)
  pb <- numeric(B)
  for(i in seq_len(B)){
    yp <- sample(y,length(y),replace=FALSE)
    pd[i] <- centroid_dist(z,yp)
    pb[i] <- balacc_loo(z,yp)
  }
  list(
    observed_distance=od,
    distance_p=(1+sum(pd>=od))/(B+1),
    distance_perm_mean=mean(pd),
    distance_perm_q95=as.numeric(quantile(pd,0.95,names=FALSE)),
    observed_balanced_accuracy=ob,
    balanced_accuracy_p=(1+sum(pb>=ob,na.rm=TRUE))/(1+sum(is.finite(pb))),
    balanced_accuracy_perm_mean=mean(pb,na.rm=TRUE),
    permutations=B,
    seed=seed
  )
}
lineage_div <- function(x){
  x <- as.character(x[valid_bc(x)])
  n <- length(x)
  if(n==0) return(list(barcoded_cells=0,unique_lineages=0,unique_fraction=NULL,normalized_shannon=NULL))
  tb <- table(x)
  k <- length(tb)
  p <- as.numeric(tb)/sum(tb)
  h <- -sum(p*log(p))
  hn <- if(k==1) 0 else h/log(k)
  list(barcoded_cells=n,unique_lineages=k,unique_fraction=k/n,normalized_shannon=hn)
}
sample_centroid <- function(z,meta,s){
  ii <- which(as.character(meta$sample_id)==s)
  if(length(ii)==0) return(NULL)
  colMeans(z[ii,,drop=FALSE])
}

pm <- get_obj(defs$pm,"pm")
pp <- align_pca(pm,get_obj(defs$pp,"pp"))
um <- get_obj(defs$um,"um")
up <- align_pca(um,get_obj(defs$up,"up"))

early <- unlist(cfg$source_defined_samples$early_persister,use.names=FALSE)
base_sample <- cfg$source_defined_samples$chemonaive[[1]]
early_barcodes <- unique(as.character(pm$cons_BC_lenti[as.character(pm$sample_id) %in% early & valid_bc(pm$cons_BC_lenti)]))
base_idx <- which(as.character(pm$sample_id)==base_sample & valid_bc(pm$cons_BC_lenti))
if(length(base_idx)==0) stop("no barcoded baseline cells")
base_bc <- as.character(pm$cons_BC_lenti[base_idx])

rp <- retain80(pp)
p <- pp[,seq_len(rp$k),drop=FALSE]
u <- sort(unique(base_bc))
L <- matrix(NA_real_,nrow=length(u),ncol=rp$k,dimnames=list(u,colnames(p)))
lc <- integer(length(u))
for(i in seq_along(u)){
  ii <- base_idx[base_bc==u[i]]
  L[i,] <- colMeans(p[ii,,drop=FALSE])
  lc[i] <- length(ii)
}
future <- u %in% early_barcodes
if(sum(future)<2 || sum(!future)<2) stop("insufficient baseline lineage groups")
Z <- zscale(L)
pt <- permute_modal(Z,future,10000,20260924)
modal_pass <- is.finite(pt$distance_p) && pt$distance_p <= as.numeric(cfg$baseline_modal_test$alpha)

pairs <- cfg$source_defined_samples$unc5fu_matched
flat <- unlist(pairs,use.names=FALSE)
missing_samples <- setdiff(flat,unique(as.character(um$sample_id)))
if(length(missing_samples)>0) stop(paste("missing matched samples",paste(missing_samples,collapse=",")))

div <- list()
for(s in flat) div[[s]] <- lineage_div(um$cons_BC_lenti[as.character(um$sample_id)==s])
pair_results <- list()
dirpass <- logical(length(pairs))
for(i in seq_along(pairs)){
  a <- pairs[[i]][[1]]
  b <- pairs[[i]][[2]]
  dirpass[i] <- div[[b]]$unique_fraction > div[[a]]$unique_fraction
  pair_results[[paste0("pair",i)]] <- list(
    fiveFU=a,
    unc_plus_5FU=b,
    fiveFU_metrics=div[[a]],
    unc_plus_5FU_metrics=div[[b]],
    delta_unique_fraction=div[[b]]$unique_fraction-div[[a]]$unique_fraction,
    delta_normalized_shannon=div[[b]]$normalized_shannon-div[[a]]$normalized_shannon,
    primary_direction_pass=dirpass[i]
  )
}
lineage_gate <- all(dirpass)

sel <- which(as.character(um$sample_id) %in% flat & !is.na(um$louvain_partition) & !is.na(um$CDH2))
parts2 <- sort(unique(as.character(um$louvain_partition[sel])))
med <- sapply(parts2,function(g) median(um$CDH2[sel][as.character(um$louvain_partition[sel])==g],na.rm=TRUE))
mx <- max(med,na.rm=TRUE)
high <- sort(parts2[med==mx])[1]
cluster_div <- list()
cluster_ok <- TRUE
min_cells <- as.integer(cfg$substrate_intervention_lineage_test$cluster_specific_sensitivity$minimum_barcoded_cells_per_sample_cluster)
for(s in flat){
  ii <- which(as.character(um$sample_id)==s & as.character(um$louvain_partition)==high)
  cluster_div[[s]] <- lineage_div(um$cons_BC_lenti[ii])
  if(cluster_div[[s]]$barcoded_cells < min_cells) cluster_ok <- FALSE
}
cluster_pairs <- list()
if(cluster_ok){
  for(i in seq_along(pairs)){
    a <- pairs[[i]][[1]]
    b <- pairs[[i]][[2]]
    cluster_pairs[[paste0("pair",i)]] <- list(
      delta_unique_fraction=cluster_div[[b]]$unique_fraction-cluster_div[[a]]$unique_fraction,
      delta_normalized_shannon=cluster_div[[b]]$normalized_shannon-cluster_div[[a]]$normalized_shannon,
      direction_pass=cluster_div[[b]]$unique_fraction>cluster_div[[a]]$unique_fraction
    )
  }
}

ru <- retain80(up)
uz <- zscale(up[,seq_len(ru$k),drop=FALSE])
modal_pairs <- list()
for(i in seq_along(pairs)){
  a <- pairs[[i]][[1]]
  b <- pairs[[i]][[2]]
  ca <- sample_centroid(uz,um,a)
  cb <- sample_centroid(uz,um,b)
  if(is.null(ca) || is.null(cb)) stop("missing intervention modal sample")
  modal_pairs[[paste0("pair",i)]] <- list(
    fiveFU=a,
    unc_plus_5FU=b,
    centroid_distance=sqrt(sum((ca-cb)^2))
  )
}
chem <- c("MM468_chemonaive","MM468_chemonaive_2")
chem_present <- chem[chem %in% unique(as.character(um$sample_id))]
chem_comp <- NULL
if(length(chem_present)==2){
  c1 <- sample_centroid(uz,um,chem_present[1])
  c2 <- sample_centroid(uz,um,chem_present[2])
  chem_comp <- list(samples=chem_present,centroid_distance=sqrt(sum((c1-c2)^2)))
}

bio_status <- if(lineage_gate) "P0Q_SUBSTRATE_CONDITIONED_LINEAGE_FATE_SUPPORTED" else "P0Q_SUBSTRATE_CONDITIONED_LINEAGE_FATE_NOT_REPRODUCED_IN_FROZEN_SINGLE_CELL_GATE"
modal_status <- if(modal_pass) "P0Q_BASELINE_TRANSCRIPTOMIC_MODAL_INHERITANCE_SUPPORTED" else "P0Q_BASELINE_TRANSCRIPTOMIC_MODAL_INHERITANCE_NOT_DETECTED"

result <- list(
  schema_version="0.1",
  gate="Marsolier 2022 top-down substrate-conditioned persistence inheritance",
  status="PASS_ANALYSIS_EXECUTED",
  baseline_modal=list(
    retained_pc_count=rp$k,
    cumulative_variance=rp$cum[rp$k],
    baseline_barcoded_cells=length(base_idx),
    baseline_lineages=length(u),
    future_persister_lineages=sum(future),
    nonpersisting_lineages=sum(!future),
    future_persister_cells=sum(base_bc %in% u[future]),
    nonpersisting_cells=sum(base_bc %in% u[!future]),
    standardized_pc_count=ncol(Z),
    permutation=pt,
    disposition=modal_status
  ),
  intervention_lineage=list(
    sample_metrics=div,
    matched_pairs=pair_results,
    directional_gate=lineage_gate,
    disposition=bio_status,
    cdh2_high_cluster_sensitivity=list(
      selected_partition=high,
      partition_median_CDH2=as.list(med),
      evaluable=cluster_ok,
      sample_metrics=cluster_div,
      matched_pairs=cluster_pairs
    )
  ),
  intervention_modal=list(
    retained_pc_count=ru$k,
    cumulative_variance=ru$cum[ru$k],
    standardized_pc_count=ncol(uz),
    matched_pair_centroid_distances=modal_pairs,
    chemonaive_comparator=chem_comp,
    promotion_rule="DESCRIPTIVE_ONLY_NO_DIRECTIONAL_SUCCESS_RULE"
  ),
  scalar=list(opened=FALSE,disposition="SCALAR_NOT_REQUIRED_AND_NOT_LICENSED"),
  topdown_disposition=list(
    Bio_Chi_relation=bio_status,
    modal_inheritance=modal_status,
    scalar="NOT_REQUIRED",
    heldout_external_replication="SOURCE_REPORTED_CONTEXT_ONLY"
  ),
  epistemic=list(tier="P0-Q",source_outcomes_known=TRUE,P1_confirmation=FALSE)
)

write(toJSON(result,pretty=TRUE,auto_unbox=TRUE,null="null",digits=16),
      file.path(outdir,"marsolier2022_topdown_analysis_v0_1.json"))

md <- c(
  "# Marsolier 2022 top-down Bio Chi analysis v0.1",
  "",
  paste0("Bio Chi lineage gate: ",bio_status),
  paste0("Baseline modal inheritance: ",modal_status),
  "",
  "## Baseline lineage modal test",
  paste0("- barcoded chemonaive cells: ",length(base_idx)),
  paste0("- baseline lineages: ",length(u)," (future ",sum(future),"; nonpersisting ",sum(!future),")"),
  paste0("- retained PCs to >=80% score variance: ",rp$k),
  paste0("- centroid separation: ",format(pt$observed_distance,digits=8)),
  paste0("- lineage-label permutation p: ",format(pt$distance_p,digits=8)),
  paste0("- LOOCV balanced accuracy: ",format(pt$observed_balanced_accuracy,digits=8)),
  paste0("- balanced-accuracy permutation p: ",format(pt$balanced_accuracy_p,digits=8)),
  "",
  "## H3K27 substrate-intervention lineage test"
)
for(nm in names(pair_results)){
  x <- pair_results[[nm]]
  md <- c(md,paste0("- ",x$fiveFU," -> ",x$unc_plus_5FU,
    ": delta unique-lineage fraction = ",format(x$delta_unique_fraction,digits=8),
    "; delta normalized Shannon = ",format(x$delta_normalized_shannon,digits=8),
    "; pass = ",x$primary_direction_pass))
}
md <- c(md,"",paste0("Primary two-lane lineage gate: ",lineage_gate),
  "",
  "## Scalar gate",
  "No scalar was opened. The persistence/inheritance event is testable without inventing a continuous-time scalar carrier.",
  "",
  "## Ceiling",
  "P0-Q only. The source-native PCA basis includes outcome samples, so this qualifies representation and joint meaning rather than prospective prediction."
)
writeLines(md,file.path(outdir,"MARSOLIER2022_TOPDOWN_ANALYSIS_V01_AUDIT.md"))

cat(toJSON(list(
  biochi_status=bio_status,
  modal_status=modal_status,
  baseline_modal=result$baseline_modal,
  intervention_lineage=result$intervention_lineage,
  intervention_modal=result$intervention_modal,
  scalar=result$scalar
),pretty=TRUE,auto_unbox=TRUE,null="null",digits=16))
cat("\nBIO_CHI_MARSOLIER_TOPDOWN_ANALYSIS_DONE\n")
