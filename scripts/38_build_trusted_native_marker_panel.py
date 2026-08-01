#!/usr/bin/env python3
"""Build a first-pass trusted Wolffia-native marker panel.

This script converts the broader marker-program candidate table into a smaller,
review-ready panel. The output is still provisional: it is meant to be manually
reviewed before being treated as a final annotation reference.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


DEFAULT_INPUT = Path("data/metadata/wolffia_native_program_marker_candidates.csv")
DEFAULT_OUTPUT = Path("data/metadata/wolffia_trusted_native_marker_panel.csv")


UNKNOWN_PROGRAM_ID = "unknown_high_marker"
MAX_MARKERS_PER_PROGRAM = 8
CORE_RANK_CUTOFF = 5
SUPPORTING_RANK_CUTOFF = 8


def marker_tier(row: pd.Series) -> str:
    """Assign a transparent review tier to one candidate marker row."""
    if row["native_program_id"] == UNKNOWN_PROGRAM_ID:
        return "watchlist_unknown"
    if row["evidence_level"] == "high" and row["best_marker_rank"] <= CORE_RANK_CUTOFF:
        return "core_marker"
    if row["evidence_level"] in {"high", "medium"} and row["best_marker_rank"] <= SUPPORTING_RANK_CUTOFF:
        return "supporting_marker"
    return "exclude_initial_panel"


def inclusion_reason(row: pd.Series) -> str:
    """Human-readable reason for including a marker in the first-pass panel."""
    if row["trusted_panel_tier"] == "core_marker":
        return (
            "High-evidence marker with top-five rank in at least one Wolffia "
            "Leiden cluster and interpretable annotation."
        )
    if row["trusted_panel_tier"] == "supporting_marker":
        return (
            "High- or medium-evidence marker within the top-eight ranks; useful "
            "as supporting evidence for this candidate program."
        )
    if row["trusted_panel_tier"] == "watchlist_unknown":
        return (
            "Strong Wolffia marker with unknown or unclear annotation; keep as "
            "a watchlist feature rather than a final biological marker."
        )
    return "Not included in the initial trusted panel."


def build_panel(candidates: pd.DataFrame) -> pd.DataFrame:
    """Create the first-pass trusted marker panel from candidate markers."""
    required_columns = {
        "native_program_id",
        "native_program_name",
        "waus8730_gene_id",
        "preferred_name",
        "source_leiden_clusters",
        "best_marker_rank",
        "max_marker_score",
        "evidence_level",
        "annotation_summary",
    }
    missing = sorted(required_columns - set(candidates.columns))
    if missing:
        raise ValueError(f"Input marker table is missing required columns: {missing}")

    panel = candidates.copy()
    panel["trusted_panel_tier"] = panel.apply(marker_tier, axis=1)
    panel = panel[panel["trusted_panel_tier"] != "exclude_initial_panel"].copy()

    panel["tier_sort"] = panel["trusted_panel_tier"].map(
        {"core_marker": 0, "supporting_marker": 1, "watchlist_unknown": 2}
    )
    panel = panel.sort_values(
        [
            "native_program_id",
            "tier_sort",
            "best_marker_rank",
            "max_marker_score",
            "waus8730_gene_id",
        ],
        ascending=[True, True, True, False, True],
    )

    # Keep the panel readable. Unknown markers are handled as a watchlist group;
    # all other programs keep at most eight markers in this first pass.
    panel = (
        panel.groupby("native_program_id", group_keys=False, sort=False)
        .head(MAX_MARKERS_PER_PROGRAM)
        .copy()
    )

    panel["reason_for_inclusion"] = panel.apply(inclusion_reason, axis=1)
    panel["manual_review_status"] = "needs_manual_review"

    output_columns = [
        "native_program_id",
        "native_program_name",
        "trusted_panel_tier",
        "waus8730_gene_id",
        "preferred_name",
        "source_leiden_clusters",
        "best_marker_rank",
        "max_marker_score",
        "evidence_level",
        "annotation_summary",
        "reason_for_inclusion",
        "manual_review_status",
    ]
    return panel[output_columns].reset_index(drop=True)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Build a first-pass trusted Wolffia-native marker panel."
    )
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    candidates = pd.read_csv(args.input)
    panel = build_panel(candidates)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    panel.to_csv(args.output, index=False)

    print(f"Wrote: {args.output}")
    print(f"Rows: {len(panel)}")
    print("Rows by program:")
    print(panel["native_program_name"].value_counts().sort_index().to_string())
    print("Rows by tier:")
    print(panel["trusted_panel_tier"].value_counts().sort_index().to_string())


if __name__ == "__main__":
    main()
