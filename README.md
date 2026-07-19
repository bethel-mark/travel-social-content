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
- 🎯 **11 大模型专项优化** — 为 GPT Image 2 / Gemini 3 Pro & Flash / Seedream 5.0 / FLUX 2 Max / Hunyuan 3.0 / Qwen-Image 2.0 / 通义万相 / GLM-Image / MiniMax-Image-01 / 文心一格 2.0 各写了针对性 prompt 公式 + 参数体系 + 对比示例。详见 [`references/image-models-optimization.md`](references/image-models-optimization.md)
- 📚 **可缓存参考** — 8 大景点档案已收录，重复调用秒回
- 🌐 **REST API** — 内置 FastAPI 服务，HTTP 调用、批量、CI 集成都开箱即用
- 🐳 **Docker 部署** — docker compose up 一键起，没有 Python 环境也能跑

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

## 🧪 6 个真实样例（共 2246 行完整方案）

| 主题 | 目的地 | 样例 | 体量 | 主题亮点 |
|---|---|---|---|---|
| 🏔️ 美食城市 | 乐山 | [`leshan-output.md`](examples/leshan-output.md) | 364 行 | 大佛 + 跷脚牛肉 + 嘉阳小火车 |
| 🍲 文化古城 | 宜宾 | [`yibin-output.md`](examples/yibin-output.md) | 287 行 | 5 种风格全覆盖 + 美食 + 酒文化 |
| 🌸 大盘省份 | 四川 8 大景点 | [`sichuan-output.md`](examples/sichuan-output.md) | 346 行 | 反差吸引型合集 + 8 期连载 |
| 🏛️ 历史古都 | **西安** | [`xian-output.md`](examples/xian-output.md) | **482 行** | 兵马俑 + 大唐不夜城 + 华山 |
| 🏜️ 沙漠丝路 | **敦煌** | [`dunhuang-output.md`](examples/dunhuang-output.md) | **369 行** | 莫高窟 + 鸣沙山 + 雅丹 |
| 🌊 文艺疗愈 | **大理** | [`dali-output.md`](examples/dali-output.md) | **398 行** | 洱海环湖 + 苍山 + 三塔 |


---

## 🌐 REST API 服务（可选）

如果你想给这个 Skill 加一层 HTTP 接口，方便接 CI / Notion / Slack bot：

```bash
# 一键启动
cp .env.example .env && vim .env       # 至少填 1 个 LLM key
docker compose up -d                    # http://localhost:8000

# 或者本地直接跑
pip install -r requirements-api.txt
export ANTHROPIC_API_KEY=sk-ant-xxx     # 或 OPENAI / DEEPSEEK
python scripts/api/server.py
```

**API 端点**（完整 Swagger 见 `http://localhost:8000/docs`）：
- `GET /health` — 健康检查
- `POST /api/v1/generate` — 核心生成端点，支持 platform / style / secondary_styles
- `GET /api/v1/destinations` — 速查城市列表

**两种运行模式**：
- 🟢 配了 LLM key → 自动返回完整 Markdown
- 🟡 没收 key → 返回拼好的 prompt 字符串，复制到任意 AI 助手

详见 [`scripts/api/README.md`](scripts/api/README.md) · 测试用例 [`examples/api-curl.sh`](examples/api-curl.sh)

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
