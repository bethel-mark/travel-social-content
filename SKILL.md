---
name: travel-social-content
description: >
  生成旅游目的地社交媒体内容方案。当用户希望为某个旅游城市/景点产出可直接发布的小红书、Instagram、朋友圈、微博等平台的图文或视频脚本时调用本 skill。输入景点或城市名（可附平台与风格偏好），自动搜索爆款文案、提炼热门标签、生成 5 种风格的中英文对照文案与 AI 生图 Prompt、给出发布时间与互动话术建议，并输出可复制粘贴的最终方案 Markdown。 触发词：旅游社媒、旅行文案、目的地文案、城市文案、travel social。 Use when 用户要求为旅游目的地生成社媒文案（小红书/IG/微博）。
---

# 🧳 Travel Social Content · 旅游社媒内容生成

> 一句话定位：**给一个景点名，输出一份可直接发的小红书 / IG / 朋友圈 / 微博内容方案**。

本 skill 强调「**不依赖外部 API**」：网页搜索 / 信息抓取 / 图片生成全部走宿主平台（Codex / Claude Code）内建能力，开箱即用、零配置。

---

## ✅ 何时调用

- 用户说：「帮我做一份 XX 市的社媒方案」「给九寨沟出个 9 宫格小红书」「稻城亚丁 IG Reel 脚本怎么写」
- 用户甩一张景点图或一个地点名，希望输出图文 + AI prompt + 标签组合
- 用户要做**系列化**旅游内容（如「我的中国城市巡游」「川西小环线」）
- 用户希望借鉴已有爆款，生成差异化内容

## ❌ 何时**不要**调用

- 纯商业广告 / 品牌种草文（不是真实体验种草）
- 不涉及旅游目的地的纯情感文案 / 朋友圈日常
- 用户只要简短问答（如「九寨沟门票多少」），直接答即可，不必出方案

---

## 📥 输入约定

Skill 接受以下输入（缺失部分会用合理默认值）：

| 字段 | 必填 | 默认值 | 说明 |
|---|---|---|---|
| `目的地` | ✅ | — | 城市名 / 景点名（如「稻城亚丁」「宜宾市」） |
| `平台` | ❌ | `小红书` | `小红书 / Instagram / 朋友圈 / 微博 / 全平台` |
| `风格` | ❌ | `情绪共鸣型` | 5 种风格见下文 |
| `张数` | ❌ | `6` | AI 生图数量（1-9） |
| `真实参考` | ❌ | — | 用户提供的参考图 URL 或文字描述（可选） |

---

## 🧭 标准执行流程（7 步）

### Step 1 · 解析输入
- 提取目的地、平台、风格、张数
- 若目的地在 [`references/destinations.md`](references/destinations.md) 中存在速查档案 → **直接读取缓存**，仅做差异补充
- 若不在 → 进入 Step 2 全量搜索

### Step 2 · 搜索 4 类信息
通过宿主 web 搜索/抓取能力并行获取：

1. **景点基本信息**：地理位置、最佳季节、门票、开放时间、游玩时长
2. **爆款文案**：小红书 / 抖音 / 马蜂窝 上同目的地的标题套路与高频情绪词
3. **热门标签**：目的地相关标签 + 城市/省份大词 + 季节词 + 情绪词
4. **视觉参考**：标志性景观（机位、构图、光线）+ 真实图片链接（用于 Prompt 校准）

### Step 3 · 拆解 3-6 个代表性打卡点
- 一个目的地通常产出 **3-6 个** 子景点（如乐山：大佛 / 峨眉山 / 跷脚牛肉 / 苏稽古镇 / 嘉阳小火车 / 张公桥）
- 每个子景点需覆盖：自然 / 人文 / 美食 / 夜景 / 季节限定 至少 2 种类型
- 子景点列表写入最终方案的「景点详细方案」章节

### Step 4 · 生成 5 种风格的文案矩阵
详见 [`references/copywriting-formulas.md`](references/copywriting-formulas.md)：

| 风格 | 钩子结构 | 适用情绪 |
|---|---|---|
| **A. 系列打卡型** | Day1 / Day2 / 单点多图 | 实用、收藏型 |
| **B. 情绪共鸣型** | 名句 + 抒情短句 | 文青、治愈 |
| **C. 反差吸引型** | 「以为 X / 结果 Y」 | 悬念、反转 |
| **D. 数字攻略型** | 「8 大秘境」/「3 天 2 夜」 | 攻略、清单 |
| **E. 沉浸式白描** | 60 秒分镜脚本 | 视频号/抖音 |

每次至少生成 **3 种风格**（默认 A + B + C），按需叠加 D / E。

### Step 5 · 生成 AI 生图 Prompt 套件
每个子景点输出：
- **主图 Prompt**：最具视觉冲击力的标志性画面（英文）
- **备用 Prompt ×1-2**：人物/夜景/季节限定等差异化变体
- 全部 prompt 必须可**直接粘贴**到 Midjourney / DALL-E / 即梦 / 豆包 / Stable Diffusion，附参数建议 `--ar / --s / --v`

详见两份 references：
- 通用/MJ/DALL-E/即梦/SDXL 见 [`references/image-prompts-cheatsheet.md`](references/image-prompts-cheatsheet.md)
- 11 大模型（GPT Image 2 / Gemini 3 Pro / Gemini 3.1 Flash / Seedream 5.0 / FLUX 2 Max / Hunyuan 3.0 / Qwen-Image 2.0 / 通义万相 / GLM-Image / MiniMax-Image-01 / 文心一格 2.0）见 [`references/image-models-optimization.md`](references/image-models-optimization.md)

