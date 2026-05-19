# 前后端架构

这个项目第一版是本地运行的小系统，不是纯静态 HTML。

## 启动方式

```bash
python3 app.py
```

打开：

```text
http://127.0.0.1:8765
```

## 架构边界

前端只访问页面路由，不直接访问本地文件夹。

后端负责读写文件夹和 Markdown / JSON。

这样不会再出现浏览器打开文件夹后显示“目录索引”的问题。

## 前端

```text
frontend/
  templates/
    dashboard.html   # 首页
    import.html      # 导入资料
    materials.html   # 资料库
    material.html    # 单份资料处理页
    writing.html     # 写作页
    settings.html    # 目标设置
    message.html     # 错误/提示页
  static/
    style.css
    app.js
```

前端页面职责：

- 首页：展示真实状态，不使用 demo 数据。
- 导入页：上传 PDF / 文章，或粘贴文章。
- 资料页：写现实启发、行动清单、内容选题、英语积累、概念卡、思维导图和草稿。
- 写作页：写不绑定具体资料的草稿。
- 设置页：修改当前目标。

## 后端

```text
backend/
  routes.py            # 页面路由和表单提交
  import_service.py    # 导入 PDF / 文章
  material_service.py  # 资料、笔记、草稿读写
  score_service.py     # 分数、证据和首页状态
  profile_service.py   # 目标设置
  template.py          # 简单模板渲染
  paths.py             # 项目路径
  utils.py             # 通用工具
```

后端路由：

```text
GET  /                         首页
GET  /import                   导入资料
POST /api/import/pdf           上传 PDF
POST /api/import/article       上传文章文件
POST /api/import/article-text  粘贴文章内容
GET  /materials                资料库
GET  /materials/<id>           单份资料处理页
POST /api/materials/<id>/notes/<type>
POST /api/materials/<id>/outputs/draft
GET  /writing                  写作页
POST /api/writing/inbox        保存独立草稿
GET  /settings                 目标设置
POST /api/settings/profile     保存目标
POST /api/score/rebuild        根据真实 score_growth.json 重建首页
```

## 数据层

```text
data/
  raw/
    pdf/          # 上传的 PDF 原文件
    articles/     # 上传或粘贴的文章原文
  materials/
    <material_id>/
      manifest.json
      source.md
      notes/
        reality_insights.md
        action_list.md
        content_topics.md
        english_extract.md
        concept_cards.md
        mind_map.md
      outputs/
        draft.md
        score_growth.json
  writing/
    drafts/
      inbox.md
  scores/
    score.json
```

## 真实状态规则

首页必须遵守：

1. 没有导入资料：不判断薄弱项，四项能力都是 0。
2. 导入资料但没有写笔记：不判断薄弱项，不加分。
3. 写了笔记但没有 `score_growth.json`：显示“等待评分”，不自动加分。
4. 只有真实 `score_growth.json` 才能更新能力值和 AI 薄弱项。
5. `examples/` 永远只是示例，不进入真实首页。

## 失败处理规则

同一个问题最多尝试 3 次。

第 3 次仍然不通，就停下来问方向，不继续硬改。

