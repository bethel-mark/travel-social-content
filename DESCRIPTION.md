# Repository Description

> 此文件专为 GitHub 仓库页提供精简的项目说明（区别于 [`SKILL.md`](SKILL.md) 的完整技能规范）。

---

## 🧳 travel-social-content · 一句话定位

**为一个旅游城市/景点，输出一份可发的「小红书/IG/朋友圈/微博」社媒方案** —— 含 5 个子景点 × 5 种文案风格 × 11 大生图模型 × AI 中英 prompt。

---

## 🎯 何时使用

- **想要给一个城市做旅行系列内容**（乐山 / 西安 / 敦煌 / 大理 / 拉萨...）
- **想要借鉴成熟爆款结构**而不只是"复制粘贴"
- **需要中英双语对照文案**（兼容 IG 海外用户）
- **AI 生图模型 prompt 不想自己写**（MJ / GPT-Image-2 / Seedream 5.0 等 11 个）

## ❌ 何时不要使用

- 纯商业品牌投放（不是真实体验种草）
- 不涉及旅游目的地的纯情感文案
- 非中文/英文市场（如阿拉伯语、日语）

---

## 💡 关键能力

| 能力 | 文档 |
|---|---|
| 5 种文案风格公式 | [`references/copywriting-formulas.md`](references/copywriting-formulas.md) |
| 4 大平台规范 | [`references/platforms.md`](references/platforms.md) |
| 11 大生图模型 prompt 优化 | [`references/image-models-optimization.md`](references/image-models-optimization.md) |
| 7 个城市完整方案 | [`examples/`](examples/) |
| REST API 服务（4 Provider）| [`scripts/api/server.py`](scripts/api/server.py) |
| 一键安装到 Codex | [`scripts/install.sh`](scripts/install.sh) |
| GitHub 上传 6 步流程 | [`docs/GITHUB_UPLOAD_GUIDE.md`](docs/GITHUB_UPLOAD_GUIDE.md) |
| 真实出图样例 | [`assets/generated-samples/terracotta_cogview3_zhipu_1024.png`](assets/generated-samples/terracotta_cogview3_zhipu_1024.png) |

---

## 🚀 快速上手

```text
在 Codex/Claude Code 输入:
请用 travel-social-content skill 为「敦煌」出 1 份小红书风格内容方案。

或本地 CLI:
bash scripts/install.sh symlink    # 一键安装到 ~/.codex/skills/
python scripts/api/server.py        # 起 REST API 服务（http://localhost:8000）
```

---

## 🔗 关联 Skill

- [`../food-social-content/`](../food-social-content/) —— 同一作者，美食主题版
- [`../travel-and-food-skill/`](../travel-and-food-skill/) —— 旅游+美食合并版（COMBO 模式）

## 📜 版本 / 合规

- License: MIT
- 已实测：Zhipu CogView-3 真实生成兵马俑图
- 遵守《人工智能生成合成内容标识办法》及平台规则

---

> 🏷 **GitHub Topics**: `claude-code` · `codex` · `skill` · `travel` · `social-media` · `xiaohongshu` · `instagram` · `midjourney` · `dall-e` · `openai-gpt-image` · `flux`
