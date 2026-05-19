from __future__ import annotations

from typing import Any

from backend.material_service import list_materials, material_dir, material_has_user_evidence
from backend.paths import SCORE_PATH
from backend.utils import h, read_json, today, write_json


ABILITIES = ["认知力", "表达力", "商业力", "英语力"]


def empty_score(goal: str = "先导入第一份资料，再根据真实证据判断薄弱项。") -> dict[str, Any]:
    return {
        "profile": {
            "goal": goal,
            "updated_at": today(),
        },
        "abilities": {
            name: {"value": 0.0, "weekly_delta": 0.0, "evidence": []}
            for name in ABILITIES
        },
        "ai_weakness": None,
        "recent_materials": [],
        "weekly_changes": [],
    }


def load_score() -> dict[str, Any]:
    score = read_json(SCORE_PATH, empty_score())
    base = empty_score(score.get("profile", {}).get("goal", empty_score()["profile"]["goal"]))
    base.update(score)
    base["abilities"] = {**base["abilities"], **score.get("abilities", {})}
    for name in ABILITIES:
        base["abilities"].setdefault(name, {"value": 0.0, "weekly_delta": 0.0, "evidence": []})
    return base


def save_score(score: dict[str, Any]) -> None:
    write_json(SCORE_PATH, score)


def reset_score_to_empty() -> None:
    save_score(empty_score())


def rebuild_score_from_material_scores() -> dict[str, Any]:
    """
    Rebuild score.json from real material score_growth.json files.

    No score_growth.json means no growth. This prevents fake progress.
    """
    current = load_score()
    score = empty_score(current.get("profile", {}).get("goal", ""))
    materials = list_materials()
    score["recent_materials"] = [
        {
            "title": item.get("title", ""),
            "type": item.get("type", ""),
            "date": str(item.get("imported_at", ""))[:10],
            "id": item.get("id", ""),
        }
        for item in materials[:10]
    ]

    latest_ai = None
    for item in reversed(materials):
        mid = item.get("id", "")
        growth = read_json(material_dir(mid) / "outputs" / "score_growth.json", None)
        if not growth:
            continue
        for ability in ABILITIES:
            ability_growth = growth.get("growth", {}).get(ability, {})
            delta = float(ability_growth.get("delta", 0) or 0)
            delta = max(0.0, min(delta, 0.5))
            score["abilities"][ability]["value"] += delta
            score["abilities"][ability]["weekly_delta"] += delta
            score["abilities"][ability]["evidence"].extend(ability_growth.get("evidence", []))
        if growth.get("ai_weakness"):
            latest_ai = growth["ai_weakness"]

    score["ai_weakness"] = latest_ai
    score["weekly_changes"] = []
    save_score(score)
    return score


def dashboard_status(score: dict[str, Any]) -> dict[str, str]:
    materials = list_materials()
    has_evidence = any(material_has_user_evidence(item.get("id", "")) for item in materials)
    ai_weakness = score.get("ai_weakness")

    if not materials:
        return {
            "label": "还没有导入资料",
            "ability": "暂不判断",
            "reason": "系统没有任何真实资料，因此不能判断薄弱项，也不能给任何能力加分。",
            "next_task": "先导入第一份 PDF 或公众号文章。",
            "evidence": "<p class=\"empty\">暂无证据。</p>",
        }

    if not has_evidence:
        return {
            "label": "已有资料，但还没有个人证据",
            "ability": "暂不判断",
            "reason": "你已经导入资料，但还没有写个人理解、行动清单、草稿或英文练习。此时不能判断薄弱项。",
            "next_task": "打开一份资料，先写“与我现实有关的启发”。",
            "evidence": "<p class=\"empty\">暂无可评分证据。</p>",
        }

    if not ai_weakness:
        return {
            "label": "等待评分",
            "ability": "暂未评分",
            "reason": "你已经写了笔记，但还没有生成评分文件。",
            "next_task": "复制本资料的笔记给 ChatGPT 评分，并把结果保存为 score_growth.json。",
            "evidence": "<p class=\"empty\">已有笔记或草稿，但还没有评分证据。</p>",
        }

    evidence = ai_weakness.get("evidence", [])
    if evidence:
        evidence_html = "<ul class=\"simple-list\">" + "".join(
            f"<li>{h(item)}</li>" for item in evidence
        ) + "</ul>"
    else:
        evidence_html = "<p class=\"empty\">暂无证据。</p>"
    return {
        "label": "AI 已根据证据判断",
        "ability": ai_weakness.get("ability", "暂未评分"),
        "reason": ai_weakness.get("reason", ""),
        "next_task": ai_weakness.get("next_task", ""),
        "evidence": evidence_html,
    }


def ability_rows_html(score: dict[str, Any]) -> str:
    rows = []
    for name in ABILITIES:
        item = score.get("abilities", {}).get(name, {})
        value = float(item.get("value", 0) or 0)
        delta = float(item.get("weekly_delta", 0) or 0)
        evidence = item.get("evidence", [])
        evidence_text = evidence[0] if evidence else "暂无证据"
        rows.append(
            f"""
            <section class="ability-row">
              <div class="ability-meta">
                <strong>{name}</strong>
                <span>{value:.1f}%</span>
              </div>
              <div class="bar"><div style="width: {max(0, min(value, 100)):.1f}%"></div></div>
              <p>本周 +{delta:.1f}% · {evidence_text}</p>
            </section>
            """
        )
    return "\n".join(rows)
