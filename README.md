# read-level-system

本地运行的个人读书经验系统。

它不是普通读书笔记工具，而是一个“个人知识成长系统”：把 PDF 电子书和公众号文章转化为结构化笔记、行动清单、内容选题、英语表达积累，并根据真实证据评估能力成长。

第一版使用：

- Python 本地后端
- Markdown
- JSON
- 本地网页前端

不接 Notion，不用数据库。

## 启动

```bash
cd /Users/karwai/Documents/个人成长系统/read-level-system
python3 app.py
```

打开：

```text
http://127.0.0.1:8765
```

## 一键启动

第一次使用：

```bash
chmod +x start.command
```

以后使用：

- 双击 `start.command`

打开地址：

```text
http://127.0.0.1:8765
```

说明：

- 这是本地网页，不是公网网站。
- PDF、公众号文章、笔记都保存在本机 `data/` 目录。
- `.gitignore` 已经阻止真实资料上传 GitHub。
- 第一版只支持可复制文字的 PDF。
- 扫描版、图片型、加密 PDF 暂不支持 OCR。

## 当前规则

真实首页从空白开始：

- 没有导入资料：四项能力都是 0。
- 没有个人理解、行动、草稿或英文练习：不加分。
- 没有 `score_growth.json`：不自动评分。
- 项目从空白状态开始，不内置任何书籍或文章内容。

## 主要页面

```text
/             首页
/import       导入资料
/materials    资料库
/writing      写作页
/settings     目标设置
```

## 文件结构

```text
read-level-system/
  app.py
  backend/
  frontend/
    templates/
    static/
  config/
    user_profile.example.md
    user_profile.md
    ability_rules.md
    scoring_rules.md
  prompts/
  data/
    raw/
      pdf/
      articles/
    materials/
      <material_id>/
        manifest.json
        source.md
        notes/
        outputs/
    writing/
      drafts/
    scores/
      score.json
```

## GitHub 上传说明

这个项目适合上传代码和示例，不适合上传你的真实阅读资料。

会保留在仓库里的内容：

- 本地后端和前端代码
- 能力规则和评分规则
- 提示词模板
- `score.example.json`
- `user_profile.example.md`

不会上传的本地个人数据：

- `data/raw/` 里的 PDF 和文章
- `data/materials/` 里的真实资料、笔记和草稿
- `data/writing/drafts/` 里的真实草稿
- `data/scores/score.json`
- `config/user_profile.md`

这些规则写在：

```text
.gitignore
```

## 详细架构

见：

```text
ARCHITECTURE.md
```

## 命令行导入

也可以不用网页，直接命令行导入：

```bash
python3 scripts/import_article.py data/raw/articles/你的文章.md
python3 scripts/import_pdf.py data/raw/pdf/你的书.pdf
```

导入结果会进入：

```text
data/materials/<material_id>/
```
