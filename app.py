#!/usr/bin/env python3
"""
Local entry point for read-level-system.

Run:
  python3 app.py

Then open:
  http://127.0.0.1:8765
"""

from __future__ import annotations

from http.server import ThreadingHTTPServer

from backend.paths import ensure_project_dirs
from backend.routes import ReadLevelHandler


def main() -> None:
    ensure_project_dirs()
    host = "127.0.0.1"
    port = 8765
    server = ThreadingHTTPServer((host, port), ReadLevelHandler)
    print(f"read-level-system is running at http://{host}:{port}")
    print("Press Ctrl+C to stop.")
    server.serve_forever()


if __name__ == "__main__":
    main()

