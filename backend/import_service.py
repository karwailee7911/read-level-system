from __future__ import annotations

import re
from pathlib import Path

from backend.material_service import create_material
from backend.paths import RAW_ARTICLE_DIR, RAW_PDF_DIR
from backend.utils import decode_bytes, now_iso, safe_name, write_text


def infer_article_title(filename: str, text: str, explicit_title: str = "") -> str:
    if explicit_title.strip():
        return explicit_title.strip()
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("# "):
            return stripped.lstrip("#").strip()
        if stripped:
            return stripped[:40]
    return Path(filename).stem


def normalize_article_markdown(text: str, title: str, source_file: str) -> str:
    body = text.strip()
    if not body.startswith("#"):
        body = f"# {title}\n\n{body}"
    return "\n".join(
        [
            "---",
            f"title: {title}",
            "source_type: article",
            f"source_file: {source_file}",
            f"imported_at: {now_iso()}",
            "---",
            "",
            body,
            "",
        ]
    )


def import_article_upload(filename: str, data: bytes, title: str = "") -> dict:
    if not filename.lower().endswith((".md", ".txt")):
        raise ValueError("公众号文章只支持 .md 或 .txt")

    text = decode_bytes(data)
    doc_title = infer_article_title(filename, text, title)
    raw_name = safe_name(filename)
    raw_path = RAW_ARTICLE_DIR / raw_name
    raw_path.write_bytes(data)

    source_markdown = normalize_article_markdown(text, doc_title, raw_name)
    return create_material(doc_title, "article", raw_name, source_markdown)


def load_pdf_reader():
    try:
        from pypdf import PdfReader  # type: ignore

        return PdfReader
    except ImportError:
        try:
            from PyPDF2 import PdfReader  # type: ignore

            return PdfReader
        except ImportError as exc:
            raise RuntimeError("缺少 PDF 解析依赖，请先安装 pypdf。") from exc


def clean_pdf_text(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def extract_pdf_markdown(pdf_path: Path, title: str, source_file: str) -> str:
    PdfReader = load_pdf_reader()
    reader = PdfReader(str(pdf_path))
    pages = []
    for index, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        pages.append(f"## Page {index}\n\n{clean_pdf_text(text)}")

    return "\n".join(
        [
            "---",
            f"title: {title}",
            "source_type: pdf",
            f"source_file: {source_file}",
            f"imported_at: {now_iso()}",
            "---",
            "",
            f"# {title}",
            "",
            *pages,
            "",
        ]
    )


def import_pdf_upload(filename: str, data: bytes, title: str = "") -> dict:
    if not filename.lower().endswith(".pdf"):
        raise ValueError("PDF 资料只支持 .pdf")

    doc_title = title.strip() or Path(filename).stem
    raw_name = safe_name(filename)
    raw_path = RAW_PDF_DIR / raw_name
    raw_path.write_bytes(data)

    source_markdown = extract_pdf_markdown(raw_path, doc_title, raw_name)
    return create_material(doc_title, "pdf", raw_name, source_markdown)


def import_article_text(title: str, text: str) -> dict:
    doc_title = title.strip() or infer_article_title("pasted_article.md", text)
    raw_name = safe_name(f"{doc_title}.md")
    write_text(RAW_ARTICLE_DIR / raw_name, text)
    source_markdown = normalize_article_markdown(text, doc_title, raw_name)
    return create_material(doc_title, "article", raw_name, source_markdown)

