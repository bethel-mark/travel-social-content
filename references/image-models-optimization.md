# 🎨 11 大图像生成模型 · 专项优化指南

> 通用准则（公式、禁忌、推荐词、英文 prompt 模板）见 [`image-prompts-cheatsheet.md`](image-prompts-cheatsheet.md)。  
> **本文件专注：** 用户级使用跨境 / 国产 11 大模型时的**模型特性差异** + **针对性优化策略** + **同一景点的对比示例**。

---

## 📋 速查表（11 个模型 × 6 维）

| # | 模型 | 厂商 | 强项 | 短板 | 推荐 prompt 长度 | 适用场景 |
|---|---|---|---|---|---|---|
| 1 | **GPT Image 2** | OpenAI | narrative 场景理解 / 推理增强 | 易向"摄影"靠拢 | 50-150 字 | 复杂场景、写实风 |
| 2 | **Gemini 3 Pro Image** | Google | 多模态 + 长 prompt + 文字渲染 | 风格化有时过重 | 100-300 字 | 排版、海报、复杂指令 |
| 3 | **Gemini 3.1 Flash Image** | Google | 速度 × 5 + 成本低 | 细节弱于 Pro | 80-200 字 | 批量 A/B 测试 |
| 4 | **Seedream 5.0** | 字节跳动 | **中文 prompt 极致** + 东亚人脸 | 西方场景略弱 | 60-150 字（中文）| 中国风、人物真实 |
| 5 | **FLUX 2 Max** | Black Forest Labs | prompt fidelity 最高 + typography | 需要长且细的 prompt | 200-500 字 | 排版 / Logo / 写实 |
| 6 | **Hunyuan Image 3.0** | 腾讯混元 | 国风水墨 + 中国元素 + 多镜头 | 国际化场景中等 | 80-200 字（中文）| 古风、仙侠、文物 |
| 7 | **Qwen-Image 2.0** | 阿里 Qwen 团队 | 文字渲染 + 中文排版 + 开源 | 风格化强项弱 | 60-150 字（中文）| 海报、长文字 |
| 8 | **通义万相** | 阿里另一产品线 | 中文 + 商业设计 + 海报 | 写实细节弱于 MJ | 80-200 字（中文）| 商业海报、品牌 |
| 9 | **GLM-Image** | 智谱 | 多模态理解 + 中文字渲染 | 场景复杂时略抽象 | 60-150 字（中文）| 中文场景 |
| 10 | **MiniMax-Image-01** | MiniMax | 影视级美术 + 复杂场景 + 中英双语 | 部分中文细节待提升 | 50-200 字 | 电影感 / 史诗场景 |
| 11 | **文心一格 2.0** | 百度 | 中文 + 中国元素 | 国际场景较弱 | 80-180 字（中文）| 国潮、东方美学 |

---

## 🎓 跨 11 个模型的通用准则

虽然每个模型有差异，但 3 条原则通用：

### 1. 结构化你的 prompt（结构 > 关键词堆叠）
```
[主体 + 数量 + 状态] + [环境/季节/天气] + [光线/色调] + [构图/视角] + [风格/参考] + [技术参数]
```

### 2. 始终是「自然句子」而非「标签清单」（除了 Seedream）
**坏**：`cinematic, 8k, dramatic, gold light, mountains, snow`  
**好**：`Mount Hua (Xiyue) at sunrise, viewed from the West Peak summit, with a sea of clouds rolling beneath the ridge and an exploding red horizon.`

### 3. 始终给出**风格参考**
永远别让模型"猜你想要什么风格"。明确写：
- 摄影：`cinematic photography, National Geographic style, 35mm film grain`
- 国风：`Chinese ink wash, traditional long-scroll painting style`
- 插画：`digital illustration, Studio Ghibli, soft palette`

---

## 1️⃣ GPT Image 2（OpenAI）

### 一句话定位
**OpenAI 的图像生成最新旗舰，靠 o 系列推理内核增强 prompt 理解。**