### Step 6 · 平台适配
依据 [`references/platforms.md`](references/platforms.md) 中各平台字数 / 标签 / 排版 / 时间规范，输出对应平台版本：
- 小红书：6-9 张同色系拼图 + 标题 12-18 字 + 20 个标签
- Instagram：英文 Reel 旁白 + 3 张 carousel + 30 个 hashtag
- 朋友圈：1 张封面 + 6-9 张九宫格 + 单段文字
- 微博：140 字以内 + 5-10 个 #话题# + @提及

### Step 7 · 输出方案
套用 [`references/output-template.md`](references/output-template.md) 的章节顺序，整合输出。可直接保存为 `examples/<目的地>-output.md`。

---

## 📐 输出结构（强制）

最终 Markdown 必须包含以下章节（缺失即视为输出不完整）：

```
# <城市/景点名> 旅游社交媒体内容方案

## 📌 目的地简述            # 1 段 80 字以内总览
## 🏞️ 景点详细方案          # 3-6 个子景点 × 6 字段
   ## 1. <子景点名>
      - 📝 文案参考
      - 🎨 图片风格建议
      - 🖼️ AI 生图提示词（中英双语，可选）
      - 📱 小红书风格模板（3 种）
      - 📋 实用信息速查表
      - ✨ 视觉元素特写（可选）
## 📢 发布建议              # 封面图 / 标题 / 标签 / 时间
## 📈 热门趋势分析          # 3-5 条
## 🔗 参考来源              # 5-8 条链接（编号）
```

完整示例：
- [`examples/leshan-output.md`](examples/leshan-output.md)
- [`examples/yibin-output.md`](examples/yibin-output.md)
- [`examples/sichuan-output.md`](examples/sichuan-output.md)

---

## 🎚️ 5 种文案风格速查

### A · 系列打卡型
```
📍<城市>
第①站·<景点A>  <情绪钩子> 📸
·
📍<城市>
第②站·<景点B>  <情绪钩子> 📸
·
#<城市旅游> #<景点A> #<景点B>
```

### B · 情绪共鸣型
```
总要去趟<城市>吧
看看<A>，<情绪短句> 💙
吹吹<B>的<风/雨>，<抒情> 🌬️
走在<C>，眼睛在天堂
```

### C · 反差吸引型
```
以为<刻板印象>
直到我看见了这些 👇
-
<A>，<反差金句>
<B>，<反差金句>
-
<城市>，远比你想象的更<美/野/治愈>
```

### D · 数字攻略型
```
<城市><天数><玩法>攻略｜人均<预算>
────────────────
✓ <必玩点>
✓ <必吃>
✓ <必拍>
⚠️ <避坑>
────────────────
#<城市旅游> #<数字>天<数字>夜
```

### E · 60 秒沉浸白描（脚本）
```
[0-3s]   黑屏字幕：<钩子>
[3-10s]  高能镜头快剪 + BGM
[10-30s] 中段沉浸（每镜 < 5s）
[30-50s] 实用干货（字幕条）
[50-60s] 互动钩子 + 封面 CTA
```

---

## 🖼️ AI 生图 Prompt 通用结构

```
[主体] + [环境/季节/天气] + [光线/色调] + [构图/视角] + [风格/参考] + [参数]
```

**模板**：
```
<Subject> in <Setting> during <Season/Time>,
<Lighting/Color Palette>, <Composition/Camera>,
<Style Reference>, 8K ultra detail.
--ar <3:2|9:16|16:9> --style raw --v 6.2
```

**禁忌**：
- ❌「a photo of」（触发 NSFW 过滤）
- ❌ 版权特定人物 / 商标
- ❌「perfect」（过度抽象）
- ✅ 使用「photorealistic / cinematic / film grain / golden hour」等可量化短语

---

## 🛡️ 边界与限制

- **票价/开放时间**可能过时，需提醒用户「出行前再次核实」
- **AI 生图**可能产出不一致的细节（人脸畸变、文字错乱），建议配「后期微调」提示
- **不要照抄**第三方爆款文案，保持 ≥30% 改写度以避免平台限流
- 必须遵守中国《人工智能生成合成内容标识办法》：AI 图发布时建议带 `#AI生成` 标签

---

## 📁 项目结构

```
travel-social-content/
├── README.md                      # GitHub 项目说明
├── LICENSE                        # MIT
├── SKILL.md                       # ← 你正在读
├── references/
│   ├── destinations.md            # 8 大景点速查档案
│   ├── platforms.md               # 4 大平台格式规范
│   ├── copywriting-formulas.md    # 5 种风格公式库
│   ├── image-prompts-cheatsheet.md # AI 生图参数速查
│   └── output-template.md         # 标准输出章节模板
├── examples/
│   ├── leshan-output.md           # 乐山实测样例
│   ├── yibin-output.md            # 宜宾样例
│   └── sichuan-output.md          # 四川 8 大景点集合样例
├── scripts/
│   ├── search-destination.sh      # 命令行检索目的地信息
│   └── make-output.sh             # 一键组装最终方案
├── assets/
│   └── reference-images/          # 静态参考图（占位）
└── docs/
    ├── CHANGELOG.md
    └── ROADMAP.md
```

---

## 🧪 测试用例

| 目的地 | 平台 | 风格 | 样例 |
|---|---|---|---|
| 乐山市 | 小红书 | 系列打卡型 + 情绪共鸣型 + 反差吸引型 | [`examples/leshan-output.md`](examples/leshan-output.md) |
| 宜宾市 | 多平台 | 全 5 种风格 | [`examples/yibin-output.md`](examples/yibin-output.md) |
| 四川（8 大景点合集） | 小红书 | 反差吸引型 + 数字攻略型 | [`examples/sichuan-output.md`](examples/sichuan-output.md) |

---

> **本 skill 由 Codex 协作设计，遵守中国《人工智能生成合成内容标识办法》使用与传播。**
