#!/usr/bin/env python3
"""
Unified UI copy management.

All user-facing strings are defined here, not scattered in HTML templates.
This ensures consistent product messaging and prevents implementation details
from leaking into the interface.
"""

from __future__ import annotations


DASHBOARD = {
    "title": "能力成长追踪",
    "goal_label": "当前目标",
    "status_no_materials": {
        "label": "准备开始",
        "ability": "—",
        "confidence": "none",
        "reason": "导入第一份资料后，系统才能判断你的薄弱项。",
        "next_task": "导入 PDF 或公众号文章",
    },
    "status_no_evidence": {
        "label": "已有资料",
        "ability": "—",
        "confidence": "none",
        "reason": "你已导入资料，现在需要写出个人理解和行动才能开始评分。",
        "next_task": "打开资料，记录对你有启发的地方",
    },
    "status_no_score": {
        "label": "等待评分",
        "ability": "—",
        "confidence": "none",
        "reason": "已发现你的笔记，现在正待评分生成成长数据。",
        "next_task": "继续导入更多资料，丰富评分样本",
    },
    "status_scored": {
        "label": "AI 已评分",
        "ability_template": "{ability}",
        "confidence_template": "评分准度 {confidence}",
    },
    "section_workflow": {
        "step_1_title": "1. 导入资料",
        "step_1_desc": "上传 PDF 或粘贴公众号文章。",
        "step_2_title": "2. 写笔记",
        "step_2_desc": "记录启发、行动、选题、英文积累。",
        "step_3_title": "3. 输出草稿",
        "step_3_desc": "把学习转化为 300 字以上的真实输出。",
    },
    "abilities_section": "能力成长",
    "recent_section": "最近导入",
}

IMPORT = {
    "title": "导入资料",
    "hero_title": "把资料放进系统",
    "hero_desc": "导入只提取原文，不自动加分。成长需要你后续的笔记和输出。",
    "pdf_section": "上传 PDF",
    "pdf_label_title": "PDF 标题（可选）",
    "pdf_label_title_placeholder": "例如：原则",
    "pdf_label_file": "PDF 文件",
    "pdf_button": "导入 PDF",
    "article_section": "上传文章文件",
    "article_label_title": "文章标题（可选）",
    "article_label_title_placeholder": "将自动读取文章标题",
    "article_label_file": "Markdown 或 txt 文件",
    "article_button": "导入文章文件",
    "paste_section": "直接粘贴",
    "paste_label_title": "文章标题",
    "paste_label_title_placeholder": "例如：一篇关于商业判断的文章",
    "paste_label_content": "文章内容",
    "paste_label_content_placeholder": "把公众号文章正文粘贴到这里",
    "paste_button": "导入粘贴内容",
}

MATERIALS = {
    "title": "资料库",
    "empty": "还没有导入资料。",
    "item_type_pdf": "PDF",
    "item_type_article": "文章",
    "button_open": "打开",
}

MATERIAL_DETAIL = {
    "title_template": "{title}",
    "meta_type": "类型",
    "meta_imported": "导入时间",
    "section_notes": "个人笔记",
    "note_reality_insights": "与我现实有关的启发",
    "note_action_list": "可执行行动清单",
    "note_content_topics": "内容选题",
    "note_english_extract": "英语表达积累",
    "note_concept_cards": "关键概念卡片",
    "note_mind_map": "思维导图",
    "section_draft": "输出草稿",
    "button_save": "保存",
    "placeholder_note": "写在这里，保存后变成 Markdown 文件。",
    "placeholder_draft": "输出完成后标记为完成。",
}

WRITING = {
    "title": "写作",
    "hero_title": "不绑定资料的草稿",
    "hero_desc": "如果是针对某份资料的输出，建议在那份资料的处理页里写。",
    "label": "Inbox 草稿",
    "placeholder": "临时草稿。保存后变成 Markdown 文件。",
    "button": "保存草稿",
}

SETTINGS = {
    "title": "目标设置",
    "hero_title": "设置你的当前目标",
    "hero_desc": "只显示目标，不显示系统配置。",
    "goal_label": "目标",
    "goal_button": "保存目标",
    "abilities_section": "能力维度",
    "abilities_desc": {
        "cognition": "认知力：理解问题、提炼概念、提出质疑、连接现实。",
        "expression": "表达力：用自己的话讲清楚，形成可输出内容。",
        "business": "商业力：发现需求、场景、产品、流量或行动机会。",
        "english": "英语力：积累词汇、句式、阅读理解和表达练��。",
    },
    "scoring_section": "评分原则",
    "scoring_rules": [
        "没有证据，不加分。",
        "只摘要，少加分。",
        "有输出、有复盘、有行动，才加分。",
        "单次单项最高 +0.5%。",
    ],
}

MESSAGES = {
    "material_imported": "资料已导入，现在可以写笔记。",
    "note_saved": "笔记已保存。",
    "draft_saved": "草稿已保存。",
    "goal_saved": "目标已保存。",
    "score_rebuilt": "已根据真实 score_growth.json 重新生成首页数据。",
    "error_prefix": "操作失败：",
    "error_no_file": "没有选择文件",
    "error_empty_file": "文件是空的",
    "error_empty_content": "文章内容不能为空",
}

NAV = {
    "brand": "Read Level System",
    "import": "导入资料",
    "materials": "资料库",
    "writing": "写作",
    "settings": "目标设置",
}
