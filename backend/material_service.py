from __future__ import annotations

import shutil
import re
from pathlib import Path
from typing import Any

from backend.paths import ARTICLE_LIBRARY_DIRS, MATERIALS_DIR
from backend.utils import h, material_id, now_iso, read_json, read_text, today, write_json, write_text


NOTE_TYPES = {
    "reality_insights": "与我现实有关的启发",
    "action_list": "可执行行动清单",
    "content_topics": "内容选题",
    "english_extract": "英语表达积累",
    "concept_cards": "关键概念卡片",
    "mind_map": "思维导图",
}

PRIMARY_NOTE_TYPES = {
    "reality_insights": "启发",
    "action_list": "行动",
    "content_topics": "选题",
    "concept_cards": "概念",
    "mind_map": "导图",
}


def material_dir(mid: str) -> Path:
    return MATERIALS_DIR / mid


def manifest_path(mid: str) -> Path:
    return material_dir(mid) / "manifest.json"


def create_material(
    title: str,
    source_type: str,
    source_file: str,
    source_markdown: str,
    source_hash: str = "",
) -> dict[str, Any]:
    """Create a material folder under data/materials."""
    mid = material_id(title)
    folder = material_dir(mid)
    (folder / "notes").mkdir(parents=True, exist_ok=True)
    (folder / "outputs").mkdir(parents=True, exist_ok=True)
    (folder / "assets").mkdir(parents=True, exist_ok=True)

    manifest = {
        "id": mid,
        "title": title,
        "type": source_type,
        "source_file": source_file,
        "source_hash": source_hash,
        "imported_at": now_iso(),
        "updated_at": now_iso(),
        "source_path": "source.md",
    }
    write_text(folder / "source.md", source_markdown)
    write_json(folder / "manifest.json", manifest)
    return manifest


def list_materials() -> list[dict[str, Any]]:
    """List real imported materials only. Examples are not included."""
    materials = []
    if not MATERIALS_DIR.exists():
        return materials

    for path in MATERIALS_DIR.iterdir():
        if not path.is_dir():
            continue
        manifest = read_json(path / "manifest.json", None)
        if manifest:
            materials.append(manifest)

    return sorted(materials, key=lambda item: item.get("imported_at", ""), reverse=True)


def get_material(mid: str) -> dict[str, Any] | None:
    manifest = read_json(manifest_path(mid), None)
    if not manifest:
        return None
    return manifest


def find_material_by_source_hash(source_hash: str) -> dict[str, Any] | None:
    if not source_hash:
        return None

    if not MATERIALS_DIR.exists():
        return None

    for path in MATERIALS_DIR.iterdir():
        if not path.is_dir():
            continue
        manifest = read_json(path / "manifest.json", None)
        if not manifest:
            continue
        if manifest.get("source_hash") == source_hash:
            return manifest
    return None


def get_source(mid: str) -> str:
    return read_text(material_dir(mid) / "source.md")


def source_is_english(markdown: str) -> bool:
    body = strip_frontmatter(markdown)
    ascii_letters = len(re.findall(r"[A-Za-z]", body))
    chinese_chars = len(re.findall(r"[\u4e00-\u9fff]", body))
    return ascii_letters > 300 and ascii_letters > chinese_chars * 1.5


def material_asset_dir(mid: str) -> Path:
    return material_dir(mid) / "assets"


def resolve_material_folder(mid: str) -> Path:
    target = material_dir(mid).resolve()
    base = MATERIALS_DIR.resolve()
    target.relative_to(base)
    return target


def delete_material(mid: str) -> None:
    folder = resolve_material_folder(mid)
    if not folder.exists() or not folder.is_dir():
        raise FileNotFoundError("资料不存在")
    shutil.rmtree(folder)


def copy_article_assets(mid: str, source_markdown_path: Path) -> None:
    """Copy sibling article image assets when the original folder is available."""
    images_dir = source_markdown_path.parent / "images"
    target_dir = material_asset_dir(mid) / "images"
    if images_dir.exists() and images_dir.is_dir():
        target_dir.mkdir(parents=True, exist_ok=True)
        for item in images_dir.iterdir():
            if item.is_file():
                shutil.copy2(item, target_dir / item.name)


def find_external_asset(mid: str, relative_path: str) -> Path | None:
    """
    Resolve relative assets for imported article markdown.

    Browser uploads only provide the file bytes, so we try to recover sibling
    images from the user's article library using the original file name.
    """
    manifest = get_material(mid)
    if not manifest:
        return None

    local_asset = material_asset_dir(mid) / relative_path
    if local_asset.exists():
        return local_asset

    source_file = str(manifest.get("source_file", "")).strip()
    title = str(manifest.get("title", "")).strip()
    for root in ARTICLE_LIBRARY_DIRS:
        if not root.exists():
            continue
        direct_candidates = [
            root / title / relative_path,
            root / Path(source_file).stem / relative_path,
        ]
        for candidate in direct_candidates:
            if candidate.exists():
                return candidate
        if source_file:
            for markdown_path in root.rglob(source_file):
                candidate = markdown_path.parent / relative_path
                if candidate.exists():
                    return candidate
    return None


