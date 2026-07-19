# 🚀 GitHub 上传通用指南

> 把本地仓库上传到 GitHub 并完善的 **6 步流程**。适用于本仓库和后续美食 Skill 仓库（food-social-content）。

---

## 📋 上传前自检清单

发布前确认：

```bash
cd /path/to/your-repo
echo "📋 Pre-upload checklist..."

# 1. README 完整
test -f README.md && echo "✅ README.md 存在" || echo "❌ README.md 缺失"

# 2. LICENSE
test -f LICENSE && echo "✅ LICENSE 存在" || echo "❌ LICENSE 缺失"

# 3. SKILL.md 有标准 frontmatter
head -1 SKILL.md | grep -q "^---$" && echo "✅ SKILL.md frontmatter 正常" || echo "❌ SKILL.md frontmatter 缺失"

# 4. Git 已 commit
[ -d .git ] && echo "✅ Git 仓库已初始化" || echo "❌ .git 缺失"

# 5. 没有敏感信息
! git grep -l "sk-proj\|sk-or-v1\|AKIA\|password\|secret" 2>/dev/null && echo "✅ 无敏感信息泄漏" || echo "⚠️  检测到可能的密钥"

# 6. .gitignore 完整
test -f .gitignore && echo "✅ .gitignore 存在" || echo "❌ .gitignore 缺失"

# 7. CHANGELOG 已写
test -f docs/CHANGELOG.md && echo "✅ CHANGELOG 存在" || echo "❌ CHANGELOG 缺失"

# 8. examples 真实可复现
test -f examples/leshan-output.md && test -f examples/xian-output.md && echo "✅ examples 完整" || echo "❌ examples 不全"

# 9. README 没有 internal tokens
! grep -q "Bearer\|api_key=" README.md 2>/dev/null && echo "✅ README 无硬编码 token" || echo "⚠️  README 含 token"

# 10. 数量统计
echo "📊 项目体量:"
echo "  - 文件数: $(find . -type f -not -path './.git/*' | wc -l | tr -d ' ')"
echo "  - 代码行数: $(find . -type f \( -name '*.md' -o -name '*.sh' -o -name '*.py' -o -name '*.yml' -o -name '*.toml' \) -not -path './.git/*' -exec cat {} + | wc -l | tr -d ' ')"
```

---

## 🚀 6 步上传流程

### Step 1 · GitHub 创建空仓库

```
1. 打开 https://github.com/new
2. 填写 Repository name: travel-social-content
3. Description: "Generate travel destination social media content plans for XHS/IG/WeChat/Weibo"
4. ❌ 不勾选 README (用自己写的)
5. ❌ 不勾选 LICENSE (用自己写的)  
6. ❌ 不勾选 .gitignore (用自己写的)
7. ❌ 不勾选 LICENSE (用自己写的)
8. Public (开源) 或 Private (私有)
9. Create repository
```

---

### Step 2 · 本地 Git 推到 GitHub

```bash
cd /Users/a1234/Documents/06-YouTube/travel-social-content

# 添加 GitHub 远端（替换 bethel-mark）
git remote add origin git@github.com:bethel-mark/travel-social-content.git

# 主分支改名（GitHub 默认 main）
git branch -M main

# 推送主分支
git push -u origin main

# 推送 tags（如果有）
git push --tags
```

> 💡 **GitHub 推荐 SSH 推送**。https 推送需用 Personal Access Token (PAT)：
> `git remote add origin https://YOUR_TOKEN@github.com/bethel-mark/travel-social-content.git`

---

### Step 3 · 配置 GitHub Pages（README 自动渲染）

```
1. 在 GitHub 仓库页 → Settings → Pages
2. Source: Deploy from a branch
3. Branch: main → / (root)
4. Save

# 等待 1-2 分钟，访问:
# https://bethel-mark.github.io/travel-social-content/
```

GitHub Pages 会自动用 Jekyll 渲染 `README.md`。**注意**：

- **图片**：用 markdown `![](https://...)` 引用仓库内图片。仓库内图片用相对路径：`![](docs/images/screenshot.png)`
- **GitHub Pages 默认域名是 `<user>.github.io/<repo>`**，不是 `<user>.github.io`，所以路径都以 `/<repo>` 开头

---

### Step 4 · 配置 GitHub Secrets（API Keys 加密）

```
1. 仓库页 → Settings → Secrets and variables → Actions
2. New repository secret
3. 添加以下 secrets（按需）:

GOOGLE_API_KEY          = AIza-xxx
OPENAI_API_KEY          = sk-proj-xxx
OPENROUTER_API_KEY      = sk-or-v1-xxx
BAILIAN_API_KEY         = sk-xxx
ZHIPU_API_KEY           = 594db1c9fb1f...
DEEPSEEK_API_KEY        = sk-xxx
KIMI_API_KEY            = sk-ocl...
ANTHROPIC_API_KEY       = sk-ant-...

4. 后续在 .github/workflows/*.yml 中用:
   ${{ secrets.GOOGLE_API_KEY }}
```

**绝不能把 Key 写进代码或 commit！**

---

### Step 5 · 配置 GitHub Releases（可选）

```bash
# 创建第一个 release tag
cd travel-social-content
git tag -a v1.0.0 -m "v1.0.0 首发版：5 大景点 × 11 生图模型"
git push origin v1.0.0

# 在 GitHub 上:
# → Releases → Create release from tag
# → Title: v1.0.0 首发版
# → 自动生成 changelog
# → Publish release
```

**好处**：用户从 Releases 页面下 tarball / 看 changelog。

---

