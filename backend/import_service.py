from __future__ import annotations

import re
import hashlib
from pathlib import Path

from backend.material_service import copy_article_assets, create_material, find_material_by_source_hash
from backend.paths import RAW_ARTICLE_DIR, RAW_PDF_DIR
from backend.utils import decode_bytes, now_iso, safe_name, write_text


PDF_DEPENDENCY_MESSAGE = "缺少 PDF 解析依赖，请先运行：pip install -r requirements.txt"
PDF_PARSE_FAILED_MESSAGE = "PDF 解析失败。请确认文件不是损坏、加密或扫描版 PDF。"
PDF_UNSUPPORTED_MESSAGE = "当前 PDF 可能是扫描版、图片型或加密 PDF，第一版暂不支持 OCR。"


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


def calculate_source_hash(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_bytes(data: bytes) -> str:
    return calculate_source_hash(data)


def sha256_text(text: str) -> str:
    return calculate_source_hash(text.encode("utf-8"))


def import_article_upload(
    filename: str,
    data: bytes,
    title: str = "",
    source_path: Path | None = None,
) -> dict:
    if not filename.lower().endswith((".md", ".txt")):
        raise ValueError("公众号文章只支持 .md 或 .txt")

    source_hash = calculate_source_hash(data)
    existing = find_material_by_source_hash(source_hash)
    if existing:
        duplicated = dict(existing)
        duplicated["duplicated"] = True
        return duplicated

    text = decode_bytes(data)
    doc_title = infer_article_title(filename, text, title)
    raw_name = safe_name(filename)
    raw_path = RAW_ARTICLE_DIR / raw_name
    raw_path.write_bytes(data)

    source_markdown = normalize_article_markdown(text, doc_title, raw_name)
    material = create_material(doc_title, "article", raw_name, source_markdown, source_hash)
    if source_path is not None:
        copy_article_assets(material["id"], source_path)
    return material


def load_pdf_reader():
    try:
        from pypdf import PdfReader  # type: ignore

        return PdfReader
    except ImportError as exc:
        raise RuntimeError(PDF_DEPENDENCY_MESSAGE) from exc


def pdf_import_available() -> bool:
    try:
        load_pdf_reader()
        return True
    except RuntimeError:
        return False


def clean_pdf_text(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def extract_pdf_markdown(pdf_path: Path, title: str, source_file: str) -> str:
    PdfReader = load_pdf_reader()
    try:
        reader = PdfReader(str(pdf_path))
        if getattr(reader, "is_encrypted", False):
            raise RuntimeError(PDF_UNSUPPORTED_MESSAGE)

        pages = []
        extracted_texts = []
        for index, page in enumerate(reader.pages, start=1):
            text = clean_pdf_text(page.extract_text() or "")
            extracted_texts.append(text)
            pages.append(f"## Page {index}\n\n{text}")
    except RuntimeError:
        raise
    except Exception as exc:
        raise RuntimeError(PDF_PARSE_FAILED_MESSAGE) from exc

    if not any(text.strip() for text in extracted_texts):
        raise RuntimeError(PDF_UNSUPPORTED_MESSAGE)

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

    source_hash = calculate_source_hash(data)
    existing = find_material_by_source_hash(source_hash)
    if existing:
        duplicated = dict(existing)
        duplicated["duplicated"] = True
        return duplicated

    doc_title = title.strip() or Path(filename).stem
    raw_name = safe_name(filename)
    raw_path = RAW_PDF_DIR / raw_name
    raw_path.write_bytes(data)

    source_markdown = extract_pdf_markdown(raw_path, doc_title, raw_name)
    return create_material(doc_title, "pdf", raw_name, source_markdown, source_hash)


def import_article_text(title: str, text: str) -> dict:
    source_hash = calculate_source_hash(text.strip().encode("utf-8"))
    existing = find_material_by_source_hash(source_hash)
    if existing:
        duplicated = dict(existing)
        duplicated["duplicated"] = True
        return duplicated

    doc_title = title.strip() or infer_article_title("pasted_article.md", text)
    raw_name = safe_name(f"{doc_title}.md")
    write_text(RAW_ARTICLE_DIR / raw_name, text)
    source_markdown = normalize_article_markdown(text, doc_title, raw_name)
    return create_material(doc_title, "article", raw_name, source_markdown, source_hash)
