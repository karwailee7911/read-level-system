#!/usr/bin/env python3
"""
UI Copy Management - Centralized user interface strings.

Keeps all user-facing copy organized and separate from code logic.
All HTML templates should reference these strings via backend rendering.
"""

from __future__ import annotations

# ============================================================================
# DASHBOARD PAGE - Home page copy
# ============================================================================
DASHBOARD = {
    "page_title": "个人读书经验系统",
    "hero_subtitle": "当前目标",
    # Removed: "系统只根据真实资料、笔记、草稿和评分证据更新能力，不用演示数据冒充进度。"
    # This was a system explanation, not user-facing content

    "section_abilities": "四维能力",
    "section_recent": "最近处理",
    "section_evidence": "评分证据",

    "workflow_step_1_title": "1. 导入资料",
    "workflow_step_1_desc": "上传 PDF，或粘贴公众号文章。",
    "workflow_step_2_title": "2. 写结构化笔记",
    "workflow_step_2_desc": "在单份资料页写现实启发、行动和选题。",
    "workflow_step_3_title": "3. 写草稿",
    "workflow_step_3_desc": "把阅读转成 300 字以上的真实输出。",

    "button_import": "导入资料",
    "button_materials": "打开资料库",

    # Status labels for different dashboard states
    "status_no_materials": "还没有导入资料",
    "status_no_evidence": "已有资料，但还没有个人证据",
    "status_waiting_score": "已有证据，等待 AI 评分",
    "status_scored": "AI 已根据证据判断",

    "ability_none": "暂不判断",
    "ability_not_scored": "暂未评分",

    "reason_no_materials": "导入第一份资料后，系统才能判断你的薄弱项。",
    "reason_no_evidence": "你已导入资料，但还没有写个人理解。打开一份资料，先写内容。",
    "reason_waiting_score": "笔记或草稿已保存。可以对本次工作做一次手动评分。",

    "next_task_import": "先导入第一份 PDF 或公众号文章。",
    "next_task_evidence": "打开一份资料，写'与我现实有关的启发'。",
    "next_task_score": "对本次阅读工作做一次保守的自我评分。",

    "evidence_empty": "暂无证据。",
    "evidence_available": "已有笔记或草稿。",

    "recent_empty": "暂无。导入第一份资料后，这里才会出现记录。",

    "weekly_delta_prefix": "本周 +",
    "evidence_prefix": " · ",
}

# ============================================================================
# IMPORT PAGE
# ============================================================================
IMPORT = {
    "page_title": "导入资料",
    "hero_title": "先把资料放进系统，再开始写证据。",
    "hero_desc": "导入只提取原文，不自动加分。成长需要你后续的笔记和输出。",

    "section_pdf_title": "上传 PDF",
    "section_article_title": "上传公众号文章",
    "section_paste_title": "直接粘贴文章",

    "label_title": "���料标题，可不填",
    "label_pdf": "PDF 文件",
    "label_article": "Markdown 或 txt 文件",
    "label_article_content": "文章内容",

    "placeholder_title": "例如：原则",
    "placeholder_article_title": "默认读取文章标题",
    "placeholder_content": "把公众号文章正文粘贴到这里",

    "button_import_pdf": "导入 PDF",
    "button_import_article": "导入文章文件",
    "button_import_paste": "导入粘贴内容",

    "message_success_pdf": "PDF 已导入，现在可以写笔记。",
    "message_success_article": "文章已导入，现在可以写笔记。",
}

# ============================================================================
# MATERIALS PAGE - Material library
# ============================================================================
MATERIALS = {
    "page_title": "资料库",
    "list_empty": "还没有导入资料。",
    "button_open": "打开处理页",
}

# ============================================================================
# MATERIAL DETAIL PAGE
# ============================================================================
MATERIAL_DETAIL = {
    "section_notes_title": "笔记",
    "section_draft_title": "草稿",
    "message_note_saved": "笔记已保存。",
    "message_draft_saved": "草稿已保存。",
}

# ============================================================================
# WRITING PAGE - Independent drafts
# ============================================================================
WRITING = {
    "page_title": "写作",
    "hero_title": "不绑定资料的草稿",
    "hero_desc": "如果是针对某份资料的输出，建议在那份资料的处理页里写。",

    "label_draft": "Inbox 草稿",
    "placeholder_draft": "临时草稿，保存后变成 Markdown 文件。",
    "button_save": "保存草稿",
    "message_saved": "草稿已保存。",
}

# ============================================================================
# SETTINGS PAGE - Goals and ability definitions
# ============================================================================
SETTINGS = {
    "page_title": "目标设置",
    "hero_title": "设置你的当前目标",
    "hero_desc": "首页会根据这个目标判断你的薄弱项和下一步任务。",

    "label_goal": "当前目标",
    "button_save_goal": "保存目标",
    "message_saved": "目标已保存。",

    "section_abilities_title": "四维能力说明",
    "ability_cognition": "认知力：理解问题、提炼概念、提出质疑、连接现实。",
    "ability_expression": "表达力：用自己的话讲清楚，形成可输出内容。",
    "ability_business": "商业力：发现需求、场景、产品、流量或行动机会。",
    "ability_english": "英语力：积累词汇、句式、阅读理解和表达练习。",

    "section_scoring_title": "评分原则",
    "scoring_rule_1": "没有证据，不加分。",
    "scoring_rule_2": "只摘要，少加分。",
    "scoring_rule_3": "有输出、有复盘、有行动，才加分。",
    "scoring_rule_4": "单次单项最高 +0.5%。",
}

# ============================================================================
# NOTE TYPES - Labels for different note categories
# ============================================================================
NOTE_TYPES_DISPLAY = {
    "reality_insights": "与我现实有关的启发",
    "action_list": "可执行行动清单",
    "content_topics": "内容选题",
    "english_extract": "英语表达积累",
    "concept_cards": "关键概念卡片",
    "mind_map": "思维导图",
}

# ============================================================================
# NAVIGATION
# ============================================================================
NAVIGATION = {
    "brand": "Read Level System",
    "home": "首页",
    "import": "导入资料",
    "materials": "资料库",
    "writing": "写作",
    "settings": "目标设置",
}

# ============================================================================
# ERROR MESSAGES
# ============================================================================
ERRORS = {
    "page_not_found": "没有找到页面",
    "message_not_found": "这个地址不是系统页面。请回到首页。",
    "action_failed": "操作失败：",
    "no_file_selected": "没有选择文件",
    "file_is_empty": "文件是空的",
    "content_required": "文章内容不能为空",
    "unknown_note_type": "Unknown note type",
}

# ============================================================================
# COMMON UI ELEMENTS
# ============================================================================
UI_ELEMENTS = {
    "button_back_home": "回首页",
    "notice_prefix": "提示：",
    "empty_state": "暂无",
}
