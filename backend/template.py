from __future__ import annotations

from backend.paths import TEMPLATE_DIR


def render_template(name: str, context: dict[str, str]) -> str:
    """Tiny template renderer for {{ key }} placeholders."""
    template = (TEMPLATE_DIR / name).read_text(encoding="utf-8")
    for key, value in context.items():
        template = template.replace("{{ " + key + " }}", value)
    return template

