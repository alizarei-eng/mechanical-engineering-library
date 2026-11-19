#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Extract embedded PDF text and detectable tables into a UTF-8 TXT file.

Install: python -m pip install -r requirements.txt
Example: python pdf_to_txt.py input.pdf -o output.txt --pages 10-25
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import fitz
import pdfplumber


def parse_page_range(value: str, total_pages: int) -> list[int]:
    """Parse 1-based page selection, e.g. '1-5,8,12-14'."""
    selected: set[int] = set()
    for part in value.split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            pieces = part.split("-", maxsplit=1)
            start, end = (int(piece.strip()) for piece in pieces)
        else:
            start = end = int(part)
        if start < 1 or end < start or end > total_pages:
            raise ValueError(
                f"Invalid page range '{part}'. Valid pages: 1-{total_pages}"
            )
        selected.update(range(start, end + 1))
    if not selected:
        raise ValueError("No pages selected.")
    return sorted(selected)


def clean_text(value: str | None) -> str:
    """Normalize line endings while preserving paragraph separation."""
    if not value:
        return ""
    value = value.replace("\r\n", "\n").replace("\r", "\n")
    lines = [line.rstrip() for line in value.split("\n")]
    result: list[str] = []
    blank_count = 0
    for line in lines:
        if line.strip():
            result.append(line.strip())
            blank_count = 0
        else:
            blank_count += 1
            if blank_count == 1:
                result.append("")
    return "\n".join(result).strip()


def normalize_cell(cell: object) -> str:
    if cell is None:
        return ""
    return " ".join(str(cell).replace("\r", "\n").split())


def format_table(table: list[list[object]]) -> str:
    lines = []
    for row in table:
        if row is None:
            continue
        cells = [normalize_cell(cell) for cell in row]
        if any(cells):
            lines.append(" | ".join(cells))
    return "\n".join(lines)


def extract_page_tables(page: pdfplumber.page.Page) -> list[list[list[object]]]:
    """Try ruled-table detection, then a text-alignment fallback."""
    strategies = [
        {
            "vertical_strategy": "lines",
            "horizontal_strategy": "lines",
            "intersection_tolerance": 5,
            "snap_tolerance": 3,
            "join_tolerance": 3,
            "edge_min_length": 3,
        },
        {
            "vertical_strategy": "text",
            "horizontal_strategy": "text",
            "min_words_vertical": 2,
            "min_words_horizontal": 1,
            "intersection_tolerance": 5,
        },
    ]
    for settings in strategies:
        try:
            tables = page.extract_tables(table_settings=settings) or []
            useful = [
                table for table in tables
                if table and any(
                    any(normalize_cell(cell) for cell in row)
                    for row in table if row
                )
            ]
            if useful:
                return useful
        except Exception:
            continue
    return []


def extract_pdf(
    pdf_path: Path,
    output_path: Path,
    pages_argument: str | None = None,
) -> tuple[int, int, int]:
    if not pdf_path.is_file():
        raise FileNotFoundError(f"Input PDF not found: {pdf_path}")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    text_pages = 0
    table_count = 0

    with fitz.open(pdf_path) as document, pdfplumber.open(pdf_path) as pdf:
        total_pages = len(document)
        selected = (
            parse_page_range(pages_argument, total_pages)
            if pages_argument else list(range(1, total_pages + 1))
        )

        with output_path.open("w", encoding="utf-8-sig", newline="\n") as out:
            out.write("PDF TEXT AND TABLE EXTRACTION\n")
            out.write("=" * 78 + "\n")
            out.write(f"Source file: {pdf_path.name}\n")
            out.write(f"Total PDF pages: {total_pages}\n")
            out.write(f"Processed pages: {len(selected)}\n")
            out.write(
                "Note: automatically detected tables must be checked "
                "against the original PDF.\n\n"
            )

            for page_number in selected:
                print(
                    f"Processing page {page_number}/{total_pages}...",
                    file=sys.stderr,
                )
                text = clean_text(
                    document[page_number - 1].get_text("text", sort=True)
                )
                if text:
                    text_pages += 1

                tables = extract_page_tables(pdf.pages[page_number - 1])
                table_count += len(tables)

                out.write("\n" + "=" * 78 + "\n")
                out.write(f"PAGE {page_number}\n")
                out.write("=" * 78 + "\n\n")
                out.write("[PAGE TEXT]\n" + "-" * 40 + "\n")
                out.write(
                    text + "\n" if text
                    else "[No embedded text detected; this page may be scanned.]\n"
                )

                out.write("\n[TABLES]\n" + "-" * 40 + "\n")
                if tables:
                    for index, table in enumerate(tables, start=1):
                        out.write(f"\nTABLE {index}\n")
                        out.write(format_table(table) + "\n")
                else:
                    out.write("[No table detected automatically.]\n")
                out.write("\n")

            out.write("\n" + "=" * 78 + "\nEXTRACTION SUMMARY\n")
            out.write("=" * 78 + "\n")
            out.write(f"Pages processed: {len(selected)}\n")
            out.write(f"Pages with embedded text: {text_pages}\n")
            out.write(f"Pages without embedded text: {len(selected) - text_pages}\n")
            out.write(f"Tables detected: {table_count}\n")
            out.write(
                "Pages without embedded text may require OCR. "
                "Merged or borderless tables may be detected incorrectly.\n"
            )

    return len(selected), text_pages, table_count


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Extract PDF text and detectable tables to UTF-8 TXT."
    )
    parser.add_argument("pdf", type=Path, help="Input PDF path")
    parser.add_argument(
        "-o", "--output", type=Path,
        default=Path("extracted_output.txt"),
        help="Output TXT path (default: extracted_output.txt)",
    )
    parser.add_argument(
        "--pages",
        help="Optional 1-based page selection, e.g. 1-10,15,20-25",
    )
    args = parser.parse_args()

    try:
        processed, text_pages, tables = extract_pdf(
            args.pdf, args.output, args.pages
        )
    except (FileNotFoundError, ValueError, fitz.FileDataError) as error:
        parser.error(str(error))
    except Exception as error:
        print(f"Extraction failed: {error}", file=sys.stderr)
        return 1

    print("\nExtraction completed.")
    print(f"Pages processed: {processed}")
    print(f"Pages with embedded text: {text_pages}")
    print(f"Tables detected: {tables}")
    print(f"Output: {args.output.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
