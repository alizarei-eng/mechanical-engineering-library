# PDF Text and Table Extractor

A Python utility for extracting embedded text and automatically detectable tables from PDF files into a UTF-8 text file. It is intended for Persian technical documents, regulations, standards, and engineering references.

## Requirements

- Python 3.10+
- PyMuPDF
- pdfplumber

Install dependencies:

    python -m pip install -r requirements.txt

## Usage

Extract all pages:

    python pdf_to_txt.py "input.pdf" -o "output.txt"

Extract a page range (page numbers are 1-based):

    python pdf_to_txt.py "input.pdf" -o "chapter-5.txt" --pages 105-145

Select multiple ranges/pages:

    python pdf_to_txt.py "input.pdf" -o "selected-pages.txt" --pages 1-5,12,20-24

## Output

For each page, the TXT file contains:
- [PAGE TEXT]: text extracted by PyMuPDF.
- [TABLES]: tables detected by pdfplumber, with cells separated by |.
- A final summary showing processed pages, pages with embedded text, and table count.

The output is UTF-8 with BOM (utf-8-sig), which is convenient for common Windows text editors.

## Limitations and quality control

1. Scanned PDFs: this version does not run OCR. Pages with no embedded text are flagged. OCR with a Persian language model such as Tesseract fas must be added/run separately.
2. Table accuracy: detection is heuristic. Merged cells, borderless tables, multi-line cells, and complex engineering tables may be extracted incorrectly or missed.
3. Persian direction: the script does not reverse Persian strings or apply visual RTL transformations, to avoid corrupting character order. Review with an RTL-capable editor.
4. Reading order: geometric sorting improves extraction but cannot guarantee correct reading order in every multi-column PDF.
5. Verify all extracted numerical/regulatory table values against the original PDF before using them in engineering calculations.

## Recommended workflow

1. Extract the full PDF or the required page range.
2. Review pages flagged as having no embedded text; these may need OCR.
3. Compare every extracted table with its source page.
4. Convert only verified content into structured JSON/CSV with edition, clause, table, and page metadata.
