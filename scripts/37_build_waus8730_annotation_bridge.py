#!/usr/bin/env python3
"""Build a Waus8730 annotation bridge for Wolffia model application.

This script uses two externally provided annotation tables:

1. an OrthoFinder-style orthogroup table containing Arabidopsis and
   Waus8730 proteins
2. an eggNOG-mapper table containing functional annotations for Waus8730
   proteins/transcripts

It produces a compact bridge from Arabidopsis model genes to Waus8730 gene IDs.
The bridge is intended to help apply the existing Arabidopsis-trained,
ortholog-aware transfer model to future Waus8730 single-cell count matrices.

Raw externally shared tables are not committed to the repository by default.
Keep them in local, external, or cluster storage and run this script to create
derived bridge tables when needed.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_TRANSFER_FEATURES = PROJECT_ROOT / "data" / "metadata" / "wolffia_transfer_feature_set.csv"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build an Arabidopsis-to-Waus8730 orthogroup and annotation bridge."
    )
    parser.add_argument(
        "--orthogroups",
        required=True,
        type=Path,
        help="Path to OrthoFinder-style Orthogroups.csv.",
    )
    parser.add_argument(
        "--waemap",
        required=True,
        type=Path,
        help="Path to Waus8730 eggNOG-mapper annotation CSV.",
    )
    parser.add_argument(
        "--transfer-features",
        default=DEFAULT_TRANSFER_FEATURES,
        type=Path,
        help=(
            "Optional current 340-feature transfer table. When present, the bridge is "
            "restricted to Arabidopsis genes used by the current model."
        ),
    )
    parser.add_argument(
        "--output-dir",
        default=PROJECT_ROOT / "data" / "metadata" / "waus8730_bridge",
        type=Path,
        help="Directory for derived bridge outputs.",
    )
    parser.add_argument(
        "--max-pairs-per-orthogroup",
        default=5000,
        type=int,
        help="Safety cap for one orthogroup's Arabidopsis x Waus8730 pair expansion.",
    )
    return parser.parse_args()


def strip_arabidopsis_isoform(value: str) -> str:
    """Convert AT1G01010.1-like IDs to AT1G01010."""
    match = re.search(r"(AT[1-5CM]G\d{5})(?:\.\d+)?", value.upper())
    return match.group(1) if match else ""


def strip_waus8730_transcript(value: str) -> str:
    """Convert Waus8730 transcript IDs to gene-level IDs."""
    value = value.strip()
    if not value:
        return ""
    return re.sub(r"\.t\d+$", "", value)


def split_cell_entries(value: object) -> list[str]:
    if pd.isna(value):
        return []
    text = str(value).strip()
    if not text or text == "-":
        return []
    return [entry.strip() for entry in text.split(",") if entry.strip()]


def load_orthogroups(path: Path) -> pd.DataFrame:
    raw = pd.read_csv(path, dtype=str).fillna("")

    # Some spreadsheet exports preserve generic Column1/Column2 headers and store
    # the real headers in the first row. Normalize that common export shape.
    if raw.shape[0] and raw.iloc[0, 0] == "Orthogroup":
        raw.columns = raw.iloc[0].tolist()
        raw = raw.iloc[1:].reset_index(drop=True)

    required = {"Orthogroup", "Ath_protein", "Wa8730_protein"}
    missing = required.difference(raw.columns)
    if missing:
        raise ValueError(f"Orthogroup table is missing required columns: {sorted(missing)}")

    return raw


def load_transfer_genes(path: Path) -> set[str]:
    if not path.exists():
        return set()
    transfer = pd.read_csv(path, dtype=str)
    if "arabidopsis_gene_id" not in transfer.columns:
        raise ValueError(f"{path} must contain an arabidopsis_gene_id column")
    return set(transfer["arabidopsis_gene_id"].dropna().str.upper())


def classify_mapping(n_ath: int, n_waus: int) -> str:
    if n_ath == 1 and n_waus == 1:
        return "one_to_one_orthogroup"
    if n_ath == 1 and n_waus > 1:
        return "one_arabidopsis_to_many_waus8730"
    if n_ath > 1 and n_waus == 1:
        return "many_arabidopsis_to_one_waus8730"
    return "many_to_many_orthogroup"


def build_bridge(
    orthogroups: pd.DataFrame,
    transfer_genes: set[str],
    max_pairs_per_orthogroup: int,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    rows: list[dict[str, object]] = []
    skipped: list[dict[str, object]] = []

    for _, row in orthogroups.iterrows():
        orthogroup = row["Orthogroup"]
        ath_entries = split_cell_entries(row["Ath_protein"])
        wa_entries = split_cell_entries(row["Wa8730_protein"])

        ath_genes = sorted({strip_arabidopsis_isoform(entry) for entry in ath_entries} - {""})
        wa_transcripts = sorted(set(wa_entries))
        wa_genes = sorted({strip_waus8730_transcript(entry) for entry in wa_transcripts} - {""})

        if transfer_genes:
            ath_genes = [gene for gene in ath_genes if gene in transfer_genes]
            if not ath_genes:
                continue

        n_pairs = len(ath_genes) * len(wa_genes)
        if n_pairs > max_pairs_per_orthogroup:
            skipped.append(
                {
                    "orthogroup": orthogroup,
                    "n_arabidopsis_genes": len(ath_genes),
                    "n_waus8730_genes": len(wa_genes),
                    "n_candidate_pairs": n_pairs,
                    "reason": "exceeds_max_pairs_per_orthogroup",
                }
            )
            continue

        relation_type = classify_mapping(len(ath_genes), len(wa_genes))
        for ath_gene in ath_genes:
            for wa_gene in wa_genes:
                rows.append(
                    {
                        "orthogroup": orthogroup,
                        "arabidopsis_gene_id": ath_gene,
                        "waus8730_gene_id": wa_gene,
                        "n_arabidopsis_genes_in_orthogroup": len(ath_genes),
                        "n_waus8730_genes_in_orthogroup": len(wa_genes),
                        "orthogroup_relation_type": relation_type,
                    }
                )

    bridge = pd.DataFrame(rows)
    skipped_df = pd.DataFrame(skipped)

    if not bridge.empty:
        bridge = bridge.sort_values(
            ["arabidopsis_gene_id", "orthogroup", "waus8730_gene_id"]
        ).reset_index(drop=True)

    return bridge, skipped_df


def normalize_waemap(path: Path) -> pd.DataFrame:
    waemap = pd.read_csv(path, dtype=str).fillna("")
    if "#query" not in waemap.columns:
        raise ValueError("waemap table must contain a #query column")

    waemap = waemap.rename(columns={"#query": "waus8730_transcript_id"})
    waemap["waus8730_gene_id"] = waemap["waus8730_transcript_id"].map(strip_waus8730_transcript)

    preferred_columns = [
        "waus8730_gene_id",
        "waus8730_transcript_id",
        "seed_ortholog",
        "evalue",
        "score",
        "Description",
        "Preferred_name",
        "GOs",
        "EC",
        "KEGG_ko",
        "KEGG_Pathway",
        "KEGG_Module",
        "BRITE",
        "PFAMs",
    ]
    present = [col for col in preferred_columns if col in waemap.columns]
    extra = [col for col in waemap.columns if col not in present]
    return waemap[present + extra].sort_values(["waus8730_gene_id", "waus8730_transcript_id"])


def write_summary(
    output_dir: Path,
    bridge: pd.DataFrame,
    skipped: pd.DataFrame,
    transfer_genes: set[str],
    annotated_bridge: pd.DataFrame,
) -> None:
    if bridge.empty:
        relation_counts: dict[str, int] = {}
        mapped_transfer_genes = 0
        mapped_waus_genes = 0
        annotated_waus_genes = 0
    else:
        relation_counts = (
            bridge["orthogroup_relation_type"].value_counts().sort_index().astype(int).to_dict()
        )
        mapped_transfer_genes = int(bridge["arabidopsis_gene_id"].nunique())
        mapped_waus_genes = int(bridge["waus8730_gene_id"].nunique())
        annotated_waus_genes = int(
            annotated_bridge.loc[
                annotated_bridge.get("Description", pd.Series("", index=annotated_bridge.index)).ne(""),
                "waus8730_gene_id",
            ].nunique()
        )

    summary = {
        "transfer_feature_filter_used": bool(transfer_genes),
        "n_transfer_genes_input": len(transfer_genes),
        "n_transfer_genes_mapped_to_waus8730_orthogroups": mapped_transfer_genes,
        "n_waus8730_genes_in_bridge": mapped_waus_genes,
        "n_waus8730_genes_with_description_in_bridge": annotated_waus_genes,
        "n_bridge_rows": int(len(bridge)),
        "n_skipped_orthogroups": int(len(skipped)),
        "orthogroup_relation_counts": relation_counts,
    }
    (output_dir / "waus8730_bridge_summary.json").write_text(json.dumps(summary, indent=2))


def main() -> None:
    args = parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    orthogroups = load_orthogroups(args.orthogroups)
    transfer_genes = load_transfer_genes(args.transfer_features)

    bridge, skipped = build_bridge(
        orthogroups,
        transfer_genes=transfer_genes,
        max_pairs_per_orthogroup=args.max_pairs_per_orthogroup,
    )
    waemap = normalize_waemap(args.waemap)

    annotated_bridge = bridge.merge(waemap, on="waus8730_gene_id", how="left")

    bridge.to_csv(args.output_dir / "waus8730_arabidopsis_orthogroup_bridge.csv", index=False)
    waemap.to_csv(args.output_dir / "waus8730_functional_annotation.csv", index=False)
    annotated_bridge.to_csv(
        args.output_dir / "waus8730_model_feature_annotation_bridge.csv", index=False
    )
    skipped.to_csv(args.output_dir / "waus8730_skipped_large_orthogroups.csv", index=False)
    write_summary(args.output_dir, bridge, skipped, transfer_genes, annotated_bridge)

    print(f"Wrote bridge outputs to {args.output_dir}")
    print(f"Mapped Arabidopsis transfer genes: {bridge['arabidopsis_gene_id'].nunique() if not bridge.empty else 0}")
    print(f"Waus8730 genes in bridge: {bridge['waus8730_gene_id'].nunique() if not bridge.empty else 0}")


if __name__ == "__main__":
    main()

