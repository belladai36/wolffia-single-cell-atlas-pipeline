#!/usr/bin/env python3
"""Create a structured review table for trusted Wolffia-native markers.

This does not replace biological/manual review. It creates a clean first-pass
review sheet so each marker can be inspected, kept, revised, or removed.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


DEFAULT_INPUT = Path("data/metadata/wolffia_trusted_native_marker_panel.csv")
DEFAULT_OUTPUT = Path("data/metadata/wolffia_trusted_native_marker_panel_review.csv")


def review_call(row: pd.Series) -> str:
    """Assign a first-pass review call from marker tier and annotation."""
    tier = row["trusted_panel_tier"]
    text = f"{row.get('preferred_name', '')} {row.get('annotation_summary', '')}".lower()

    if tier == "watchlist_unknown":
        return "unknown_watchlist"
    if "unknown function" in text or "duf" in text:
        return "unknown_watchlist"
    if tier == "core_marker":
        return "keep_initial"
    if tier == "supporting_marker":
        return "supporting_review"
    return "needs_review"


def priority(row: pd.Series) -> str:
    """Prioritize rows for human review."""
    call = row["initial_review_call"]
    if call == "keep_initial" and row["best_marker_rank"] <= 3:
        return "high"
    if call in {"keep_initial", "supporting_review"}:
        return "medium"
    return "watchlist"


def review_note(row: pd.Series) -> str:
    """Explain why the row received its first-pass review call."""
    call = row["initial_review_call"]
    if call == "keep_initial":
        return "Strong ranked marker with interpretable annotation; keep for first-pass scoring unless manual review finds a problem."
    if call == "supporting_review":
        return "Useful supporting marker, but should be checked manually before being treated as a core program marker."
    if call == "unknown_watchlist":
        return "Strong marker with unclear/unknown annotation; keep visible as a Wolffia-specific watchlist gene."
    return "Needs manual review before use."


def build_review_table(panel: pd.DataFrame) -> pd.DataFrame:
    """Add review columns to the trusted panel."""
    review = panel.copy()
    review["initial_review_call"] = review.apply(review_call, axis=1)
    review["manual_review_priority"] = review.apply(priority, axis=1)
    review["review_note"] = review.apply(review_note, axis=1)
    review["manual_decision"] = ""
    review["manual_decision_notes"] = ""

    columns = [
        "native_program_id",
        "native_program_name",
        "trusted_panel_tier",
        "initial_review_call",
        "manual_review_priority",
        "waus8730_gene_id",
        "preferred_name",
        "source_leiden_clusters",
        "best_marker_rank",
        "max_marker_score",
        "evidence_level",
        "annotation_summary",
        "reason_for_inclusion",
        "review_note",
        "manual_decision",
        "manual_decision_notes",
    ]
    return review[columns].sort_values(
        [
            "native_program_name",
            "manual_review_priority",
            "initial_review_call",
            "best_marker_rank",
            "max_marker_score",
        ],
        ascending=[True, True, True, True, False],
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Create a first-pass review table for trusted Wolffia-native markers."
    )
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    panel = pd.read_csv(args.input)
    review = build_review_table(panel)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    review.to_csv(args.output, index=False)

    print(f"Wrote: {args.output}")
    print(f"Rows: {len(review)}")
    print("Initial review calls:")
    print(review["initial_review_call"].value_counts().sort_index().to_string())
    print("Review priorities:")
    print(review["manual_review_priority"].value_counts().sort_index().to_string())


if __name__ == "__main__":
    main()