### 核心优势
- **最强 narrative 理解**：把"一个场景故事"塞进去，它能拆成画面
- **真实感 default**：默认偏电影摄影，**不太会"硬拗"成插画**
- **多步骤推理**：含 `think` 的复杂场景也能拆解
- **与 GPT 文本模型联动**：可以"先用 GPT 写场景、再生成图"的工作流

### 典型短板
- 风格化（动漫、油画）有时偏弱，会偷偷"美化"成摄影
- 文字渲染中等（不如 Gemini / Qwen）
- 长 prompt（> 200 字）效果衰减

### 针对性 Prompt 公式
```
[一个完整场景描述，包括谁、在哪、做什么、看到什么、感受如何]，
[摄影/绘画风格参考]，[光线 + 色调 + 视角]，
[技术参数：aspect + 质感]
```

**关键差异**：
- ✅ 用**完整句子**写场景
- ❌ **不要 keyword stuffing**（"8k, cinematic, dramatic, masterpiece, trending"）
- ✅ 像写 mini 剧本那样写 prompt

### 参数体系
| 参数 | 取值 |
|---|---|
| `size` | `1024x1024`、`1024x1536`（竖）、`1536x1024`（横）|
| `quality` | `low` / `medium` / `high` / `auto` |
| `background` | `transparent`（仅 API） / `auto` |
| `n` | 1-4（一次几张）|

> GPT Image 2 当前**未公开 n>1 参数到 image generation endpoint**，单次 1 张。

### 最佳实践
1. ✅ 把"主体 + 动作 + 环境 + 情绪"讲成**故事**
2. ✅ 给出 1-2 个**风格参考锚点**（如 `in the style of Annie Leibovitz portraiture`）
3. ✅ 光线要从**物理角度**描述（晨光 / 黄昏 / 散射 / 侧光）
4. ✅ 写英文（中文效果差一档）
5. ❌ 避免"8K, ultra-detailed, masterpiece, trending on artstation"等 tags

### 禁忌事项
- ❌ 不要堆叠风格词汇（MUST 直接选定 1 个）
- ❌ 不要"perfect"（GPT Image 2 会把 perfect 字面执行）
- ❌ 不要写"photorealistic"（与默认冲突，会输出冗余）
- ❌ 避免人名（肖像权）

### 针对「兵马俑」的优化示例
❌ 通用 Midjourney 式 prompt：
```
Pit No.1 of the Terracotta Army, hundreds of clay warriors, 
dramatic single shaft of light, museum editorial, photorealistic, 8k
--ar 3:2 --style raw --v 6.2
```

✅ GPT Image 2 优化版（叙事化 + 单句长描述）：
```
A documentary photograph inside Pit No.1 of the Terracotta Army 
Museum in Xi'an, Shaanxi. Hundreds of life-sized Qin Dynasty warriors 
stand in silent battle formation, half-buried in yellow earth. 
A single shaft of morning light falls through a high museum window 
onto the front rank of generals. Their faces are weathered, 
expressions solemn. The atmosphere is reverent and hushed. 
Captured in the style of Annie Leibovitz, shot on medium-format 
film with shallow depth of field, warm earth tones in the 
foreground fading into atmospheric haze in the deep rows.
```
（成段 narrative，约 100 词，比 Midjourney 更长但效果最佳）

---

## 2️⃣ Gemini 3 Pro Image（Google）

### 一句话定位
**Google 的最强多模态生图模型，专长文字渲染、复杂排版、长指令理解。**

### 核心优势
- **最强文字渲染**：海报、Logo、信息图的英文/中文排版
- **多回合理解**：可基于上次生成的图"接着改"
- **长 prompt 衰减最弱**：可用 200-400 字复杂指令
- **Gemini 多模态联动**：可"看图改图"工作流无缝

### 典型短板
- 风格化有时过重（容易"美化"）
- 写实感和 MJ/DALL-E 比略弱
- 默认比例固定（需显式指定 `aspect_ratio`）

### 针对性 Prompt 公式
```
[主体场景描述，约 80-150 字]，
[camera + lighting],
[mood + style reference],
[explicit aspect ratio]
```

