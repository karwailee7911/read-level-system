from __future__ import annotations

import cgi
import mimetypes
from http.server import BaseHTTPRequestHandler
from pathlib import Path
from urllib.parse import parse_qs, quote, unquote, urlparse

from backend.import_service import import_article_text, import_article_upload, import_pdf_upload
from backend.material_service import (
    get_draft,
    get_material,
    get_source,
    list_materials,
    materials_list_html,
    note_editors_html,
    recent_materials_html,
    save_draft,
    save_note,
)
from backend.paths import DRAFTS_DIR, STATIC_DIR
from backend.profile_service import get_goal, get_profile_text, save_goal
from backend.score_service import ability_rows_html, dashboard_status, load_score, rebuild_score_from_material_scores
from backend.template import render_template
from backend.utils import h, read_text, write_text


class ReadLevelHandler(BaseHTTPRequestHandler):
    """Small local web app handler."""

    server_version = "read-level-system/0.1"

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        path = parsed.path
        query = parse_qs(parsed.query)

        if path.startswith("/static/"):
            self.serve_static(path)
            return
        if path == "/":
            self.page_dashboard(query)
            return
        if path == "/import":
            self.page_import(query)
            return
        if path == "/materials":
            self.page_materials(query)
            return
        if path.startswith("/materials/"):
            self.page_material_detail(path, query)
            return
        if path == "/writing":
            self.page_writing(query)
            return
        if path == "/settings":
            self.page_settings(query)
            return

        self.not_found()

    def do_POST(self) -> None:
        parsed = urlparse(self.path)
        path = parsed.path

        try:
            if path == "/api/import/article":
                self.action_import_article()
                return
            if path == "/api/import/article-text":
                self.action_import_article_text()
                return
            if path == "/api/import/pdf":
                self.action_import_pdf()
                return
            if path.startswith("/api/materials/") and "/notes/" in path:
                self.action_save_note(path)
                return
            if path.startswith("/api/materials/") and path.endswith("/outputs/draft"):
                self.action_save_draft(path)
                return
            if path == "/api/writing/inbox":
                self.action_save_writing_inbox()
                return
            if path == "/api/settings/profile":
                self.action_save_settings()
                return
            if path == "/api/score/rebuild":
                self.action_rebuild_score()
                return
        except Exception as exc:
            self.redirect(f"/?msg={quote('操作失败：' + str(exc))}")
            return

        self.not_found()

    def log_message(self, format: str, *args) -> None:
        """Keep terminal output quiet."""
        return

    def send_html(self, html: str, status: int = 200) -> None:
        data = html.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def redirect(self, location: str) -> None:
        self.send_response(303)
        self.send_header("Location", location)
        self.end_headers()

    def not_found(self) -> None:
        self.send_html(
            render_template(
                "message.html",
                {
                    "title": "没有找到页面",
                    "message": "这个地址不是系统页面。请回到首页。",
                    "action_url": "/",
                    "action_label": "回首页",
                },
            ),
            status=404,
        )

    def serve_static(self, path: str) -> None:
        relative = path.replace("/static/", "", 1)
        target = (STATIC_DIR / relative).resolve()
        if not str(target).startswith(str(STATIC_DIR.resolve())) or not target.exists():
            self.not_found()
            return

        data = target.read_bytes()
        content_type = mimetypes.guess_type(str(target))[0] or "application/octet-stream"
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def page_dashboard(self, query: dict[str, list[str]]) -> None:
        score = load_score()
        materials = list_materials()
        status = dashboard_status(score)
        self.send_html(
            render_template(
                "dashboard.html",
                {
                    "message": self.message_html(query),
                    "goal": h(score.get("profile", {}).get("goal", "")),
                    "state_label": h(status["label"]),
                    "weak_ability": h(status["ability"]),
                    "confidence": h(status["confidence"]),
                    "reason": h(status["reason"]),
                    "next_task": h(status["next_task"]),
                    "evidence_html": status["evidence"],
                    "ability_rows": ability_rows_html(score),
                    "recent_materials": recent_materials_html(materials),
                },
            )
        )

    def page_import(self, query: dict[str, list[str]]) -> None:
        self.send_html(render_template("import.html", {"message": self.message_html(query)}))

    def page_materials(self, query: dict[str, list[str]]) -> None:
        materials = list_materials()
        self.send_html(
            render_template(
                "materials.html",
                {
                    "message": self.message_html(query),
                    "materials": materials_list_html(materials),
                },
            )
        )

    def page_material_detail(self, path: str, query: dict[str, list[str]]) -> None:
        mid = unquote(path.strip("/").split("/", 1)[1])
        material = get_material(mid)
        if not material:
            self.not_found()
            return

        source = get_source(mid)
        source_preview = h(source[:5000] + ("\n\n..." if len(source) > 5000 else ""))
        draft = h(get_draft(mid))
        self.send_html(
            render_template(
                "material.html",
                {
                    "message": self.message_html(query),
                    "id": h(mid),
                    "title": h(material.get("title", "未命名资料")),
                    "type": h(material.get("type", "")),
                    "imported_at": h(material.get("imported_at", "")),
                    "source_preview": source_preview,
                    "note_editors": note_editors_html(mid),
                    "draft": draft,
                },
            )
        )

    def page_writing(self, query: dict[str, list[str]]) -> None:
        inbox_path = DRAFTS_DIR / "inbox.md"
        self.send_html(
            render_template(
                "writing.html",
                {
                    "message": self.message_html(query),
                    "draft": h(read_text(inbox_path)),
                },
            )
        )

    def page_settings(self, query: dict[str, list[str]]) -> None:
        self.send_html(
            render_template(
                "settings.html",
                {
                    "message": self.message_html(query),
                    "goal": h(get_goal()),
                    "profile": h(get_profile_text()),
                },
            )
        )

    def message_html(self, query: dict[str, list[str]]) -> str:
        msg = query.get("msg", [""])[0]
        if not msg:
            return ""
        return f'<div class="notice">{h(msg)}</div>'

    def parse_urlencoded(self) -> dict[str, str]:
        length = int(self.headers.get("Content-Length", "0") or 0)
        raw = self.rfile.read(length).decode("utf-8")
        parsed = parse_qs(raw)
        return {key: values[0] if values else "" for key, values in parsed.items()}

    def parse_multipart(self) -> cgi.FieldStorage:
        return cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={
                "REQUEST_METHOD": "POST",
                "CONTENT_TYPE": self.headers.get("Content-Type", ""),
            },
        )

    def uploaded_file(self, form: cgi.FieldStorage) -> tuple[str, bytes]:
        item = form["file"] if "file" in form else None
        if item is None or not getattr(item, "filename", ""):
            raise ValueError("没有选择文件")
        filename = Path(item.filename).name
        data = item.file.read()
        if not data:
            raise ValueError("文件是空的")
        return filename, data

    def action_import_article(self) -> None:
        form = self.parse_multipart()
        filename, data = self.uploaded_file(form)
        title = form.getfirst("title", "")
        material = import_article_upload(filename, data, title)
        self.redirect(f"/materials/{quote(material['id'])}?msg={quote('文章已导入，现在可以写笔记。')}")

    def action_import_article_text(self) -> None:
        form = self.parse_urlencoded()
        title = form.get("title", "").strip()
        content = form.get("content", "").strip()
        if not content:
            raise ValueError("文章内容不能为空")
        material = import_article_text(title, content)
        self.redirect(f"/materials/{quote(material['id'])}?msg={quote('文章已导入，现在可以写笔记。')}")

    def action_import_pdf(self) -> None:
        form = self.parse_multipart()
        filename, data = self.uploaded_file(form)
        title = form.getfirst("title", "")
        material = import_pdf_upload(filename, data, title)
        self.redirect(f"/materials/{quote(material['id'])}?msg={quote('PDF 已导入，现在可以写笔记。')}")

    def action_save_note(self, path: str) -> None:
        parts = path.strip("/").split("/")
        mid = unquote(parts[2])
        note_type = unquote(parts[4])
        form = self.parse_urlencoded()
        save_note(mid, note_type, form.get("content", ""))
        self.redirect(f"/materials/{quote(mid)}?msg={quote('笔记已保存。')}")

    def action_save_draft(self, path: str) -> None:
        parts = path.strip("/").split("/")
        mid = unquote(parts[2])
        form = self.parse_urlencoded()
        save_draft(mid, form.get("content", ""))
        self.redirect(f"/materials/{quote(mid)}?msg={quote('草稿已保存。')}")

    def action_save_writing_inbox(self) -> None:
        form = self.parse_urlencoded()
        write_text(DRAFTS_DIR / "inbox.md", form.get("content", ""))
        self.redirect(f"/writing?msg={quote('草稿已保存。')}")

    def action_save_settings(self) -> None:
        form = self.parse_urlencoded()
        save_goal(form.get("goal", ""))
        self.redirect(f"/settings?msg={quote('目标已保存。')}")

    def action_rebuild_score(self) -> None:
        rebuild_score_from_material_scores()
        self.redirect(f"/?msg={quote('已根据真实 score_growth.json 重新生成首页数据。')}")