def strip_frontmatter(markdown: str) -> str:
    """Hide import metadata from the reading view."""
    text = markdown.strip()
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) == 3:
            return parts[2].strip()
    return markdown.strip()


def markdown_inline(text: str, asset_prefix: str = "") -> str:
    """Render only safe, common inline Markdown patterns."""
    raw_img = re.search(r"<img[^>]+(?:src|data-src)=[\"']([^\"']+)[\"'][^>]*>", text)
    if raw_img and raw_img.group(1).startswith(("http://", "https://")):
        return f'<img src="{h(raw_img.group(1))}" alt="" loading="lazy">'

    bare_img = re.match(r"^(https?://\S+(?:png|jpe?g|gif|webp|svg)(?:\?\S*)?)$", text)
    if bare_img:
        return f'<img src="{h(bare_img.group(1))}" alt="" loading="lazy">'

    wechat_img = re.match(r"^(https?://\S*(?:mmbiz|qpic|qq)\S*)$", text)
    if wechat_img and ("wx_fmt=" in text or "/mmbiz_" in text):
        return f'<img src="{h(wechat_img.group(1))}" alt="" loading="lazy">'

    rel_img = re.match(r"^!\[([^\]]*)\]\(([^)]+)\)$", text)
    if rel_img and not rel_img.group(2).startswith(("http://", "https://")):
        src = f"{asset_prefix}/{rel_img.group(2).lstrip('./')}" if asset_prefix else rel_img.group(2)
        return f'<img src="{h(src)}" alt="{h(rel_img.group(1))}" loading="lazy">'

    escaped = h(text)
    escaped = re.sub(
        r"!\[([^\]]*)\]\((https?://[^)]+)\)",
        r'<img src="\2" alt="\1" loading="lazy">',
        escaped,
    )
    escaped = re.sub(
        r"\[([^\]]+)\]\((https?://[^)]+)\)",
        r'<a href="\2" target="_blank" rel="noreferrer">\1</a>',
        escaped,
    )
    escaped = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", escaped)
    return escaped


def render_source_html(markdown: str, asset_prefix: str = "") -> str:
    """
    Render a readable source view.

    This is deliberately small: enough for article reading, image display, and
    clean line breaks without turning the project into a Markdown engine.
    """
    body = strip_frontmatter(markdown)
    blocks = []
    list_items: list[str] = []

    def flush_list() -> None:
        if list_items:
            blocks.append("<ul>" + "".join(list_items) + "</ul>")
            list_items.clear()

    for raw_line in body.splitlines():
        line = raw_line.strip()
        if not line:
            flush_list()
            continue

        if line in {"---", "***", "___"}:
            flush_list()
            continue
        elif line.startswith("# "):
            flush_list()
            blocks.append(f"<h1>{markdown_inline(line[2:].strip(), asset_prefix)}</h1>")
        elif line.startswith("## "):
            flush_list()
            blocks.append(f"<h2>{markdown_inline(line[3:].strip(), asset_prefix)}</h2>")
        elif line.startswith("### "):
            flush_list()
            blocks.append(f"<h3>{markdown_inline(line[4:].strip(), asset_prefix)}</h3>")
        elif line.startswith(">"):
            flush_list()
            blocks.append(f"<blockquote>{markdown_inline(line.lstrip('>').strip(), asset_prefix)}</blockquote>")
        elif line.startswith(("- ", "* ")):
            list_items.append(f"<li>{markdown_inline(line[2:].strip(), asset_prefix)}</li>")
        elif re.match(r"^!?\[[^\]]*\]\([^)]+\)$", line):
            flush_list()
            blocks.append(f"<p>{markdown_inline(line, asset_prefix)}</p>")
        else:
            flush_list()
            blocks.append(f"<p>{markdown_inline(line, asset_prefix)}</p>")

    flush_list()
    return "\n".join(blocks) or '<p class="empty">暂无原文。</p>'


def get_note(mid: str, note_type: str) -> str:
    if note_type not in NOTE_TYPES:
        return ""
    return read_text(material_dir(mid) / "notes" / f"{note_type}.md")


def save_note(mid: str, note_type: str, content: str) -> None:
    if note_type not in NOTE_TYPES:
        raise ValueError("Unknown note type")
    write_text(material_dir(mid) / "notes" / f"{note_type}.md", content)
    touch_material(mid)


def append_note(mid: str, note_type: str, content: str) -> None:
    if note_type not in NOTE_TYPES:
        raise ValueError("Unknown note type")
    path = material_dir(mid) / "notes" / f"{note_type}.md"
    existing = read_text(path).strip()
    incoming = content.strip()
    if not incoming:
        return
    merged = incoming if not existing else f"{existing}\n\n---\n\n{incoming}"
    write_text(path, merged)
    touch_material(mid)