**关键差异**：
- ✅ **优先结构化句子**（Gemini 内部就有结构分析）
- ✅ 中英文都极强（最适合国内用户中文出图）
- ✅ **一定要在 prompt 里写 aspect ratio**（如 `aspect_ratio: "16:9"`）

### 参数体系
| 参数 | 格式 |
|---|---|
| `aspect_ratio` | `"1:1"`, `"16:9"`, `"9:16"`, `"4:3"`, `"3:4"` |
| `num_outputs` | 通常 1-4 |
| `prompt` | 可用中英双语 |

### 最佳实践
1. ✅ 把 `aspect_ratio` 写进 prompt 主体或外部 parameter
2. ✅ 复杂场景可以**列 bullet**（Gemini 解析 markdown 结构最好）
3. ✅ 中文 prompt 同样顶，但**带英文摄影术语更稳**
4. ✅ 用于海报 / 信息图时尤其突出（vs 其他模型）

### 禁忌事项
- ❌ 不要超长（> 400 字 prompt 衰减）
- ❌ 不要省略风格（让 Gemini 自由发挥容易过"美化"）
- ❌ 不要大量参数列举（Gemini 会"挑重点"）

### 针对「兵马俑」的优化示例
✅ Gemini 优化版（中英结合 + 结构化）：
```
Render a high-angle editorial photograph of Pit No.1 at the 
Terracotta Army Museum in Xi'an.

Camera: 35mm wide-angle from the second-floor museum walkway.
Composition: rows of Qin-era clay warriors extending into 
atmospheric haze, single natural light shaft from high window 
illuminating the front rank.

Mood: solemn, hushed, reverent. Time of day: 10:00 AM, mid-October.
Palette: earthen ochres, weathered grays, single warm beam.

Style reference: National Geographic archaeology feature, 
Steven Alvarez museum lighting.

aspect_ratio: "3:2"
```

---

## 3️⃣ Gemini 3.1 Flash Image（Google）

### 一句话定位
**Gemini 3 Pro Image 的速度版（~5× 快）、成本约 1/3，适合批量。**

### 核心优势
- **速度 × 5** + **成本 -70%**
- 复杂指令理解**仍强**
- 适合 A/B 测试、批量生成迭代方案

### 典型短板
- 细节保持弱于 Pro（约 80% 质量）
- 文字渲染细节处略模糊
- 写实感弱于 Pro

### 何时用 1.1 Flash
- ✅ 一组 prompt 想试 4-8 个变体
- ✅ 出图量大、希望短时间看效果
- ✅ 内部协作 / 个人小项目

### Prompt 公式
与 Pro **相同**，但：
- **长度可缩短 20-30%**（Flash 对短 prompt 容忍度更高）
- **省略例行修饰词**：直接进主体

### 禁忌
- ❌ 不要用于海报终稿（细节不及 Pro）
- ❌ 不要用于需要文字精确渲染

---

## 4️⃣ Seedream 5.0（字节跳动）

### 一句话定位
**国产出海中 prompt 最强者，中文 prompt 理解的天花板。**

### 核心优势
- **中文 prompt 极致**：白话文也能解析
- **东亚人脸真实感** 国内 SOTA
- **多镜头叙事一致性强**（多张图可保持人脸 / 服装统一）
- 出图快（在线 SaaS）

### 典型短板
- **西方场景薄弱**（需要明确引导）
- 风格化有时过"网红"（审美偏年轻化）
- 极度复杂场景可能"硬凹"

### 针对性 Prompt 公式
```
[中文主体场景描述，150-200 字]，
[摄影/绘画风格]，[光线、色调、构图]，
[技术参数]
```

### 参数体系
| 参数 | 格式 |
|---|---|
| `aspect_ratio` | `"1:1"`、`"3:4"`、`"4:3"`、`"9:16"`、`"16:9"`、`"21:9"` |
| `style` | `写实` / `动漫` / `水墨` / `电影` 等 |
| `seed` | 整数，复现用 |

### 最佳实践
1. ✅ **写中文**（不要写英文！效果差异巨大）
2. ✅ 关键摄影/电影术语可用**英文括号标注**：
   `cinematic style（电影风格）`、`warm sunset（暖色夕阳）`
