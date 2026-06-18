#!/usr/bin/env Rscript

args <- commandArgs(trailingOnly = TRUE)
if (length(args) < 1) {
  stop("Usage: Rscript scripts/14_extract_gse121619_from_monocle.R <split>\nExample: Rscript scripts/14_extract_gse121619_from_monocle.R All")
}

suppressPackageStartupMessages({
  library(monocle)
  library(Matrix)
})

split_name <- args[[1]]
raw_dir <- "data/public_references/raw/GSE121619"
input_path <- file.path(raw_dir, "GSE121619_Control_Heatshock_cds_unwrapped.rds")
export_dir <- file.path(raw_dir, "exports", split_name)

obj <- readRDS(input_path)
if (!split_name %in% names(obj)) {
  stop(sprintf("Split '%s' not found. Available splits: %s", split_name, paste(names(obj), collapse = ", ")))
}

cds <- obj[[split_name]]
dir.create(export_dir, recursive = TRUE, showWarnings = FALSE)

counts <- exprs(cds)
obs <- as.data.frame(pData(cds))
var <- as.data.frame(fData(cds))

writeMM(as(counts, "dgCMatrix"), file.path(export_dir, "matrix.mtx"))
write.table(obs, file.path(export_dir, "obs.tsv"), sep = "\t", quote = FALSE, row.names = TRUE, col.names = NA)
write.table(var, file.path(export_dir, "var.tsv"), sep = "\t", quote = FALSE, row.names = TRUE, col.names = NA)

cat(sprintf("Exported split %s to %s\n", split_name, export_dir))