def get_draft(mid: str) -> str:
    return read_text(material_dir(mid) / "outputs" / "draft.md")


def save_draft(mid: str, content: str) -> None:
    write_text(material_dir(mid) / "outputs" / "draft.md", content)
    touch_material(mid)


def touch_material(mid: str) -> None:
    manifest = get_material(mid)
    if not manifest:
        return
    manifest["updated_at"] = now_iso()
    write_json(manifest_path(mid), manifest)


def primary_note_editors_html(mid: str) -> str:
    """Render only the first three writing fields to keep the page focused."""
    sections = []
    for index, (note_type, label) in enumerate(PRIMARY_NOTE_TYPES.items()):
        content = h(get_note(mid, note_type))
        hidden = "" if index == 0 else " hidden"
        active = " active" if index == 0 else ""
        sections.append(
            f"""
            <section class="editor-card{active}" data-write-panel="{h(note_type)}"{hidden}>
              <form method="post" action="/api/materials/{h(mid)}/notes/{h(note_type)}">
                <textarea name="content" rows="12" placeholder="直接写，不用填满。">{content}</textarea>
                <button type="submit">保存</button>
              </form>
            </section>
            """
        )
    return "\n".join(sections)


def classify_note_type(content: str, english_allowed: bool) -> tuple[str, str]:
    text = content.strip()
    lower = text.lower()

    if english_allowed:
        english_ratio = len(re.findall(r"[A-Za-z]", text)) / max(len(text), 1)
        if english_ratio > 0.45 or any(word in lower for word in ["expression", "phrase", "vocabulary", "rewrite", "english"]):
            return "english_extract", "英语表达积累"

    if re.search(r"(^|\n)\s*[-*]\s|\btodo\b|行动|截止|完成证据|清单|下一步|本周可做", text, re.I):
        return "action_list", "可执行行动清单"
    if re.search(r"选题|标题|读者|角度|可写观点|推荐形式", text):
        return "content_topics", "内容选题"
    if re.search(r"概念|一句话解释|它解决的问题|容易被误解|现实例子", text):
        return "concept_cards", "关键概念卡片"
    if re.search(r"(^|\n)\s*[-*]\s.*\n\s{2,}[-*]\s|思维导图|核心问题|关键概念|可执行行动", text):
        return "mind_map", "思维导图"
    return "reality_insights", "与我现实有关的启发"


def unified_capture_preview_html(mid: str, english_allowed: bool) -> str:
    note_order = [
        "reality_insights",
        "action_list",
        "content_topics",
        "concept_cards",
        "mind_map",
    ]
    if english_allowed:
        note_order.append("english_extract")

    items = []
    for note_type in note_order:
        label = NOTE_TYPES[note_type]
        content = get_note(mid, note_type).strip()
        if not content:
            continue
        preview = h(content[:140] + ("..." if len(content) > 140 else ""))
        items.append(
            f"""
            <details class="saved-item">
              <summary>{h(label)}</summary>
              <pre>{preview}</pre>
            </details>
            """
        )
    return "\n".join(items) if items else '<p class="empty">还没有保存内容。</p>'


def materials_list_html(materials: list[dict[str, Any]]) -> str:
    if not materials:
        return '<p class="empty">还没有导入资料。</p>'

    items = []
    for item in materials:
        mid = item.get("id", "")
        items.append(
            f"""
            <article class="list-item">
              <div>
                <strong>{h(item.get("title", "未命名资料"))}</strong>
                <span>{h(item.get("type", ""))} · {h(item.get("imported_at", ""))}</span>
              </div>
              <div class="list-actions">
                <a class="button" href="/materials/{h(mid)}">打开处理页</a>
                <form method="post" action="/api/materials/{h(mid)}/delete" onsubmit="return confirm('确定删除这份资料？此操作不可恢复。');">
                  <button type="submit">删除</button>
                </form>
              </div>
            </article>
            """
        )
    return "\n".join(items)


def recent_materials_html(materials: list[dict[str, Any]]) -> str:
    if not materials:
        return '<p class="empty">暂无。导入第一份资料后，这里才会出现记录。</p>'

    items = []
    for item in materials[:5]:
        mid = item.get("id", "")
        items.append(
            f"""
            <li>
              <a href="/materials/{h(mid)}">{h(item.get("title", "未命名资料"))}</a>
              <span>{h(item.get("type", ""))} · {h(item.get("imported_at", ""))}</span>
            </li>
            """
        )
    return f'<ul class="simple-list">{ "".join(items) }</ul>'


def material_has_user_evidence(mid: str) -> bool:
    folder = material_dir(mid)
    note_files = list((folder / "notes").glob("*.md")) if (folder / "notes").exists() else []
    output_files = list((folder / "outputs").glob("*.md")) if (folder / "outputs").exists() else []
    for path in note_files + output_files:
        if read_text(path).strip():
            return True
    return False
