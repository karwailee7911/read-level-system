#!/usr/bin/env python3
"""
Command-line PDF import.

The web app uses the same backend service, so both paths write to:
data/materials/<material_id>/
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from backend.import_service import import_pdf_upload  # noqa: E402
from backend.paths import ensure_project_dirs  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract a PDF into Markdown.")
    parser.add_argument("pdf", help="Path to the PDF file")
    parser.add_argument("--title", help="Optional title for the material", default="")
    args = parser.parse_args()

    ensure_project_dirs()
    input_path = Path(args.pdf).expanduser().resolve()
    if not input_path.exists():
        raise SystemExit(f"PDF not found: {input_path}")

    material = import_pdf_upload(input_path.name, input_path.read_bytes(), args.title)
    print(f"Imported PDF: {material['title']}")
    print(f"Material page: http://127.0.0.1:8765/materials/{material['id']}")
    print(f"Local folder: data/materials/{material['id']}")


if __name__ == "__main__":
    main()

