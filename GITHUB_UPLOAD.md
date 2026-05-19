# 上传到 GitHub

我已经把项目整理成适合上传的状态：

- `.gitignore` 已经排除真实资料、真实笔记、真实草稿和真实评分。
- `data/scores/score.example.json` 可以作为公开示例。
- `config/user_profile.example.md` 可以作为公开示例。
- `examples/` 只放演示内容。

## 需要你在终端里运行

当前环境不允许我创建 `.git` 目录，所以 `git init` 需要你自己运行。

```bash
cd /Users/karwai/Documents/个人成长系统/read-level-system
git init
git add .
git status
```

确认没有把个人数据加进去后，再提交：

```bash
git commit -m "Initial local read level system"
```

## 建议先建 private 仓库

在 GitHub 建一个 private repo，例如：

```text
read-level-system
```

然后按 GitHub 给你的地址添加远程仓库：

```bash
git remote add origin git@github.com:你的用户名/read-level-system.git
git branch -M main
git push -u origin main
```

如果你用 HTTPS：

```bash
git remote add origin https://github.com/你的用户名/read-level-system.git
git branch -M main
git push -u origin main
```

## 上传前重点检查

运行：

```bash
git status --short
```

不应该看到这些真实个人文件：

```text
data/raw/你的PDF或文章
data/materials/真实资料ID/
data/writing/drafts/真实草稿
data/scores/score.json
config/user_profile.md
```

