from __future__ import annotations

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
FRONTEND_DIR = PROJECT_ROOT / "frontend"
TEMPLATE_DIR = FRONTEND_DIR / "templates"
STATIC_DIR = FRONTEND_DIR / "static"

DATA_DIR = PROJECT_ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
RAW_PDF_DIR = RAW_DIR / "pdf"
RAW_ARTICLE_DIR = RAW_DIR / "articles"
MATERIALS_DIR = DATA_DIR / "materials"
WRITING_DIR = DATA_DIR / "writing"
DRAFTS_DIR = WRITING_DIR / "drafts"
SCORES_DIR = DATA_DIR / "scores"
SCORE_PATH = SCORES_DIR / "score.json"
CONFIG_DIR = PROJECT_ROOT / "config"
USER_PROFILE_PATH = CONFIG_DIR / "user_profile.md"


def ensure_project_dirs() -> None:
    """Create the folders the local app needs."""
    for path in [
        RAW_PDF_DIR,
        RAW_ARTICLE_DIR,
        MATERIALS_DIR,
        DRAFTS_DIR,
        SCORES_DIR,
        STATIC_DIR,
        TEMPLATE_DIR,
        CONFIG_DIR,
    ]:
        path.mkdir(parents=True, exist_ok=True)

