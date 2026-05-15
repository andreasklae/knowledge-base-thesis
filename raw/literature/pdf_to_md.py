#!/usr/bin/env python3
"""Convert a PDF to Markdown using docling.

Usage: .docling-venv/bin/python pdf_to_md.py <input.pdf> <output.md>

Setup (one-time):
    python3 -m venv .docling-venv
    .docling-venv/bin/pip install docling

The venv is required because docling pulls in transformers/sklearn versions
that conflict with the system Anaconda install. First run downloads ~500MB
of model weights into ~/.cache/docling; subsequent runs are fast.
"""
import sys
from pathlib import Path
from docling.document_converter import DocumentConverter


def main():
    if len(sys.argv) != 3:
        print("Usage: python3 pdf_to_md.py <input.pdf> <output.md>", file=sys.stderr)
        sys.exit(1)

    src = Path(sys.argv[1])
    dst = Path(sys.argv[2])

    if not src.exists():
        print(f"Input not found: {src}", file=sys.stderr)
        sys.exit(1)

    converter = DocumentConverter()
    result = converter.convert(str(src))
    md = result.document.export_to_markdown()
    dst.write_text(md, encoding="utf-8")
    print(f"Wrote {dst} ({len(md):,} chars)")


if __name__ == "__main__":
    main()
