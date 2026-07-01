#!/usr/bin/env python
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from collections import Counter
from pathlib import Path
from urllib.parse import unquote

os.environ.setdefault("MPLCONFIGDIR", "/private/tmp/mplconfig")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from pipeline_utils import PROJECT_ROOT


REFERENCE_ROOT = PROJECT_ROOT / "data" / "reference" / "orthology"
DEFAULT_SELECTED_GENES = PROJECT_ROOT / "results" / "root_reference_consensus" / "selected_genes.csv"
DEFAULT_MARKERS = PROJECT_ROOT / "data" / "metadata" / "public_reference_program_markers.csv"
DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "results" / "orthology"
DEFAULT_FIGURE_DIR = PROJECT_ROOT / "figures" / "orthology"
DEFAULT_MODEL_MAPPING = PROJECT_ROOT / "data" / "metadata" / "arabidopsis_wolffia_model_orthologs.csv"
DEFAULT_MARKER_MAPPING = PROJECT_ROOT / "data" / "metadata" / "wolffia_program_marker_orthologs.csv"
DEFAULT_TRANSFER_FEATURES = PROJECT_ROOT / "data" / "metadata" / "wolffia_transfer_feature_set.csv"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build Arabidopsis-to-Wolffia reciprocal protein ortholog mappings with DIAMOND."
    )
    parser.add_argument("--reference-root", type=Path, default=REFERENCE_ROOT)
    parser.add_argument("--selected-genes", type=Path, default=DEFAULT_SELECTED_GENES)
    parser.add_argument("--markers", type=Path, default=DEFAULT_MARKERS)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--figure-dir", type=Path, default=DEFAULT_FIGURE_DIR)
    parser.add_argument("--model-mapping", type=Path, default=DEFAULT_MODEL_MAPPING)
    parser.add_argument("--marker-mapping", type=Path, default=DEFAULT_MARKER_MAPPING)
    parser.add_argument("--transfer-features", type=Path, default=DEFAULT_TRANSFER_FEATURES)
    environment_diamond = Path(sys.executable).with_name("diamond")
    parser.add_argument(
        "--diamond",
        default=str(environment_diamond) if environment_diamond.exists() else "diamond",
    )
    parser.add_argument("--threads", type=int, default=4)
    parser.add_argument("--evalue", type=float, default=1e-5)
    parser.add_argument("--min-identity", type=float, default=25.0)
    parser.add_argument("--min-query-coverage", type=float, default=50.0)
    parser.add_argument("--min-subject-coverage", type=float, default=40.0)
    return parser.parse_args()


def find_single(root: Path, filename: str) -> Path:
    matches = sorted(root.rglob(filename))
    if len(matches) != 1:
        raise FileNotFoundError(f"Expected one {filename} under {root}, found {len(matches)}")
    return matches[0]


def parse_attributes(text: str) -> dict[str, str]:
    attributes: dict[str, str] = {}
    for field in text.rstrip().split(";"):
        if "=" not in field:
            continue
        key, value = field.split("=", 1)
        attributes[key] = unquote(value)
    return attributes


def parse_gene_id(dbxref: str) -> str:
    for item in dbxref.split(","):
        if item.startswith("GeneID:"):
            return item.removeprefix("GeneID:")
    return ""


def parse_protein_gene_map(gff_path: Path, species: str) -> pd.DataFrame:
    records: dict[str, dict[str, str]] = {}
    with open(gff_path, encoding="utf-8") as handle:
        for line in handle:
            if line.startswith("#"):
                continue
            fields = line.rstrip("\n").split("\t")
            if len(fields) != 9 or fields[2] != "CDS":
                continue
            attributes = parse_attributes(fields[8])
            protein_id = attributes.get("protein_id", "")
            if not protein_id or protein_id in records:
                continue
            locus_tag = attributes.get("locus_tag", "")
            gene_symbol = attributes.get("gene", "")
            ncbi_gene_id = parse_gene_id(attributes.get("Dbxref", ""))
            if species == "arabidopsis":
                gene_key = locus_tag or gene_symbol or ncbi_gene_id
            else:
                gene_key = ncbi_gene_id or locus_tag or gene_symbol
            if not gene_key:
                continue
            records[protein_id] = {
                "protein_id": protein_id,
                "gene_key": gene_key,
                "ncbi_gene_id": ncbi_gene_id,
                "locus_tag": locus_tag,
                "gene_symbol": gene_symbol,
                "product": attributes.get("product", ""),
            }
    frame = pd.DataFrame(records.values())
    if frame.empty:
        raise ValueError(f"No protein-to-gene records were parsed from {gff_path}")
    return frame


