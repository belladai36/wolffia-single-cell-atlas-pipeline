#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import ListFlowable, ListItem, Paragraph, SimpleDocTemplate, Spacer


PROJECT_ROOT = Path(__file__).resolve().parent.parent
INPUT_PATH = PROJECT_ROOT / "docs" / "wolffia_data_generation_protocol_detailed.md"
OUTPUT_PATH = PROJECT_ROOT / "output" / "pdf" / "wolffia_data_generation_protocol_detailed.pdf"


def build_styles():
    styles = getSampleStyleSheet()
    styles.add(
        ParagraphStyle(
            name="TitlePlain",
            parent=styles["Title"],
            fontName="Helvetica-Bold",
            fontSize=18,
            leading=22,
            spaceAfter=10,
            textColor=colors.black,
        )
    )
    styles.add(
        ParagraphStyle(
            name="H1Plain",
            parent=styles["Heading1"],
            fontName="Helvetica-Bold",
            fontSize=13,
            leading=16,
            spaceBefore=10,
            spaceAfter=5,
            textColor=colors.black,
        )
    )
    styles.add(
        ParagraphStyle(
            name="H2Plain",
            parent=styles["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=11,
            leading=14,
            spaceBefore=8,
            spaceAfter=4,
            textColor=colors.black,
        )
    )
    styles.add(
        ParagraphStyle(
            name="BodyPlain",
            parent=styles["BodyText"],
            fontName="Helvetica",
            fontSize=10,
            leading=13,
            spaceAfter=4,
            alignment=TA_LEFT,
            textColor=colors.black,
        )
    )
    styles.add(
        ParagraphStyle(
            name="QuotePlain",
            parent=styles["BodyText"],
            fontName="Helvetica-Oblique",
            fontSize=10,
            leading=13,
            leftIndent=18,
            textColor=colors.black,
            spaceAfter=5,
        )
    )
    return styles


def clean_inline(text: str) -> str:
    replacements = {"&": "&amp;", "<": "&lt;", ">": "&gt;"}
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text.replace("**", "").replace("`", "")


def bullet_list(items: list[str], styles, ordered: bool = False) -> ListFlowable:
    return ListFlowable(
        [ListItem(Paragraph(clean_inline(item), styles["BodyPlain"]), leftIndent=8) for item in items],
        bulletType="1" if ordered else "bullet",
        start="circle" if not ordered else None,
        bulletFontName="Helvetica",
        bulletFontSize=8,
        leftIndent=18,
    )


def parse_markdown(lines: list[str], styles):
    story = []
    i = 0
    while i < len(lines):
        raw = lines[i].rstrip("\n")
        line = raw.strip()
        if not line:
            i += 1
            continue

        if line.startswith("# "):
            story.append(Paragraph(clean_inline(line[2:]), styles["TitlePlain"]))
            i += 1
            continue
        if line.startswith("## "):
            story.append(Paragraph(clean_inline(line[3:]), styles["H1Plain"]))
            i += 1
            continue
        if line.startswith("### "):
            story.append(Paragraph(clean_inline(line[4:]), styles["H2Plain"]))
            i += 1
            continue
        if line.startswith(">"):
            story.append(Paragraph(clean_inline(line.lstrip("> ").strip()), styles["QuotePlain"]))
            i += 1
            continue
        if line.startswith("- "):
            items = []
            while i < len(lines):
                nxt = lines[i].strip()
                if nxt.startswith("- "):
                    items.append(nxt[2:].strip())
                    i += 1
                else:
                    break
            story.append(bullet_list(items, styles, ordered=False))
            story.append(Spacer(1, 0.04 * inch))
            continue
        if len(line) > 2 and line[0].isdigit() and line[1] == ".":
            items = []
            while i < len(lines):
                nxt = lines[i].strip()
                if len(nxt) > 2 and nxt[0].isdigit() and nxt[1] == ".":
                    items.append(nxt[2:].strip())
                    i += 1
                else:
                    break
            story.append(bullet_list(items, styles, ordered=True))
            story.append(Spacer(1, 0.04 * inch))
            continue

        paragraph_lines = [line]
        i += 1
        while i < len(lines):
            nxt = lines[i].strip()
            if not nxt:
                i += 1
                break
            if nxt.startswith(("# ", "## ", "### ", "- ", ">")):
                break
            if len(nxt) > 2 and nxt[0].isdigit() and nxt[1] == ".":
                break
            paragraph_lines.append(nxt)
            i += 1
        story.append(Paragraph(clean_inline(" ".join(paragraph_lines)), styles["BodyPlain"]))
    return story


def main():
    styles = build_styles()
    lines = INPUT_PATH.read_text(encoding="utf-8").splitlines()
    story = parse_markdown(lines, styles)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(
        str(OUTPUT_PATH),
        pagesize=letter,
        leftMargin=0.8 * inch,
        rightMargin=0.8 * inch,
        topMargin=0.8 * inch,
        bottomMargin=0.75 * inch,
        title="Beginner-Friendly Guide to the Wolffia Data-Generation Protocol",
        author="OpenAI Codex",
    )
    doc.build(story)
    print(f"Wrote {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
