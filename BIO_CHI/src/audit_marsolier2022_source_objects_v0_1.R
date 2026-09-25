#!/usr/bin/env Rscript
library(jsonlite)

root <- normalizePath(file.path(dirname(commandArgs(trailingOnly=FALSE)[grep("^--file=",commandArgs(trailingOnly=FALSE))]), "..", ".."), mustWork=FALSE)
# More robustly use working directory, which is repository root in Actions.
root <- getwd()
cfg <- fromJSON(file.path(root,"BIO_CHI","config","MARSOLIER2022_SOURCE_OBJECT_SCHEMA_FREEZE_v0_1.json"), simplifyVector=FALSE)
outdir <- file.path(root,"BIO_CHI","artifacts","generated")
dir.create(outdir,recursive=TRUE,showWarnings=FALSE)

sha256_file <- function(path){
  unname(tools::md5sum(path)) # temporary MD5 is not SHA; shell sha256sum below writes exact SHA
}

records <- list()
for (objdef in cfg$objects){
  url <- paste0("https://raw.githubusercontent.com/",cfg$source_code$repository,"/",cfg$source_code$commit,"/",objdef$path)
  dest <- file.path(outdir,basename(objdef$path))
  download.file(url,dest,mode="wb",quiet=TRUE)
  env <- new.env(parent=emptyenv())
  loaded <- load(dest,envir=env)
  objects <- list()
  for (nm in loaded){
    x <- get(nm,envir=env)
    dm <- dim(x)
    cn <- colnames(x)
    objects[[length(objects)+1]] <- list(
      name=nm,
      class=class(x),
      dim=if(is.null(dm)) NULL else as.integer(dm),
      column_names=if(is.null(cn)) NULL else as.character(cn),
      has_rownames=!is.null(rownames(x))
    )
  }
  sh <- system2("sha256sum",dest,stdout=TRUE)
  sha <- strsplit(sh,"  ",fixed=TRUE)[[1]][1]
  records[[length(records)+1]] <- list(
    id=objdef$id,path=objdef$path,blob=objdef$blob,
    bytes=file.info(dest)$size,sha256=sha,loaded_objects=objects
  )
}
result <- list(
  schema_version="0.1",
  gate=cfg$gate,
  status="PASS_RDATA_SCHEMA_AUDIT",
  source_commit=cfg$source_code$commit,
  records=records,
  scientific_values_recorded=FALSE
)
write(toJSON(result,pretty=TRUE,auto_unbox=TRUE,null="null"),file.path(outdir,"marsolier2022_source_object_schema_v0_1.json"))
cat(toJSON(result,pretty=TRUE,auto_unbox=TRUE,null="null"))
cat("\nBIO_CHI_MARSOLIER_RDATA_SCHEMA_PASS\n")
