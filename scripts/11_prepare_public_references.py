#!/usr/bin/env python
from __future__ import annotations

from pathlib import Path

import anndata as ad
import pandas as pd
import scanpy as sc
from scipy import sparse

from pipeline_utils import project_path


RAW_DIR = project_path("data/public_references/raw")
PROCESSED_DIR = project_path("data/public_references/processed")


def prepare_gse227564() -> Path:
    counts_path = RAW_DIR / "GSE227564_counts.csv.gz"
    metadata_path = RAW_DIR / "GSE227564_metadata.csv.gz"

    counts = pd.read_csv(counts_path, index_col=0)
    metadata = pd.read_csv(metadata_path).rename(columns={"Unnamed: 0": "cell_id"}).set_index("cell_id")

    cell_ids = counts.columns.astype(str)
    metadata = metadata.loc[cell_ids].copy()
    metadata["seurat_clusters"] = metadata["seurat_clusters"].astype(str)

    adata = ad.AnnData(
        X=sparse.csr_matrix(counts.T.values),
        obs=metadata,
        var=pd.DataFrame(index=counts.index.astype(str)),
    )
    adata.layers["counts"] = adata.X.copy()
    adata.obs_names = cell_ids
    adata.var_names = counts.index.astype(str)
    adata.uns["dataset_accession"] = "GSE227564"
    adata.uns["dataset_title"] = "Identification of cell-types in Arabidopsis callus"

    output_path = PROCESSED_DIR / "GSE227564_callus.h5ad"
    adata.write_h5ad(output_path)
    return output_path


def prepare_gse141730() -> Path:
    matrix_path = RAW_DIR / "GSE141730_aggregated_filtered_gene_bc_matrices.h5"
    adata = sc.read_10x_h5(matrix_path)
    adata.var_names_make_unique()
    adata.layers["counts"] = adata.X.copy()
    adata.uns["dataset_accession"] = "GSE141730"
    adata.uns["dataset_title"] = "Vascular transcription factors control epidermal responses to limiting phosphate conditions"

    output_path = PROCESSED_DIR / "GSE141730_root_phosphate.h5ad"
    adata.write_h5ad(output_path)
    return output_path


def main() -> None:
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    written = [prepare_gse227564(), prepare_gse141730()]
    for path in written:
        print(f"Wrote {path}")


if __name__ == "__main__":
    main()