def read_fasta(path: Path) -> dict[str, str]:
    sequences: dict[str, list[str]] = {}
    current_id: str | None = None
    with open(path, encoding="utf-8") as handle:
        for line in handle:
            if line.startswith(">"):
                current_id = line[1:].split()[0]
                sequences.setdefault(current_id, [])
            elif current_id is not None:
                sequences[current_id].append(line.strip())
    return {identifier: "".join(parts) for identifier, parts in sequences.items()}


def choose_longest_isoforms(mapping: pd.DataFrame, sequences: dict[str, str]) -> pd.DataFrame:
    frame = mapping[mapping["protein_id"].isin(sequences)].copy()
    frame["protein_length"] = frame["protein_id"].map(lambda protein: len(sequences[protein]))
    frame = frame.sort_values(["gene_key", "protein_length", "protein_id"], ascending=[True, False, True])
    return frame.drop_duplicates("gene_key", keep="first").reset_index(drop=True)


def write_fasta(records: pd.DataFrame, sequences: dict[str, str], output_path: Path) -> None:
    with open(output_path, "w", encoding="utf-8") as handle:
        for row in records.itertuples(index=False):
            sequence = sequences[row.protein_id]
            handle.write(f">{row.protein_id}\n")
            for start in range(0, len(sequence), 80):
                handle.write(sequence[start : start + 80] + "\n")


def run_command(command: list[str]) -> None:
    subprocess.run(command, check=True)


def run_diamond(
    diamond: str,
    query_fasta: Path,
    target_fasta: Path,
    database_path: Path,
    output_path: Path,
    threads: int,
    evalue: float,
) -> None:
    run_command([diamond, "makedb", "--in", str(target_fasta), "--db", str(database_path)])
    run_command(
        [
            diamond,
            "blastp",
            "--query",
            str(query_fasta),
            "--db",
            str(database_path),
            "--out",
            str(output_path),
            "--outfmt",
            "6",
            "qseqid",
            "sseqid",
            "pident",
            "length",
            "qlen",
            "slen",
            "evalue",
            "bitscore",
            "qcovhsp",
            "scovhsp",
            "--max-target-seqs",
            "10",
            "--evalue",
            str(evalue),
            "--threads",
            str(threads),
            "--quiet",
        ]
    )


HIT_COLUMNS = [
    "query_protein",
    "subject_protein",
    "percent_identity",
    "alignment_length",
    "query_length",
    "subject_length",
    "evalue",
    "bitscore",
    "query_coverage",
    "subject_coverage",
]


def read_hits(path: Path) -> pd.DataFrame:
    if path.stat().st_size == 0:
        return pd.DataFrame(columns=HIT_COLUMNS)
    return pd.read_csv(path, sep="\t", names=HIT_COLUMNS)


def collapse_hits_to_genes(
    hits: pd.DataFrame,
    query_map: pd.DataFrame,
    subject_map: pd.DataFrame,
) -> pd.DataFrame:
    query_columns = query_map.add_prefix("query_")
    subject_columns = subject_map.add_prefix("subject_")
    merged = hits.merge(
        query_columns,
        left_on="query_protein",
        right_on="query_protein_id",
        how="inner",
    ).merge(
        subject_columns,
        left_on="subject_protein",
        right_on="subject_protein_id",
        how="inner",
    )
    merged = merged.sort_values(
        ["query_gene_key", "bitscore", "evalue", "percent_identity"],
        ascending=[True, False, True, False],
    )
    return merged.drop_duplicates(["query_gene_key", "subject_gene_key"], keep="first")


