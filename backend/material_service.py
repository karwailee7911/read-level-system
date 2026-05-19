from __future__ import annotations

from pathlib import Path
from typing import Any

from backend.paths import MATERIALS_DIR
from backend.utils import h, material_id, now_iso, read_json, read_text, today, write_json, write_text


NOTE_TYPES = {
    "reality_insights": "与我现实有关的启发",
    "action_list": "可执行行动清单",
    "content_topics": "内容选题",
    "english_extract": "英语表达积累",
    "concept_cards": "关键概念卡片",
    "mind_map": "思维导图",
}


def material_dir(mid: str) -> Path:
    return MATERIALS_DIR / mid


def manifest_path(mid: str) -> Path:
    return material_dir(mid) / "manifest.json"


def create_material(title: str, source_type: str, source_file: str, source_markdown: str) -> dict[str, Any]:
    """Create a material folder under data/materials."""
    mid = material_id(title)
    folder = material_dir(mid)
    (folder / "notes").mkdir(parents=True, exist_ok=True)
    (folder / "outputs").mkdir(parents=True, exist_ok=True)

    manifest = {
        "id": mid,
        "title": title,
        "type": source_type,
        "source_file": source_file,
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


def get_source(mid: str) -> str:
    return read_text(material_dir(mid) / "source.md")


def get_note(mid: str, note_type: str) -> str:
    if note_type not in NOTE_TYPES:
        return ""
    return read_text(material_dir(mid) / "notes" / f"{note_type}.md")


def save_note(mid: str, note_type: str, content: str) -> None:
    if note_type not in NOTE_TYPES:
        raise ValueError("Unknown note type")
    write_text(material_dir(mid) / "notes" / f"{note_type}.md", content)
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


def note_editors_html(mid: str) -> str:
    """Render note editor forms for the material page."""
    sections = []
    for note_type, label in NOTE_TYPES.items():
        content = h(get_note(mid, note_type))
        sections.append(
            f"""
            <section class="editor-card">
              <h3>{h(label)}</h3>
              <form method="post" action="/api/materials/{h(mid)}/notes/{h(note_type)}">
                <textarea name="content" rows="10" placeholder="写在这里。保存后会变成 Markdown 文件。">{content}</textarea>
                <button type="submit">保存{h(label)}</button>
              </form>
            </section>
            """
        )
    return "\n".join(sections)


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
              <a class="button" href="/materials/{h(mid)}">打开处理页</a>
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

