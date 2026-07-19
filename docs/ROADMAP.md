# Roadmap · 路线图

> 本项目未来 6 个月的发展方向。所有条目欢迎 PR 加速推进。

---

## 🎯 v1.1（短期 · 1-2 个月内）

- [ ] **扩展速查档案到 30+ 中国城市 + 20+ 国外热门**
- [ ] **新增 5 个 AI 生图平台适配**（Midjourney v7 / FLUX / GPT-4o / Imagen 4 / CogView）
- [ ] **新增 1 种输出形态：60-90s 抖音口播脚本**（含 BGM 标记与节奏卡点）
- [ ] **新增「出境游签证 + 时差 + 货币」3 速查表**（提升海外场景实用性）
- [ ] **scripts/ 增加 `validate-output.sh`**：自动检查输出是否满足 `output-template.md` 的 7 项自检清单
- [ ] **examples/ 扩到 6 个城市示例**（增加西安/北京/厦门/敦煌）

## 🎯 v1.2（中期 · 3-4 个月）

- [ ] **Docker / docker-compose 支持**（一键启动本地 LLM + 工具链）
- [ ] **GitHub Actions CI**：每次 PR 自动跑 7 项输出自检
- [ ] **新增 interactive-output.md**：用户可在 prompt 中通过下拉菜单选择风格
- [ ] **语言 i18n**（English README + 英文样例 1 个）
- [ ] **增加 1 个 `templates-and-styles/` 目录**：按「亲子 / 情侣 / 独行 / 老友」人群分风格
- [ ] **Twitter 平台适配**（高压缩 + 长 caption 风格）

## 🎯 v2.0（长期 · 6 个月 +）

- [ ] **拆分子技能**（monorepo 化）：
  - `travel-search-bot/`（景点资讯 + 价格 + 实时性）
  - `travel-content-writer/`（多平台文案生成）
  - `travel-image-prompt/`（AI 生图 Prompt 模板库）
  - `travel-publisher-bot/`（内容发布到各平台）
- [ ] **集成 MCP（Model Context Protocol）**：开放给 Claude Desktop / Cursor / Windsurf 等
- [ ] **开放 API**：将 references/ 数据对外提供 JSON 索引
- [ ] **SaaS 化探索**：在保留开源前提下，提供托管服务（自动同步价格、季节性数据）
- [ ] **贡献者激励**：累计 5 个 PR 以上可加入 Maintainers 团队

---

## 🤝 贡献优先级

想参与但不知道从哪开始？从这里选：

| 任务类型 | 难度 | 影响 |
|---|---|---|
| 给 `references/destinations.md` 加 1 个城市 | 🟢 简单 | 🟢 低（但基础） |
| 给 `examples/` 加 1 个完整示例 | 🟡 中等 | 🟡 中 |
| 给 `references/image-prompts-cheatsheet.md` 加新平台参数 | 🟡 中等 | 🟡 中 |
| 给 `scripts/` 写一个新工具 | 🔴 难 | 🟠 高 |
| 给 SKILL.md 主流程提优化建议 | 🟡 中等 | 🟠 高 |

---

## 🧪 实验性功能

下面这些功能在 v1 还没做，但希望尝试，欢迎共建：

- 🎬 **视频脚本可视化**：将 60s 脚本自动转成 storyboard 文字版
- 🎵 **BGM 智能推荐**：根据情绪关键词匹配版权免费 BGM
- 📅 **日历联动**：自动适配国家节假日 / 二十四节气，给出"今天发什么"
- 🗺️ **路线规划**：集成高德/Google Maps，输出交通节点图
- 💬 **评论话术生成器**：针对热门评论生成专业回复模板
- 📊 **数据回流**：用户发布后回填数据（点赞 / 收藏），优化 Prompt

---

## ❌ 不打算做的事

为了聚焦，以下方向明确**不做**：

- ❌ 用户账号代运营（涉及平台规则风险）
- ❌ 内容搬运 / 抄袭（违反《著作权法》）
- ❌ 真实景区票务代购（涉及合规与责任）
- ❌ 跨境支付（涉及金融服务资质）
- ❌ AI 假图生成（明确要求 `AI生成` 标识，避免歧义）

---

> 本路线图每季度评审一次，欢迎在 Issue 中投票调整。
