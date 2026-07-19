# Changelog

本项目所有重要变更记录在此。格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/)。

---

## [v1.0.0] - 2026-07-19

### ✨ 新增 (Added)

- **首个公开发布版本**
- 核心 Skill 入口：`SKILL.md`（标准 frontmatter + 7 步流程）
- 5 种文案风格模板（系列打卡 / 情绪共鸣 / 反差吸引 / 数字攻略 / 沉浸脚本）
- AI 生图 Prompt 速查手册（10 个四川景点模板）
- 4 大平台格式规范（小红书 / Instagram / 朋友圈 / 微博）
- 输出标准化模板（output-template.md）
- 速查档案：8 大四川景点 + 12 个中国城市 + 5 个国外区域
- 3 个完整输出样例（乐山 / 宜宾 / 四川 8 合集）
- 2 个辅助脚本（search-destination.sh + make-output.sh）
- GitHub-friendly README + MIT LICENSE

### 📦 文件清单

```
travel-social-content/
├── README.md (173 行)
├── LICENSE (MIT)
├── SKILL.md (249 行)
├── references/
│   ├── destinations.md (163 行)
│   ├── platforms.md (201 行)
│   ├── copywriting-formulas.md (266 行)
│   ├── image-prompts-cheatsheet.md (256 行)
│   └── output-template.md (211 行)
├── examples/
│   ├── leshan-output.md (364 行)
│   ├── yibin-output.md (287 行)
│   └── sichuan-output.md (346 行)
├── scripts/
│   ├── search-destination.sh
│   └── make-output.sh
├── assets/
│   └── reference-images/ (占位)
└── docs/
    ├── CHANGELOG.md (本文件)
    └── ROADMAP.md
```

**总代码量**：2,898 行（含脚本）

### 🔧 技术决策

1. **零外部 API**：全部走宿主平台（Codex / Claude Code）内建能力
2. **可选 CLI 升级**：`scripts/` 提供 Python 脚本化路径，但不强制
3. **数据可缓存**：`references/destinations.md` 中已收录地点 30s 完成方案
4. **发布合规**：所有 AI 生成内容均带「AI 协作生成」标识



### 🔧 v1.0.1（增量更新 · 2026-07-19）

**新增**：11 大图像生成模型的专项优化指南

- 新文件 `references/image-models-optimization.md`（723 行）
  - 速查表：11 模型 × 6 维度（强项/短板/长度/场景）
  - 每个模型独立章节：定位 / 优势 / 短板 / Prompt 公式 / 参数体系 / 最佳实践 / 禁忌 / 兵马俑对比示例
  - 跨模型对比：3 个经典景点（兵马俑 / 月牙泉 / 洱海）× 11 模型
  - 兼容性矩阵 + 决策树
  - 11 个模型官方文档链接
- 更新 `references/image-prompts-cheatsheet.md`：顶部加「延伸阅读」指针
- 更新 `SKILL.md` Step 5：引用新指南
- 更新 `README.md`：特性列表新增 11 模型支持说明

**涉及模型**：GPT Image 2 (OpenAI)、Gemini 3 Pro Image (Google)、Gemini 3.1 Flash Image (Google)、Seedream 5.0 (字节跳动)、FLUX 2 Max (Black Forest Labs)、Hunyuan Image 3.0 (腾讯混元)、Qwen-Image 2.0 (阿里 Qwen 团队)、通义万相 (阿里另一产品线)、GLM-Image (智谱)、**MiniMax-Image-01** (MiniMax)、文心一格 2.0 (百度)

---

## [Unreleased] - 未来

请查看 [ROADMAP.md](ROADMAP.md)。

---

## 版本兼容说明

- **v1.x**：保持向后兼容，主要扩 `references/` 与 `examples/`
- **v2.0+**：可能调整 `SKILL.md` 主流程，请关注 README