def ranked_gene_hits(gene_hits: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    ranked = gene_hits.copy()
    ranked["rank"] = ranked.groupby("query_gene_key").cumcount() + 1
    best = ranked[ranked["rank"] == 1].copy()
    second_scores = (
        ranked[ranked["rank"] == 2]
        .set_index("query_gene_key")["bitscore"]
        .rename("second_bitscore")
    )
    best = best.join(second_scores, on="query_gene_key")
    best["top_hit_score_ratio"] = best["bitscore"] / best["second_bitscore"].replace(0, np.nan)
    best["top_hit_score_ratio"] = best["top_hit_score_ratio"].fillna(np.inf)
    return best, ranked


def build_mapping(
    requested_genes: list[str],
    forward_best: pd.DataFrame,
    reverse_best: pd.DataFrame,
    min_identity: float,
    min_query_coverage: float,
    min_subject_coverage: float,
) -> pd.DataFrame:
    forward_by_gene = forward_best.set_index("query_gene_key")
    reverse_lookup = reverse_best.set_index("query_gene_key")["subject_gene_key"].to_dict()
    top_subject_counts = Counter(forward_best["subject_gene_key"].astype(str))
    rows: list[dict[str, object]] = []

    for gene in requested_genes:
        if gene not in forward_by_gene.index:
            rows.append(
                {
                    "arabidopsis_gene_id": gene,
                    "orthology_status": "no_hit",
                    "mapping_confidence": "unmapped",
                }
            )
            continue

        hit = forward_by_gene.loc[gene]
        wolffia_gene = str(hit["subject_gene_key"])
        passes_base = (
            hit["percent_identity"] >= min_identity
            and hit["query_coverage"] >= min_query_coverage
            and hit["subject_coverage"] >= min_subject_coverage
        )
        reciprocal = reverse_lookup.get(wolffia_gene) == gene
        well_separated = hit["top_hit_score_ratio"] >= 1.10
        high_quality = (
            reciprocal
            and hit["percent_identity"] >= 35
            and hit["query_coverage"] >= 70
            and hit["subject_coverage"] >= 50
            and well_separated
        )
        if not passes_base:
            confidence = "unmapped"
            status = "below_threshold"
        elif high_quality:
            confidence = "high"
            status = "reciprocal_best_hit"
        elif reciprocal:
            confidence = "medium"
            status = "reciprocal_best_hit"
        else:
            confidence = "low"
            status = "directional_best_hit"

        rows.append(
            {
                "arabidopsis_gene_id": gene,
                "arabidopsis_protein_id": hit["query_protein_id"],
                "arabidopsis_gene_symbol": hit["query_gene_symbol"],
                "wolffia_gene_key": wolffia_gene,
                "wolffia_ncbi_gene_id": hit["subject_ncbi_gene_id"],
                "wolffia_locus_tag": hit["subject_locus_tag"],
                "wolffia_gene_symbol": hit["subject_gene_symbol"],
                "wolffia_protein_id": hit["subject_protein_id"],
                "wolffia_product": hit["subject_product"],
                "percent_identity": hit["percent_identity"],
                "query_coverage": hit["query_coverage"],
                "subject_coverage": hit["subject_coverage"],
                "evalue": hit["evalue"],
                "bitscore": hit["bitscore"],
                "top_hit_score_ratio": hit["top_hit_score_ratio"],
                "reciprocal_best_hit": reciprocal,
                "arabidopsis_genes_sharing_wolffia_top_hit": top_subject_counts[wolffia_gene],
                "orthology_status": status,
                "mapping_confidence": confidence,
            }
        )
    return pd.DataFrame(rows)


def save_coverage_figures(
    marker_mapping: pd.DataFrame,
    model_mapping: pd.DataFrame,
    output_path: Path,
) -> None:
    confidence_order = ["high", "medium", "low", "unmapped"]
    marker_counts = (
        marker_mapping.groupby(["program", "mapping_confidence"], observed=True)
        .size()
        .unstack(fill_value=0)
        .reindex(columns=confidence_order, fill_value=0)
    )
    marker_proportions = marker_counts.div(marker_counts.sum(axis=1), axis=0)
    model_counts = model_mapping["mapping_confidence"].value_counts().reindex(confidence_order, fill_value=0)

    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    marker_proportions.plot(
        kind="barh",
        stacked=True,
        color=["#59A14F", "#4C78A8", "#F28E2B", "#BAB0AC"],
        ax=axes[0],
    )
    axes[0].set_xlim(0, 1)
    axes[0].set_xlabel("Fraction of program markers")
    axes[0].set_ylabel("Broad program")
    axes[0].set_title("Marker ortholog coverage by confidence")
    axes[0].legend(title="Mapping confidence", loc="lower right")

    sns.barplot(
        x=model_counts.index,
        y=model_counts.values,
        hue=model_counts.index,
        palette=["#59A14F", "#4C78A8", "#F28E2B", "#BAB0AC"],
        legend=False,
        ax=axes[1],
    )
    axes[1].set_xlabel("Mapping confidence")
    axes[1].set_ylabel("Model features")
    axes[1].set_title("2,000-feature model ortholog coverage")
    fig.tight_layout()
    fig.savefig(output_path, dpi=220, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    args = parse_args()
    if shutil.which(args.diamond) is None:
        raise FileNotFoundError(f"DIAMOND executable not found: {args.diamond}")
    args.output_dir.mkdir(parents=True, exist_ok=True)
    args.figure_dir.mkdir(parents=True, exist_ok=True)
    args.model_mapping.parent.mkdir(parents=True, exist_ok=True)
    args.marker_mapping.parent.mkdir(parents=True, exist_ok=True)
    args.transfer_features.parent.mkdir(parents=True, exist_ok=True)
    work_dir = args.output_dir / "work"
    work_dir.mkdir(parents=True, exist_ok=True)

    arabidopsis_root = args.reference_root / "arabidopsis"
    wolffia_root = args.reference_root / "wolffia"
    arabidopsis_proteins = find_single(arabidopsis_root, "protein.faa")
    arabidopsis_gff = find_single(arabidopsis_root, "genomic.gff")
    wolffia_proteins = find_single(wolffia_root, "protein.faa")
    wolffia_gff = find_single(wolffia_root, "genomic.gff")

    selected_genes = pd.read_csv(args.selected_genes)["selected_gene"].dropna().astype(str).tolist()
    marker_table = pd.read_csv(args.markers)
    marker_genes = marker_table["gene_id"].dropna().astype(str).tolist()
    requested_genes = list(dict.fromkeys([*selected_genes, *marker_genes]))

    arabidopsis_map = parse_protein_gene_map(arabidopsis_gff, "arabidopsis")
    wolffia_map = parse_protein_gene_map(wolffia_gff, "wolffia")
    arabidopsis_sequences = read_fasta(arabidopsis_proteins)
    wolffia_sequences = read_fasta(wolffia_proteins)
    arabidopsis_longest = choose_longest_isoforms(arabidopsis_map, arabidopsis_sequences)
    wolffia_longest = choose_longest_isoforms(wolffia_map, wolffia_sequences)

    arabidopsis_all_fasta = work_dir / "arabidopsis_longest_proteins.faa"
    wolffia_all_fasta = work_dir / "wolffia_longest_proteins.faa"
    arabidopsis_query_fasta = work_dir / "arabidopsis_requested_proteins.faa"
    write_fasta(arabidopsis_longest, arabidopsis_sequences, arabidopsis_all_fasta)
    write_fasta(wolffia_longest, wolffia_sequences, wolffia_all_fasta)
    arabidopsis_requested = arabidopsis_longest[
        arabidopsis_longest["gene_key"].isin(requested_genes)
    ].copy()
    write_fasta(arabidopsis_requested, arabidopsis_sequences, arabidopsis_query_fasta)

    forward_tsv = work_dir / "arabidopsis_to_wolffia.tsv"
    reverse_tsv = work_dir / "wolffia_to_arabidopsis.tsv"
    run_diamond(
        args.diamond,
        arabidopsis_query_fasta,
        wolffia_all_fasta,
        work_dir / "wolffia_db",
        forward_tsv,
        args.threads,
        args.evalue,
    )
    run_diamond(
        args.diamond,
        wolffia_all_fasta,
        arabidopsis_all_fasta,
        work_dir / "arabidopsis_db",
        reverse_tsv,
        args.threads,
        args.evalue,
    )

    forward_gene_hits = collapse_hits_to_genes(
        read_hits(forward_tsv),
        arabidopsis_longest,
        wolffia_longest,
    )
    reverse_gene_hits = collapse_hits_to_genes(
        read_hits(reverse_tsv),
        wolffia_longest,
        arabidopsis_longest,
    )
    forward_best, _ = ranked_gene_hits(forward_gene_hits)
    reverse_best, _ = ranked_gene_hits(reverse_gene_hits)
    full_mapping = build_mapping(
        requested_genes,
        forward_best,
        reverse_best,
        args.min_identity,
        args.min_query_coverage,
        args.min_subject_coverage,
    )

    model_mapping = pd.DataFrame({"arabidopsis_gene_id": selected_genes}).merge(
        full_mapping,
        on="arabidopsis_gene_id",
        how="left",
    )
    model_mapping["mapping_confidence"] = model_mapping["mapping_confidence"].fillna("unmapped")
    marker_mapping = marker_table.merge(
        full_mapping,
        left_on="gene_id",
        right_on="arabidopsis_gene_id",
        how="left",
    )
    marker_mapping["mapping_confidence"] = marker_mapping["mapping_confidence"].fillna("unmapped")
    model_mapping.to_csv(args.model_mapping, index=False)
    marker_mapping.to_csv(args.marker_mapping, index=False)
    transfer_features = model_mapping[
        model_mapping["mapping_confidence"].isin(["high", "medium"])
    ].copy()
    transfer_features.to_csv(args.transfer_features, index=False)

    coverage = (
        marker_mapping.assign(mapped=marker_mapping["mapping_confidence"].isin(["high", "medium"]))
        .groupby("program", observed=True)
        .agg(
            n_markers=("gene_id", "size"),
            n_high_confidence=("mapping_confidence", lambda values: (values == "high").sum()),
            n_high_or_medium=("mapped", "sum"),
        )
        .reset_index()
    )
    coverage["high_confidence_coverage"] = coverage["n_high_confidence"] / coverage["n_markers"]
    coverage["high_or_medium_coverage"] = coverage["n_high_or_medium"] / coverage["n_markers"]
    coverage.to_csv(args.output_dir / "program_ortholog_coverage.csv", index=False)

    save_coverage_figures(
        marker_mapping,
        model_mapping,
        args.figure_dir / "ortholog_coverage_summary.png",
    )

    diamond_version = subprocess.run(
        [args.diamond, "version"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    model_counts = model_mapping["mapping_confidence"].value_counts().to_dict()
    summary = {
        "arabidopsis_assembly": "GCF_000001735.4",
        "wolffia_assembly": "GCF_029677425.1",
        "wolffia_annotation_release": "GCF_029677425.1-RS_2025_12",
        "method": "gene-level reciprocal best protein hits after longest-isoform selection",
        "diamond_version": diamond_version,
        "n_requested_model_features": len(selected_genes),
        "n_requested_marker_genes": len(marker_table),
        "n_arabidopsis_longest_isoforms": len(arabidopsis_longest),
        "n_wolffia_longest_isoforms": len(wolffia_longest),
        "thresholds": {
            "evalue": args.evalue,
            "minimum_percent_identity": args.min_identity,
            "minimum_query_coverage": args.min_query_coverage,
            "minimum_subject_coverage": args.min_subject_coverage,
        },
        "model_feature_confidence_counts": {str(key): int(value) for key, value in model_counts.items()},
        "source_urls": {
            "arabidopsis": "https://www.ncbi.nlm.nih.gov/datasets/genome/GCF_000001735.4/",
            "wolffia": "https://www.ncbi.nlm.nih.gov/datasets/genome/GCF_029677425.1/",
        },
        "interpretation_warning": (
            "Reciprocal protein similarity is evidence for putative orthology, not proof of conserved expression, "
            "function, or one-to-one evolutionary history. One-to-many families require manual review."
        ),
    }
    with open(args.output_dir / "orthology_summary.json", "w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2)

    print(coverage.to_string(index=False))
    print("Model feature confidence counts:", model_counts)
    print(f"Wrote model mapping to {args.model_mapping}")
    print(f"Wrote marker mapping to {args.marker_mapping}")
    print(f"Wrote transfer feature set to {args.transfer_features}")


if __name__ == "__main__":
    main()
