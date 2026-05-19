#!/usr/bin/env python3
"""
Command-line article import.

The web app uses the same backend service, so both paths write to:
data/materials/<material_id>/
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from backend.import_service import import_article_upload  # noqa: E402
from backend.paths import ensure_project_dirs  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(description="Import a Markdown or text article.")
    parser.add_argument("article", help="Path to a .md or .txt article")
    parser.add_argument("--title", help="Optional title for the material", default="")
    args = parser.parse_args()

    ensure_project_dirs()
    input_path = Path(args.article).expanduser().resolve()
    if not input_path.exists():
        raise SystemExit(f"Article not found: {input_path}")

    material = import_article_upload(input_path.name, input_path.read_bytes(), args.title)
    print(f"Imported article: {material['title']}")
    print(f"Material page: http://127.0.0.1:8765/materials/{material['id']}")
    print(f"Local folder: data/materials/{material['id']}")


if __name__ == "__main__":
    main()