### Step 6 · 提交到 awesome-llm-skills 索引（推广）

```bash
# 1. fork 这些仓库：
#    - https://github.com/Prat011/awesome-llm-skills
#    - https://github.com/karanb192/awesome-claude-skills
#    - https://github.com/helloianneo/awesome-claude-code-skills
# 
# 2. 编辑他们的 README.md，在旅游/社媒分类下加一行：
#    - [travel-social-content](https://github.com/bethel-mark/travel-social-content)
#      - Generate complete social media content plans for travel destinations
#
# 3. 提交 PR，标题：Add travel-social-content skill
#
# 4. 等他们审核（一般 1-2 周）
```

**被收录的 checklist**：
- [ ] README 完整 + 截图
- [ ] LICENSE 明确（MIT/Apache/BSD）
- [ ] tags/releases 规范
- [ ] CI 跑过（绿色）
- [ ] codeowners 文件（可选）
- [ ] Contributing guide
- [ ] CODE_OF_CONDUCT（可选）

---

## 🧪 上传后必做 5 件事

### 1. 启用 GitHub Actions CI
- 仓库 → Actions → Enable workflow
- 第一次 push 会自动跑
- 期望结果：4 个 job 全绿（lint-markdown / lint-shell / smoke-test-api / smoke-test-image-adapter）

### 2. 设置 main 分支保护
```
Settings → Branches → Add branch protection rule
- Branch name pattern: main
- ☑ Require a pull request before merging
- ☑ Require status checks to pass before merging  
- ☑ Require signed commits (optional)
- ☑ Require linear history
```

### 3. 启用 Dependabot（自动依赖更新）
`.github/dependabot.yml`:
```yaml
version: 2
updates:
  - package-ecosystem: "pip"
    directory: "/"
    schedule:
      interval: "weekly"
```

### 4. 启用 Discussions（社区讨论）
- 仓库 → Settings → General → Features
- ☑ Discussions

### 5. 加 social-preview 图
Settings → Social preview → Upload an image (1280×640 PNG)

---

## 📣 上传后的传播策略

### 推特 / X 推广模板
```
🆕 开源 Skill: travel-social-content
给一个景点名 → 输出一份可发的 小红书/IG/朋友圈/微博 方案

✅ 5 种文案风格（系列打卡/情绪共鸣/反差吸引/数字攻略/沉浸脚本）
✅ 11 大生图模型 prompt（中英双语）
✅ Docker compose 一键起 FastAPI 服务
✅ 零外部 API 依赖

GitHub: https://github.com/bethel-mark/travel-social-content
```

### 知乎推广方向
- 「<a href="...">旅游社媒内容自动生成 Skill 开源了</a>」
- 「Claude Code Skill 怎么写？附我的 4 个真实案例」
- 「从白板到 8000 行：写一个 GitHub Skill 仓库的完整记录」

### B 站 / YouTube 视频
- 「用 AI 生成旅游社媒内容的完整工作流」
- 「5 分钟带你开发一个 Claude Code Skill」

---

## 🔧 上传后常见问题

### Q: Pages 显示 404？
A: 检查 `gh-pages` 分支或 `main /` 路径，确认 Settings → Pages 配对了。

### Q: CI 失败？
A: 看 Actions → 失败 log。常见原因：
- Python 版本不对（用 3.10+）
- 依赖装不上（升级 pip / 用 `pip install --upgrade pip`）
- shellcheck 找不到（CI 会自动装）

### Q: GitHub Pages 报「Jekyll build failed」？
A: 可能用了不被 Jekyll 支持的 markdown 插件。**最简单的解决**:
- Settings → Pages → 关闭 Pages
- 改用第三方 README 渲染服务（如 [gitreadme.dev](https://gitreadme.dev)）

### Q: 用户反映使用有问题？
A:
- 鼓励提 Issue
- 模板化 Issue (`.github/ISSUE_TEMPLATE/bug_report.md`)
- 添加 Discussions 标签 (question/enhancement/bug)

---

## ✅ 你对应的 ICON

```
⭐ Star History          → 仓库右上
👁️ Watch                → 关注 Releases
🍴 Fork                 → 二次开发
📝 Issue                → bug 报告
💬 Discussion           → 用法讨论
🔀 Pull Request         → 贡献代码
```

**目标**：发布 1 周内 50+ stars，1 月内 200+ stars，6 月内能进 awesome-claude-skills 索引。

---

## 🚀 一键上传脚本（参考）

```bash
#!/bin/bash
# upload-to-github.sh
# 用法: ./upload-to-github.sh your-username

if [ -z "$1" ]; then
    echo "Usage: $0 <github-username>"
    exit 1
fi

USER="$1"
REPO="$(basename $(pwd))"

echo "🚀 上传到 github.com/$USER/$REPO"

# 检查 git 状态
if [ -n "$(git status --porcelain)" ]; then
    echo "❌ 工作目录有未提交的改动，请先 commit"
    git status --short
    exit 1
fi

# 添加远端
if git remote get-url origin >/dev/null 2>&1; then
    echo "✓ origin 已存在"
else
    git remote add origin "git@github.com:$USER/$REPO.git"
    echo "✓ 已添加 origin"
fi

# 推送
git branch -M main
git push -u origin main

# 如果用了 tag
git push --tags 2>/dev/null || true

echo "✅ 上传完成!"
echo "   仓库: https://github.com/$USER/$REPO"
echo "   Pages: https://$USER.github.io/$REPO/"
```

---

最后 1 步：把 GitHub Pages 的 README render 当作**主视觉**，新用户看 Pages 就知道 skill 在做什么、有多漂亮。
