# 🧳 Travel Social Content

> 一份旅游目的地 → 完整社媒方案的「开箱即用」Skill。
> 给一个景点名，输出一份可直接发的小红书 / Instagram / 朋友圈 / 微博内容方案。

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Platform: Codex Skill](https://img.shields.io/badge/Platform-Codex%20%2F%20Claude%20Code%20Skill-blueviolet)](SKILL.md)
[![No External API](https://img.shields.io/badge/API-None%20Required-brightgreen)](#-零依赖)
[![Version: v1.0](https://img.shields.io/badge/Version-v1.0.0-orange)](docs/CHANGELOG.md)

---

## ✨ 这是什么

传统旅游社媒方案要花 3-5 小时查资料、写文案、磨 prompt、调排版。  
本 Skill 把这条流水线压缩到 **2-5 分钟**：输入景点名 → 输出一份含「6 段文案 + AI 生图 Prompt + 标签 + 发布时间」的 Markdown 方案。

**核心卖点**：
- 🎯 **零外部 API** — 全部走宿主平台（Codex / Claude Code）的内建 web 搜索、网页抓取和图像生成能力
- 🗺️ **5 种文案风格** — 系列打卡 / 情绪共鸣 / 反差吸引 / 数字攻略 / 沉浸脚本
- 📱 **4 大平台适配** — 小红书 / Instagram / 朋友圈 / 微博
- 🖼️ **AI 生图 Prompt** — 每个景点 2-3 套英文 prompt，可直接喂 Midjourney / DALL-E / 即梦 / 豆包 / Stable Diffusion
- 📚 **可缓存参考** — 8 大景点档案已收录，重复调用秒回

---

## 🚀 快速上手

### 在 Codex / Claude Code 中使用

```text
请用 travel-social-content skill 为「西双版纳」出一份小红书风格内容方案。
```

或者手动加载：
```text
请阅读 SKILL.md 并按其 7 步流程生成「敦煌」的多平台方案。
```

### 作为 Prompt Template 复制使用

1. 打开 [`SKILL.md`](SKILL.md)
2. 复制「标准执行流程」整段
3. 粘贴到你常用的 AI 助手，作为系统提示
4. 输入任意城市名即可

---

## 📦 仓库结构

```
travel-social-content/
├── SKILL.md                       # ⭐ Skill 主入口（必读）
├── README.md                      # GitHub 项目说明
├── LICENSE                        # MIT 协议
├── references/
│   ├── destinations.md            # 速查档案（8 大景点）
│   ├── platforms.md               # 平台格式规范
│   ├── copywriting-formulas.md    # 5 种文案公式
│   ├── image-prompts-cheatsheet.md # AI 生图速查
│   └── output-template.md         # 输出章节模板
├── examples/
│   ├── leshan-output.md           # 实测样例：乐山
│   ├── yibin-output.md            # 实测样例：宜宾
│   └── sichuan-output.md          # 8 大景点合集样例
├── scripts/
│   ├── search-destination.sh      # 命令行搜索目的地
│   └── make-output.sh             # 一键组装最终方案
├── assets/
│   └── reference-images/          # 静态资源（占位）
└── docs/
    ├── CHANGELOG.md               # 变更日志
    └── ROADMAP.md                 # 路线图
```

---

## 📚 文档导航

| 文档 | 何时读 |
|---|---|
| [SKILL.md](SKILL.md) | 上手前必读 |
| [references/destinations.md](references/destinations.md) | 看哪些景点已有速查档案 |
| [references/platforms.md](references/platforms.md) | 要在哪个平台发布 |
| [references/copywriting-formulas.md](references/copywriting-formulas.md) | 想换风格模板 |
| [references/image-prompts-cheatsheet.md](references/image-prompts-cheatsheet.md) | 想调 AI 生图参数 |
| [references/output-template.md](references/output-template.md) | 想自定义输出结构 |
| [examples/leshan-output.md](examples/leshan-output.md) | 看完整输出长什么样 |

---

## 🧪 3 个真实样例

| 目的地 | 样例 | 输出 |
|---|---|---|
| 乐山 | [`leshan-output.md`](examples/leshan-output.md) | 6 个子景点 + 3 种风格文案 + 6 段 AI prompt |
| 宜宾 | [`yibin-output.md`](examples/yibin-output.md) | 5 种文案风格全套 + 美食/夜景/文化覆盖 |
| 四川 8 大景点 | [`sichuan-output.md`](examples/sichuan-output.md) | 数字攻略型 + 反差吸引型合集 |

---

## 🛠 扩展用法

### 1. 配合 Codex 内置生图

```text
用 travel-social-content 出九寨沟方案，然后用生成的 prompt 真去生 3 张图。
```

### 2. 系列化内容生产

```text
用 travel-social-content 出一个「中国国家公园巡游」系列：
- 四川·稻城亚丁
- 云南·香格里拉
- 西藏·林芝
```

### 3. 跨平台一次性输出

```text
用 travel-social-content 为「北京」出 **小红书 + Instagram + 朋友圈 + 微博** 4 个版本。
```

---

## 🛡️ 零依赖说明

本 skill **不调用任何第三方付费 API**：
- ✅ Web 搜索 → Codex / Claude 内建工具
- ✅ 网页抓取 → 内建工具（fetch / web_fetch）
- ✅ 文本生成 → 大模型原生能力
- ✅ 图片生成 → 宿主平台的 image generation（如可用）

可选升级路径（贡献者可扩展）：
- 🔧 OpenAI / Anthropic / DeepSeek 文本 API（用于本地 Python 脚本化）
- 🔧 DALL-E / Stable Diffusion API（用于自动批量生图）
- 🔧 DuckDuckGo / SerpAPI 离线搜索

---

## 🤝 贡献指南

欢迎贡献！具体方式：

1. **追加景点速查档案** → 编辑 [`references/destinations.md`](references/destinations.md)
2. **新增样例输出** → 在 [`examples/`](examples/) 添加 `<城市>-output.md`
3. **优化 Prompt** → 编辑 [`references/image-prompts-cheatsheet.md`](references/image-prompts-cheatsheet.md)
4. **提交 Issue** → 报告 bug / 提议功能

### PR Checklist
- [ ] 参考资料文件更新了对应速查
- [ ] examples/ 增加了真实可用的输出样例
- [ ] CHANGELOG.md 增加了一条变更记录
- [ ] SKILL.md 中相关字段同步更新

---

## 📜 License

MIT License © 2026 — 你可以在保留版权声明的前提下自由使用、商用、二次分发。

详细条款见 [LICENSE](LICENSE)。

---

## 🙏 致谢

- 设计灵感来自扣子（Coze）平台的 skill 体系
- 输出参考自小红书 / 抖音 / 马蜂窝的真实爆款
- 遵守中国《人工智能生成合成内容标识办法》及《广告法》相关条款

> **本项目所有内容由 AI 协作生成，使用与传播时请遵循相关法律法规及平台规则。**
