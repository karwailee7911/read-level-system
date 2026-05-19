from __future__ import annotations

from backend.paths import USER_PROFILE_PATH
from backend.score_service import load_score, save_score
from backend.utils import read_text, today, write_text


def get_goal() -> str:
    score = load_score()
    return score.get("profile", {}).get("goal", "先导入第一份资料，再根据真实证据判断薄弱项。")


def get_profile_text() -> str:
    return read_text(USER_PROFILE_PATH, "")


def save_goal(goal: str) -> None:
    score = load_score()
    score.setdefault("profile", {})
    score["profile"]["goal"] = goal.strip() or "先导入第一份资料，再根据真实证据判断薄弱项。"
    score["profile"]["updated_at"] = today()
    save_score(score)

    existing = get_profile_text()
    if existing.strip():
        content = existing
    else:
        content = "# 用户目标档案\n\n## 当前目标\n\n"
    if "## 当前目标" in content:
        before, _, after = content.partition("## 当前目标")
        rest = after.split("\n## ", 1)
        suffix = ("\n## " + rest[1]) if len(rest) == 2 else ""
        content = before + "## 当前目标\n\n" + score["profile"]["goal"] + "\n" + suffix
    else:
        content = content.rstrip() + "\n\n## 当前目标\n\n" + score["profile"]["goal"] + "\n"
    write_text(USER_PROFILE_PATH, content)