3. ✅ 对人物/古风场景效果最佳
4. ✅ 多张出图可锁 seed 保一致性

### 禁忌
- ❌ 不要写纯英文 prompt（白白浪费中文优势）
- ❌ 不要堆砌风格标签
- ❌ 不要期待西方明星脸（特征库以东亚为主）

### 针对「兵马俑」的 Seedream 优化示例
✅ **中文 prompt**：
```
秦始皇兵马俑 1 号坑博物馆内景，几百个真人大小的秦代陶俑
军阵静默列队，半埋在黄土中。一束清晨阳光从博物馆高窗射下，
正好打在前列将军俑的面部。表情肃穆，目光深邃，凝视 2200 年。

拍摄于上午 10 点，10 月中旬。色调以土黄、灰陶和温暖的单束
光为主，前列清晰、远处阵列逐渐模糊在大气透视中。

照片风格：电影级博物馆摄影，史蒂文·阿尔瓦雷斯（Steven Alvarez）
式博物馆灯光，宽幅构图 3:2，国家地理考古专题风格。

参数：宽幅 16:9，超清
```

---

## 5️⃣ FLUX 2 Max（Black Forest Labs）

### 一句话定位
**prompt fidelity（保真度）之王，文字渲染 + 复杂构图的天花板。**

### 核心优势
- **指令保真度极高**：能精确实现"左上角 + 右下角 + 中间"这类复杂布局
- **文字渲染顶级**：海报、Logo、信息图最强
- 写实感强

### 典型短板
- 需要**长且细致**的 prompt（短 prompt 效果差）
- 风格化（动漫、水墨）弱于专门模型
- 推理较慢

### 针对性 Prompt 公式
```
[极长叙事，约 200-500 字]，
[详细物理描述：光线、材质、纹理]，
[每个元素位置]，
[风格参考锚点]
```

### 参数体系
| 参数 | 格式 |
|---|---|
| `aspect_ratio` | `"1:1"`, `"16:9"`, `"21:9"`...自由 |
| `raw` | `true` 保持自然效果（不带 MJ 风格化）|
| `num_outputs` | 1-4 |
| `prompt` | 英文最佳，中文亦可但效果稍弱 |

### 最佳实践
1. ✅ **写长 prompt**（200-500 字甚至更长）
2. ✅ 用**精确物理描述**（"晨光从西南方以 45° 角斜射"）
3. ✅ 文字内容**用引号明确括起来**：`a sign that reads "敦煌"`
4. ✅ 适合海报 / 商业设计 / 复杂排版

### 禁忌
- ❌ 短 prompt 出图不稳定
- ❌ 不要对风格化期待过高

---

## 6️⃣ Hunyuan Image 3.0（腾讯混元）

### 一句话定位
**国风水墨 / 中国元素 / 古风场景的国内 SOTA。**

### 核心优势
- **国风水墨**：山水、留白、飞白、墨韵
- **中国元素**（古建筑、汉服、纹样）细节到位
- 中文 prompt 顶级

### 典型短板
- 国际化场景（西方建筑、欧式人物）略弱
- 速度慢

### 参数体系
| 参数 | 说明 |
|---|---|
| `Style` | `写实` / `水墨` / `写意水墨` / `动漫` / `油画` / `二次元` |
| `aspect_ratio` | `"1:1"` `"16:9"` `"9:16"` 等 |

### Prompt 公式
```
[中文主体描述]，
[Style 关键词：水墨/写实/动漫]，
[技术参数]
```

### 最佳实践
1. ✅ 国风 / 古建筑 / 汉服场景必选
2. ✅ 中文字渲染较强（海报字体）
3. ✅ 用明确 `Style: 水墨` 标签

### 禁忌
- ❌ 不要用国际场景（Maya 文明、巴黎建筑会失真）

