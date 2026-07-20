#!/usr/bin/env python
from __future__ import annotations

import argparse
import gzip
from pathlib import Path

import anndata as ad
import numpy as np
import pandas as pd
import scipy.io
from scipy import sparse

from pipeline_utils import project_path


RAW_DIR = project_path("data/public_references/raw/GSE161332")
PROCESSED_DIR = project_path("data/public_references/processed")


def read_barcodes(path: Path) -> list[str]:
    with gzip.open(path, "rt") as handle:
        return [line.strip() for line in handle if line.strip()]


def read_features(path: Path) -> pd.DataFrame:
    features = pd.read_csv(path, sep="\t", header=None, compression="gzip")

    if features.shape[1] >= 2:
        features = features.iloc[:, :2].copy()
        features.columns = ["gene_id", "gene_name"]
    else:
        features = features.iloc[:, :1].copy()
        features.columns = ["gene_id"]
        features["gene_name"] = features["gene_id"].astype(str)

    features["gene_id"] = features["gene_id"].astype(str)
    features["gene_name"] = features["gene_name"].astype(str)
    return features


def build_adata(raw_dir: Path) -> ad.AnnData:
    matrix_path = raw_dir / "GSE161332_matrix.mtx.gz"
    barcodes_path = raw_dir / "GSE161332_barcodes.tsv.gz"
    features_path = raw_dir / "GSE161332_features.tsv.gz"

    for path in [matrix_path, barcodes_path, features_path]:
        if not path.exists():
            raise FileNotFoundError(
                f"Missing {path}. Download the processed GSE161332 supplementary files from GEO first."
            )

    matrix = scipy.io.mmread(matrix_path).tocsr()
    barcodes = read_barcodes(barcodes_path)
    features = read_features(features_path)

    if matrix.shape != (features.shape[0], len(barcodes)):
        raise ValueError(
            f"Matrix shape {matrix.shape} does not match genes/cells {(features.shape[0], len(barcodes))}."
        )

    obs = pd.DataFrame(index=pd.Index(np.asarray(barcodes, dtype=object), name="cell_id"))
    obs["dataset_accession"] = "GSE161332"
    obs["source_tissue"] = "Arabidopsis_leaf"
    obs["reference_layer"] = "leaf_aerial"
    obs = obs.astype(object)

    var = features.copy()
    var.index = pd.Index(np.asarray(var["gene_name"].astype(str), dtype=object), name="feature_name")
    var = var.astype(object)

    adata = ad.AnnData(X=sparse.csr_matrix(matrix.transpose()), obs=obs, var=var)
    adata.layers["counts"] = adata.X.copy()
    adata.var_names_make_unique()
    adata.uns["dataset_accession"] = "GSE161332"
    adata.uns["dataset_title"] = "Single cell RNA sequencing of Col-0 leaf cell"
    adata.uns["dataset_role"] = "first_leaf_reference_extension"
    adata.uns["source_geo"] = "https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE161332"
    return adata


def main() -> None:
    parser = argparse.ArgumentParser(description="Convert GSE161332 Arabidopsis leaf 10x-style files into h5ad.")
    parser.add_argument("--raw-dir", default=str(RAW_DIR))
    parser.add_argument("--output", default=str(PROCESSED_DIR / "GSE161332_leaf.h5ad"))
    args = parser.parse_args()

    raw_dir = project_path(args.raw_dir)
    output_path = project_path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    adata = build_adata(raw_dir)
    ad.settings.allow_write_nullable_strings = True
    adata.write_h5ad(output_path)
    print(f"Wrote {output_path}")


if __name__ == "__main__":
    main()
