#!/usr/bin/env python
from __future__ import annotations

import argparse
from pathlib import Path

import anndata as ad
import pandas as pd
import scipy.io
from scipy import sparse

from pipeline_utils import project_path


RAW_DIR = project_path("data/public_references/raw/GSE121619")
PROCESSED_DIR = project_path("data/public_references/processed")


def load_exported_split(split_name: str) -> ad.AnnData:
    export_dir = RAW_DIR / "exports" / split_name
    matrix_path = export_dir / "matrix.mtx"
    obs_path = export_dir / "obs.tsv"
    var_path = export_dir / "var.tsv"

    for path in [matrix_path, obs_path, var_path]:
        if not path.exists():
            raise FileNotFoundError(
                f"Missing {path}. Run `Rscript scripts/14_extract_gse121619_from_monocle.R {split_name}` first."
            )

    matrix = scipy.io.mmread(matrix_path).tocsr()
    obs = pd.read_csv(obs_path, sep="\t", index_col=0)
    var = pd.read_csv(var_path, sep="\t", index_col=0)

    if matrix.shape != (var.shape[0], obs.shape[0]):
        raise ValueError(
            f"Matrix shape {matrix.shape} does not match var/obs dimensions {(var.shape[0], obs.shape[0])}."
        )

    matrix = matrix.transpose().tocsr()

    if "gene_short_name" in var.columns:
        preferred_names = var["gene_short_name"].fillna("").astype(str)
        fallback_names = var.index.astype(str)
        var_names = preferred_names.where(preferred_names.str.len() > 0, fallback_names)
    else:
        var_names = var.index.astype(str)

    var = var.copy()
    var["gene_ids"] = var["id"].astype(str) if "id" in var.columns else var.index.astype(str)
    var.index = pd.Index(var_names.astype(str), name="gene_short_name")

    adata = ad.AnnData(X=sparse.csr_matrix(matrix), obs=obs.copy(), var=var.copy())
    adata.layers["counts"] = adata.X.copy()
    adata.var_names_make_unique()

    if "louvain_component" in adata.obs.columns:
        adata.obs["louvain_component"] = adata.obs["louvain_component"].astype(str)
    if "State" in adata.obs.columns:
        adata.obs["State"] = adata.obs["State"].astype(str)

    if {"UMAP1", "UMAP2"}.issubset(adata.obs.columns):
        adata.obsm["X_umap"] = adata.obs[["UMAP1", "UMAP2"]].astype(float).to_numpy()
    if {"TSNE.1", "TSNE.2"}.issubset(adata.obs.columns):
        adata.obsm["X_tsne"] = adata.obs[["TSNE.1", "TSNE.2"]].astype(float).to_numpy()

    adata.uns["dataset_accession"] = "GSE121619"
    adata.uns["dataset_title"] = "Dynamics of gene expression in single root cells of A. thaliana"
    adata.uns["source_split"] = split_name
    return adata


def main() -> None:
    parser = argparse.ArgumentParser(description="Convert exported GSE121619 Monocle split into h5ad.")
    parser.add_argument("--split", default="All", choices=["All", "control", "heatshock"])
    args = parser.parse_args()

    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    adata = load_exported_split(args.split)
    output_path = PROCESSED_DIR / f"GSE121619_{args.split.lower()}_root.h5ad"
    adata.write_h5ad(output_path)
    print(f"Wrote {output_path}")


if __name__ == "__main__":
    main()