### 针对「兵马俑」的 Hunyuan 优化示例
✅ 中文 prompt：
```
秦始皇兵马俑 1 号坑博物馆内景，史诗级博物馆摄影。

画面主体：几百个真人大小的秦代陶俑军阵，半埋在黄土中，
形貌各异、神态肃穆。前列将军俑面部被一束来自高窗的清晨阳光
照亮，刻画细腻，2200 年的岁月在他们脸上留下斑驳。

风格：写实摄影 + 国画留白意境结合
色调：以土黄、灰陶为主，前列暖色、远处冷灰色
构图：宽幅 3:2，从博物馆二楼观景台俯拍，前景清晰、远景渐隐

技术参数：8K 超细节，景深中等，电影感

Style: 写实
```

---

## 7️⃣ Qwen-Image 2.0（阿里 Qwen 团队）

### 一句话定位
**Qwen 系列的图像版本，专长中文文字渲染与复杂排版。**

### 核心优势
- **中文字渲染 SOTA**：海报、Logo、广告字
- **复杂排版**：多列、多文字、混排
- **开源可用**：可本地部署

### 典型短板
- 风格化（写意 / 油画 / 动漫）弱于专门模型
- 国际化场景中等

### 参数体系
| 参数 | 说明 |
|---|---|
| `aspect_ratio` | `1:1`、`3:4`、`4:3`、`9:16`、`16:9` |
| `prompt_extend` | `true` 模型自动润色 prompt |
| `negative_prompt` | 负面提示支持 |

### Prompt 公式
```
[中文场景] + [风格参考] + [光线色调]
```

### 最佳实践
1. ✅ **中文字渲染必选**：海报、广告、Logo
2. ✅ 配合 `prompt_extend: true` 让模型自动润色短 prompt
3. ✅ 中文长文字（标语、诗句）排版稳

### 禁忌
- ❌ 不要期待水墨 / 油画这类风格化顶级
- ❌ 不要写超复杂场景

---

## 8️⃣ 通义万相（阿里另一产品线）

### 一句话定位
**偏商业设计的出图，国内海报 + 品牌场景代表。**

### 核心优势
- **海报 / 商业设计**：排版、配色、文字
- 中文场景稳定

### 典型短板
- 写实质感弱于 MJ / DALL-E
- 抽象风格弱

### Prompt 公式
```
[中文场景 + 商业用途关键词：海报 / 广告 / banner]，
[字体描述]，[光线色彩]，
[技术参数]
```

### 最佳实践
1. ✅ 商业海报 / 品牌 banner 强项
2. ✅ 中文字渲染稳
3. ✅ 配 `style: "商业设计"` 显式标签

---

## 9️⃣ GLM-Image（智谱）

### 一句话定位
**GLM 系列的多模态图像版，强中文理解 + 商业可用。**

### 核心优势
- 中文 prompt 强
- 商业可用（API 稳定）
- 中英双语 prompt 都行

### 典型短板
- 风格化中等
- 复杂场景细节中等

### 最佳实践
1. ✅ 中文 prompt 优先
2. ✅ 配 `--style "CINEMATIC"` 或 `"写实"`
3. ✅ 国内 SaaS 集成首选（合规强）

---

## 🔟 MiniMax-Image-01（MiniMax）

### 一句话定位
**MiniMax 的图像生成模型，主打影视级美术质感和复杂叙事场景。**

### 核心优势
- **电影级美术感**：史诗场景、奇幻题材强项
- **复杂叙事场景**：能处理"主角 + 环境 + 戏剧光影"的多元素构图
- **中英双语 prompt** 均强
- 配合 MiniMax 文本模型时**视觉-语义一致性**极佳

### 典型短板
- 中文字渲染（相比 Qwen / 通义万相）稍弱
- 部分中国历史细节（如器物纹样、人物服饰）偶有偏差
- 输出 API 参数请以官方文档最新版本为准

### 针对性 Prompt 公式
```
[主体 + 戏剧性场景描述]，[电影感/史诗感美术参考]，
[光线 + 调色]，[技术参数]
```

### 最佳实践
1. ✅ **史诗 / 奇幻 / 电影分镜场景**优先
2. ✅ **配合 MiniMax-Text-01 文本模型做剧本到画面** 的工作流
3. ✅ 用英文 prompt（中文也有支持，但风格化弱 10-15%）
4. ✅ 强调"cinematic mood"、"dramatic atmosphere"

