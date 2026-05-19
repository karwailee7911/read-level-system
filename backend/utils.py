from __future__ import annotations

import hashlib
import html
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any


def now_iso() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def today() -> str:
    return datetime.now().strftime("%Y-%m-%d")


def h(value: Any) -> str:
    return html.escape(str(value), quote=True)


def safe_name(value: str) -> str:
    """Create a readable local filename while keeping Chinese text."""
    value = value.strip().replace("/", "-").replace("\\", "-")
    value = re.sub(r"\s+", "_", value)
    value = re.sub(r'[<>:"|?*]', "", value)
    return value or "untitled"


def material_id(title: str) -> str:
    """Create a stable-enough URL-safe id for a new material."""
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    digest = hashlib.sha1(f"{stamp}:{title}".encode("utf-8")).hexdigest()[:8]
    return f"m_{stamp}_{digest}"


def read_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return default


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def read_text(path: Path, default: str = "") -> str:
    if not path.exists():
        return default
    return path.read_text(encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def decode_bytes(data: bytes) -> str:
    """Decode uploaded text with a small fallback chain."""
    for encoding in ("utf-8", "utf-8-sig", "gb18030"):
        try:
            return data.decode(encoding)
        except UnicodeDecodeError:
            continue
    return data.decode("utf-8", errors="replace")

