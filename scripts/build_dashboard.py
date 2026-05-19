#!/usr/bin/env python3
"""
Legacy helper.

The project now uses a local Python web app instead of a static dashboard.
This script writes a small landing page that points to the real app.
"""

from __future__ import annotations

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_PATH = PROJECT_ROOT / "dashboard" / "index.html"


def main() -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(
        """<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>read-level-system</title>
  <style>
    body {
      margin: 0;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      background: #f7f5f0;
      color: #252525;
    }
    main {
      max-width: 760px;
      margin: 80px auto;
      padding: 28px;
      background: #fffdf8;
      border: 1px solid #e3ddd1;
      border-radius: 8px;
    }
    code {
      display: block;
      padding: 12px;
      border-radius: 8px;
      background: #f0ece3;
    }
    a {
      color: #177e76;
    }
  </style>
</head>
<body>
  <main>
    <h1>请启动本地系统</h1>
    <p>第一版已经改成本地前后端，不再使用静态 dashboard 作为主入口。</p>
    <p>在项目目录运行：</p>
    <code>python3 app.py</code>
    <p>然后打开：</p>
    <p><a href="http://127.0.0.1:8765">http://127.0.0.1:8765</a></p>
  </main>
</body>
</html>
""",
        encoding="utf-8",
    )
    print(f"Wrote landing page: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()

