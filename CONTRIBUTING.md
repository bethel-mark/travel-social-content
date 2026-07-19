# 🤝 Contributing

感谢你考虑为 `travel-social-content` 做贡献！本文档说明贡献流程。

## 🌟 适合贡献的内容

- 🆕 **新样例**：增加 `examples/<城市>-output.md`（如重庆 / 拉萨 / 厦门）
- 📚 **速查档案**：往 `references/destinations.md` 加新城市
- 🤖 **生图 prompt**：往 `references/image-models-optimization.md` 加新模型
- 🛠 **脚本**：往 `scripts/` 加新 CLI / Python 工具
- 📖 **文档**：修正 typo / 改进表达 / 翻译
- 🐛 **Bug 报告**：通过 Issue

## 📋 Pull Request 流程

1. **Fork** 仓库
2. 创建分支 (`git checkout -b feat/city-chongqing`)
3. **小颗粒度提交**（一个城市 = 一个 commit）
4. **确保通过本地烟测**（参见下方）
5. 写清晰的 PR 描述（用 PR 模板）
6. **至少 1 个 maintainer 审核通过**才能 merge

## ✅ 本地自检（在 push 前）

```bash
cd travel-social-content

# 1. Markdown 排版
which markdownlint && markdownlint references/ examples/ docs/

# 2. Shell 语法
shellcheck scripts/*.sh

# 3. Python 语法
python -m py_compile scripts/api/*.py

# 4. 7 项自检
for f in examples/*-output.md; do
  sections=$(grep -cE "^## " "$f")
  sub=$(grep -cE "^### [1-9]\." "$f")
  echo "$f: sections=$sections, sub-spots=$sub"
done

# 5. API 服务能起（如果有依赖）
pip install -r requirements-api.txt
bash scripts/install.sh symlink
```

## 📝 PR 描述模板

```markdown
## What this PR does
<!-- 一句话说明 -->

## Type of change
- [ ] 🆕 New sample (city/country)
- [ ] 📚 New city in destinations cheat-sheet
- [ ] 🤖 New image model guide
- [ ] 🐛 Bug fix
- [ ] 📖 Documentation

## How to verify
<!-- 步骤 -->

## References
<!-- 链接 -->
```

## ❌ 拒绝的贡献

- ❌ 复制第三方爆款全文（违反版权）
- ❌ 使用未授权风景/肖像图
- ❌ 虚假宣传某景区/某商家
- ❌ 引入额外外部 API 依赖（违反 skill 零依赖原则）
- ❌ 包含未经审查的 keys / secrets

## 🙏 第一贡献者奖励

- 🎁 Contributors 会被列入 README
- 🏆 Top 5 contributors 会被列入 RELEASE NOTES
- 🚀 累计 5 个 PR 可以成为 Maintainer

详细 PR 模板见 `.github/PULL_REQUEST_TEMPLATE.md`（待添加）。
