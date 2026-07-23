#!/usr/bin/env Rscript

args <- commandArgs(trailingOnly = TRUE)
input_rds <- if (length(args) >= 1) args[[1]] else "data/public_references/raw/GSE161332/pscb_leaf/leaf.RDS"
output_csv <- if (length(args) >= 2) args[[2]] else "data/public_references/raw/GSE161332/pscb_leaf/leaf_metadata_from_pscb.csv"

local_library <- normalizePath(".Rlib", mustWork = FALSE)
if (dir.exists(local_library)) {
  .libPaths(c(local_library, .libPaths()))
}

if (!requireNamespace("SeuratObject", quietly = TRUE)) {
  stop(
    "SeuratObject is required to read the PSCB leaf.RDS file. ",
    "Install it locally with: mkdir -p .Rlib && Rscript -e \"install.packages('SeuratObject', repos='https://cloud.r-project.org', lib=normalizePath('.Rlib'))\""
  )
}

suppressPackageStartupMessages(library(SeuratObject))

object <- readRDS(input_rds)
metadata <- object@meta.data
dir.create(dirname(output_csv), recursive = TRUE, showWarnings = FALSE)
write.csv(metadata, output_csv)

cat("Wrote PSCB leaf metadata:", output_csv, "\n")
cat("Cells:", nrow(metadata), "\n")
cat("Columns:", paste(colnames(metadata), collapse = ", "), "\n")