### 禁忌
- ❌ 不要用于中文文字密集海报（用 Qwen / 通义万相）
- ❌ 涉及具体中国历史服饰时需要明确 prompt 引导

### 针对「兵马俑」的 MiniMax-Image-01 优化示例
✅ 英文 prompt（电影级史诗）：
```
A cinematic wide-angle museum photograph inside Pit No.1 of the 
Terracotta Army in Xi'an. Hundreds of life-sized Qin Dynasty 
warriors stand in silent battle formation, half-emerged from 
yellow loess earth. A single dramatic shaft of late-morning 
sunlight pours through a high museum window, illuminating the 
front rank of generals with weathered expressions. The atmosphere 
is reverent and hushed. Behind them, ten thousand soldiers fade 
into atmospheric haze and shadow.  

Composition: vista style with deep rows of warriors receding into 
haze.  

Color palette: warm ochre foreground, cool gray haze background,
single golden light beam.  

Style: in the mood of Wim Wenders' museum cinematography,
medium-format film grain, National Geographic archaeology feature,
epic scale reverence.

Aspect ratio: 16:9 (cinematic widescreen)
Quality: ultra high detail
```

> 💡 **官方参数说明**：MiniMax-Image-01 的最新 API 参数（如图像尺寸档位、风格强度字段、质量档位、`seed` 复现等）请直接以 [platform.MiniMax.io/skills](https://platform.MiniMax.io) 当日文档为准。本节给出的是基于通用生成模型规律的最佳实践框架。

---

## 1️⃣1️⃣ 文心一格 2.0（百度）

### 一句话定位
**百度文心系列图像产品，国潮 + 东方美学的国内强项。**

### 核心优势
- **国潮 / 中国元素**：敦煌、故宫、龙凤等元素细
- 中文 prompt 解析好
- 国内合规

### 典型短板
- 国际化场景弱
- 写实感弱于 MJ / DALL-E

### Prompt 公式
```
[中文国潮场景描述]，[风格参考：东方美学 / 工笔 / 写意]，
[光线色调]
```

### 最佳实践
1. ✅ 国潮 / 东方题材必选
2. ✅ 中文 prompt 优先

---

## 🔄 跨模型对比示例（同一景点 × 3 案例 × 多模型）

为方便在同一视觉目标下对照 11 个模型的表现差异，给出**3 个经典景点**的多模型并排 prompt：

### 案例 A：兵马俑 1 号坑（史诗博物馆人文）

| 模型 | 优化策略 | Prompt 关键差异 |
|---|---|---|
| MJ v6.2 | keyword + `--ar 3:2 --style raw --v 6.2` | 英文关键词 + 后缀参数 |
| DALL-E 3 | natural language | 完整句子 |
| GPT Image 2 | narrative scene | 故事化描述 |
| Gemini 3 Pro | 中英结合 + aspect_ratio | 结构化段落 |
| Gemini Flash | 简化版 Pro prompt | 可省细节修饰 |
| Seedream 5.0 | 中文为主 | 电影术语括注英文 |
| FLUX 2 Max | 长 prompt（200-500 字） | 物理细节具体 |
| Hunyuan | Style: 写实 + 中文 | 国画留白结合 |
| Qwen-Image 2.0 | `prompt_extend: true` | 中文 + 商用字渲染 |
| 通义万相 | `style: "商业设计"` | 海报场景 |
| GLM-Image | 中文优先 | 合规 SaaS |
| MiniMax-Image-01 | 英文 + cinematic | 戏剧光影 |
| 文心一格 2.0 | 中文国潮 | 工笔 + 写意 |

### 案例 B：敦煌鸣沙山月牙泉（沙漠日出 + 自然奇景）

**英文通用骨架**（所有模型都适用）：
```
[SUBJECT]: Massive crescent-shaped sand dune towering over a 
turquoise crescent oasis lake
[SETUP]: Walking along the dune ridge
[ENVIRONMENT]: Ancient Silk Road atmosphere, vast Gobi plain 
stretching to the horizon
[LIGHT]: Golden hour sunrise, casting long shadows, illuminating 
amber sand
[COMPOSITION]: Cinematic wide-angle, dune in upper 1/3, lake 
in lower-left third, lone camel caravan silhouette on right ridge
[STYLE]: National Geographic photography, 35mm film, muted amber 
palette
[TECH]: 16:9 aspect, photorealistic, 8K ultra detail
```

**针对 Seedream 5.0 中文优化版**（同上骨架的中文翻译 + 关键术语英文）：
```
敦煌鸣沙山月牙泉日出，巨大月牙形沙丘环抱绿松石色的月牙泉，
清晨金色阳光（golden sunrise）斜射沙丘，驼队剪影沿着沙脊
行走，史诗级电影感宽幅（cinematic wide-angle composition），
沙漠辽阔延伸到地平线，暖琥珀色调（amber palette），尼康
D850 + 长焦镜头（telephoto lens）压缩感，国家地理摄影
（National Geographic photography），超清 8K 摄影。
```

### 案例 C：大理洱海环湖（治愈系 + 小清新）

**针对 Qwen-Image 2.0 + 通义万相**（中文 + 海报感）：
```
治愈系晨光海报：大理洱海环湖公路，碧绿湖水如镜面，倒映
苍山十九峰覆雪，湖面雾气飘过，路边一骑行者剪影孤独前行。

文字排版（必须清晰）："在洱海发呆"5 个字，竖排或横排
居中。

色调：青色为主 + 晨光暖金滤镜
风格：治愈系 / 小清新，仿胶片质感
构图：宽幅 16:9，文字在画面右侧 1/3 区域
```

> ⚠️ Qwen-Image 和通义万相在中文海报场景中**文字渲染**是其差异化优势，**务必利用**。

---

## 🧮 兼容性矩阵（按参数维度）

| 模型 | 自定义比例 | 文字渲染 | 风格化 | 速度 | 中文 prompt | 商用授权 |
|---|---|---|---|---|---|---|
| MJ v6.2 | ✅ 全比例 | ❌ 弱 | ⭐⭐⭐⭐⭐ | 慢 | 弱 | 订阅 |
| DALL-E 3 | ⚠️ 三档固定 | ⭐⭐⭐ | ⭐⭐⭐ | 中 | 弱 | API 按量 |
| GPT Image 2 | ⚠️ 三档固定 | ⭐⭐⭐⭐ | ⭐⭐⭐ | 中 | 中 | API 按量 |
| Gemini 3 Pro | ✅ 自定义 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | 中 | ⭐⭐⭐⭐⭐ | Google AI |
| Gemini 3.1 Flash | ✅ 自定义 | ⭐⭐⭐⭐ | ⭐⭐⭐ | 快 | ⭐⭐⭐⭐⭐ | Google AI |
| Seedream 5.0 | ✅ 自定义 | ⭐⭐⭐ | ⭐⭐⭐⭐ | 快 | ⭐⭐⭐⭐⭐ | 火山 / API |
| FLUX 2 Max | ✅ 自定义 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | 慢 | 中 | API 按量 |
| Hunyuan 3.0 | ✅ 自定义 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐（国风）| 慢 | ⭐⭐⭐⭐⭐ | 腾讯云 |
| Qwen-Image 2.0 | ✅ 自定义 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | 中 | ⭐⭐⭐⭐⭐ | 阿里云 + 开源 |
| 通义万相 | ✅ 自定义 | ⭐⭐⭐⭐ | ⭐⭐⭐ | 中 | ⭐⭐⭐⭐⭐ | 阿里云 |
| GLM-Image | ✅ 自定义 | ⭐⭐⭐⭐ | ⭐⭐⭐ | 中 | ⭐⭐⭐⭐⭐ | 智谱 API |
| MiniMax-Image-01 | ✅ 自定义 | ⭐⭐⭐ | ⭐⭐⭐⭐（史诗） | 中 | ⭐⭐⭐⭐ | MiniMax API |
| 文心一格 2.0 | ✅ 自定义 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐（国潮） | 中 | ⭐⭐⭐⭐⭐ | 百度智能云 |

---

## 🌳 决策树：哪个模型最适合我？

```
我想要做什么？
│
├─ 海报 / 商业设计 / 中文文字密集
│     ├─ 中文 → ✅ Qwen-Image 2.0  ⭐ 推荐
│     ├─ 海报构图 → ✅ 通义万相
│     └─ 强文字渲染 → ✅ Gemini 3 Pro Image
│
├─ 史诗 / 电影 / 奇幻场景
│     ├─ 复杂构图 + 戏剧光影  → ✅ MiniMax-Image-01
│     ├─ 极致 narrative 故事感  → ✅ GPT Image 2
│     ├─ 长 prompt 细致保真     → ✅ FLUX 2 Max
│     └─ 国风水墨 / 古风       → ✅ Hunyuan 3.0
│
├─ 写实风光明信片（社交媒体爆款）
│     ├─ 英文 prompt + 极致真实  → ✅ MJ v6.2
│     ├─ 中文 prompt + 东亚人脸  → ✅ Seedream 5.0
│     ├─ 5× 速度 + 批量           → ✅ Gemini 3.1 Flash
│     └─ 复杂布局 + 文字+图       → ✅ FLUX 2 Max
│
├─ 国潮 / 东方美学
│     ├─ 故宫 / 龙凤 / 工笔     → ✅ 文心一格 2.0
│     └─ 敦煌 / 文物 / 国画留白  → ✅ Hunyuan 3.0
│
└─ 中文场景图（万能兜底）
      ├─ 中文 prompt + 快 + 稳    → ✅ Qwen-Image 2.0
      ├─ 国产 SaaS 合规           → ✅ GLM-Image
      └─ 商业项目                → ✅ 通义万相
```

---

## 🚀 一键对照（同一句 prompt × 11 模型）

把下面这段 prompt 同时喂给 11 个模型，可视化对比效果：

```
Universal test prompt:
"Tourist silhouette standing on the summit observation deck of 
Niubei Mountain at sunrise, sea of clouds rolling beneath, golden 
sunrise light firing the sky crimson and orange, snow-capped Mt. 
Gongga (Minya Konka) on the far horizon piercing through clouds. 
Meditative atmosphere. National Geographic photography, 8K ultra 
detail, cinematic wide-angle composition, photorealistic. 
Aspect ratio 16:9."
```

| 模型 | 输出特征预期 |
|---|---|
| MJ v6.2 | 极致写实 / 戏剧云海 / 远景超清 |
| DALL-E 3 | 偏明亮 / 写实 / 偏"摄影"风格 |
| GPT Image 2 | 自然叙事 / 写实 / 沉稳 |
| Gemini 3 Pro | 高对比 / 鲜艳 / 略"美化" |
| Gemini Flash | 同 Pro 但细节弱 20% |
| Seedream 5.0 | 中文版更佳 / 西方场景略弱 |
| FLUX 2 Max | 极致细节 / prompt 保真度高 |
| Hunyuan 3.0 | 国画留白 / 写意 / 古典感 |
| Qwen-Image 2.0 | 海报感 / 文字稳 / 写实中等 |
| 通义万相 | 商业海报 / 整体偏设计 |
| GLM-Image | 中文 + 商业可用 |
| MiniMax-Image-01 | 戏剧光影 / 史诗气质 |
| 文心一格 2.0 | 国潮 / 工笔 / 东方气韵 |

---

## 📚 进一步阅读

- OpenAI Image API 官方文档：https://platform.openai.com/docs
- Google Gemini Image 文档：https://ai.google.dev/
- Seedream 文档：https://www.volcengine.com/docs/82379
- BFL FLUX 文档：https://docs.bfl.ai/
- 腾讯混元 API：https://cloud.tencent.com/product/hunyuan
- 阿里通义/Qwen Image：https://help.aliyun.com/
- 智谱 BigModel：https://open.bigmodel.cn/
- 百度文心一格：https://yige.baidu.com/
- MiniMax 平台：https://platform.MiniMax.io

---

> 📌 **最后强调**：所有模型的**最佳 prompt 长度、参数体系、API 字段名**可能随版本迭代变化。本指南给出的是**通用规律框架**，实战中请以对应平台**官方最新文档**为准；如有 PR 反馈，仓库文档会同步更新。
