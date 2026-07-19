# 🔬 跨 11 大模型对比：兵马俑 / 月牙泉 / 苍山洱海

> **本示例的目的**：把**完全相同的 prompt** 同时喂给 11 个图像生成模型，**逐一标注预期输出特征 + 微调策略**。  
> 真实出图需要 API key，请参考 [`using-image-apis.md`](using-image-apis.md) 获取。
>
> 📚 每个模型的 prompt 写法 + 优势短板：见 [`references/image-models-optimization.md`](../references/image-models-optimization.md)

---

## 🎯 如何使用本文件

1. **复制 prompt** → 替换你的 key
2. **同时喂给 11 个模型** → 看哪个最符合你的审美
3. **二次微调**：根据下表微调 prompt → 再测一轮
4. **找到最佳模型** → 在你的工作流里固化

---

## 📋 测试场景 A：兵马俑 1 号坑

### 通用英文骨架（11 模型通用）
```
A documentary photograph inside Pit No.1 of the Terracotta Army 
Museum in Xi'an, Shaanxi. Hundreds of life-sized Qin Dynasty warriors 
stand in silent battle formation, half-emerged from yellow loess 
earth. A single dramatic shaft of late-morning sunlight pours through 
a high museum window onto the front rank of generals. Their faces 
are weathered, expressions solemn, gazing forward across 22 centuries.

Composition: vista view from the second-floor museum walkway, deep 
rows of warriors receding into atmospheric haze.

Color palette: warm ochre foreground, cool gray haze background, 
single golden light beam.

Style: National Geographic archaeology feature, Annie Leibovitz 
museum lighting, medium-format film grain.

Aspect ratio: 3:2 (horizontal landscape)
Photorealistic. 8K ultra detail.
```

---

### 各模型针对性调整（同一画面的 11 种解读）

#### 🤖 1 · GPT Image 2 (OpenAI)
**微调策略**：再叙事化 50%
```
A hushed, reverent documentary photograph inside Pit No.1 of the 
Terracotta Army Museum in Xi'an. The morning light is angled to 
fall through a single high museum window, illuminating the front 
rank of weathered Qin Dynasty clay generals whose solemn faces 
have gazed forward across twenty-two centuries. Behind them, 
ten thousand warriors stand in silent battle formation, half 
emerged from the yellow loess earth of the pit. Deep rows of 
warriors recede into atmospheric haze and shadow. The air itself 
feels heavy with history. Captured in the style of Annie Leibovitz 
museum lighting, medium-format film grain, warm earth tones 
dominating the foreground.

Aspect ratio: 3:2. Photorealistic, 8K ultra detail.
```
**预期输出**：写实质感最强，几乎"就在那里"。不太会偏风格化。

---

#### 🔵 2 · Gemini 3 Pro Image (Google)
**微调策略**：拆成段落、给参数
```
[主体]
Hundreds of life-sized Qin Dynasty warriors in silent battle 
formation, half-emerged from yellow loess earth in Pit No.1 of 
the Terracotta Army Museum, Xi'an.

[技术]
Shot from second-floor museum walkway. 35mm wide-angle. Single 
shaft of late-morning light through high window illuminating 
front rank.

[氛围 + 风格]
Reverent, hushed. Warm earth tones, cool gray haze.

Style: National Geographic archaeology feature, Steven Alvarez 
museum lighting, medium-format film grain.

[输出参数]
aspect_ratio: "3:2"
```
**预期输出**：高对比、略"美化"，光感强烈。

---

#### ⚡ 3 · Gemini 3.1 Flash Image (Google)
**微调策略**：把上面的 Pro prompt 缩短 30%
```
[主体]
Hundreds of Qin warriors in silent battle formation, half-emerged 
from yellow earth in Pit No.1 of the Terracotta Army Museum.

[技术]
Single shaft of light through museum window onto front rank, deep 
rows fading into haze, warm earth palette.

aspect_ratio: "3:2"
```
**预期输出**：同 Pro 但细节弱 15-20%，速度 ×5。

---

#### 🎨 4 · Seedream 5.0 (字节)
**微调策略**：**中文为主** + 关键英文术语括注
```
秦始皇兵马俑 1 号坑博物馆内景，几百个真人大小的秦代陶俑军阵
静默列队，半埋在黄土中。一束清晨阳光（golden morning light）
从博物馆高窗射下，正好打在前列将军俑的面部。

表情肃穆，目光深邃。身穿铠甲。凝视 2200 年。

画面构图：从博物馆二楼观景台（second-floor walkway）俯拍，
前面几张清晰，远处阵列逐渐模糊在大气雾化中（atmospheric haze）。

色调：土黄、灰陶、单一暖光束
风格：国家地理考古摄影（National Geographic archaeology）， 
电影级博物馆灯光，史蒂文·阿尔瓦雷斯（Steven Alvarez）风格

参数：3:2 横向，超清 8K
```
**预期输出**：东亚人脸最真实。古代服饰细节稳。

---

#### 🔶 5 · FLUX 2 Max (Black Forest Labs)
**微调策略**：**长 prompt 极致保真**
```
A wide-angle documentary museum photograph at the Terracotta Army 
Museum in Xi'an, China.

Subject: hundreds of life-sized Qin Dynasty warriors stand in 
silent battle formation inside Pit No.1. The warriors are arranged 
in long rectangular columns facing east, with a vanguard of 
elaborate-coated generals in the front rank.

Setting: a vast excavated underground pit approximately 230 meters 
east-west by 62 meters north-south. The earthen floor is uneven 
yellow loess. Modern museum infrastructure includes a high ceiling 
window on the south wall.

Lighting: a single dramatic shaft of late-morning sunlight falls 
through the high window onto the front rank of generals, their 
weathered faces illuminated with exceptional detail. The middle 
and back rows of warriors fade into deep natural shadow and 
atmospheric haze.

Color palette: warm ochre 8B7355 in the foreground, fading to 
cool gray 6B6B6B in atmospheric haze background, with a single 
golden yellow light beam FFD700 from the window.

Composition: deep perspective view, foreground generals at 30% 
largest, mid-distance columns at 50% scale, far ranks at 20% 
fading into haze. Taken from the museum's second-floor viewing 
walkway on the north side.

Technical: medium-format film grain, 35mm equivalent wide-angle 
lens at f/5.6, 1/60s, ISO 200. Photorealistic. 8K ultra detail. 
National Geographic archaeology series aesthetic.

Aspect ratio: 3:2.
```
**预期输出**：细节最丰富、文字精确、prompt 保真度最高。

---

#### 🎨 6 · Hunyuan Image 3.0 (腾讯混元)
**微调策略**：中文 + `Style: 写实` + 国画留白
```
秦始皇兵马俑 1 号坑博物馆内景，史诗级博物馆摄影。

画面主体：几百个秦代陶俑军阵静默列队，半埋在黄土中，形貌各异、
神态肃穆。前列将军俑面部被一束来自高窗的清晨阳光照亮，刻画
细腻，2200 年的岁月在他们脸上留下斑驳。

风格：写实摄影 + 国画留白意境结合
色调：以土黄、灰陶为主，前列暖色、远处冷灰色
构图：宽幅 3:2，从博物馆二楼观景台俯拍，前景清晰、远景渐隐

技术：8K 超细节，电影感景深

Style: 写实
aspect_ratio: "3:2"
```
**预期输出**：国画留白感，古朴。**中国特色场景稳**。

---

#### 🟦 7 · Qwen-Image 2.0 (阿里)
**微调策略**：中文 + `prompt_extend: true`
```
秦始皇兵马俑 1 号坑博物馆内景，秦俑军阵、暖光、土黄色调，国家
地理风格摄影，宽幅 3:2。
```
**`prompt_extend: true`** 让 Qwen 帮你润色扩写。
**预期输出**：文字渲染稳，写实中等，海报感强。

---

#### 🟦 8 · 通义万相 (阿里)
**微调策略**：中文 + `style: "商业设计"`
```
秦始皇兵马俑 1 号坑内景，几百个秦俑军阵，前列将军俑被晨光照亮，
国家地理考古摄影，史诗博物馆级，史蒂文·阿尔瓦雷斯博物馆灯光，
宽幅海报构图，土黄 + 灰陶色调。
style: 商业设计
aspect_ratio: "3:2"
```
**预期输出**：偏商业海报感，干净。

---

#### 🟦 9 · GLM-Image (智谱)
**微调策略**：中文优先
```
秦始皇兵马俑 1 号坑博物馆内景，几百个真人大小的秦俑军阵静默列
队，前列被一束晨光照亮，国家地理考古摄影风格，史诗博物馆级
写实，宽幅 3:2。
```
**预期输出**：中文场景稳定，合规商用首选。

---

#### 🍌 10 · **nano-banana / Gemini 3 Pro Image Preview** (OpenRouter 别名)
**微调策略**：与 Gemini 3 Pro 同 prompt（OpenRouter 是 Gemini 别名路由）
```
Hundreds of Qin Dynasty warriors in silent battle formation,
half-emerged from yellow loess earth in Pit No.1 of the Terracotta
Army Museum, Xi'an. Single shaft of late-morning sunlight from
high museum window onto front rank. Deep rows fade into atmospheric
haze. National Geographic archaeology series, photorealistic,
8K, medium-format film grain.

aspect_ratio: 3:2
```
> 🍌 **nano-banana = Gemini 3 Pro Image Preview 的 OpenRouter 别名**，写 prompt 时直接用上述 Gemini 3 Pro 的 prompt 即可。

**预期输出**：与 Gemini 3 Pro 一致，但 OpenRouter 加 5% 服务费但不限速。

---

#### 🟦 11 · MiniMax-Image-01
**微调策略**：英文 + 戏剧光影 + cinematic
```
A cinematic wide-angle museum photograph inside Pit No.1 of the 
Terracotta Army in Xi'an. Hundreds of life-sized Qin Dynasty 
warriors stand in silent battle formation, half-emerged from 
yellow loess earth. A single dramatic shaft of late-morning 
sunlight pours through a high museum window, illuminating the 
front rank of generals with extraordinary detail. Their weathered 
faces, gazing forward across twenty-two centuries, carry expressions 
of solemn determination.

Composition: deep perspective from the museum's second-floor 
walkway. Mid-distance columns at half scale, far ranks fading 
into atmospheric haze.

Color palette: warm ochre foreground, cool gray haze background, 
single golden light beam.

Style: in the mood of Wim Wenders museum cinematography, 
medium-format film grain. National Geographic archaeology feature,
epic scale reverence.

Aspect ratio: 3:2 (horizontal landscape)
Quality: ultra high detail
```
**预期输出**：戏剧光影最强，电影感最重，史诗气质明显。

---

#### 🟦 12 · 文心一格 2.0 (百度)
**微调策略**：中文 + 国潮风格
```
秦始皇兵马俑 1 号坑博物馆内景，秦俑军阵，前列将军俑被晨光照亮，
国家地理考古风格，宽幅 3:2，史诗写实。
```
**预期输出**：中文国潮美学，工笔感。

---

## 📋 测试场景 B：敦煌鸣沙山月牙泉日出

### 通用英文骨架
```
A breathtaking panoramic view of Mingsha Sand Dunes (Singing 
Sand Mountain) and the iconic Crescent Lake (Yueyaquan) oasis in 
Dunhuang, Gansu, at golden sunrise.

Subject: a massive crescent-shaped dune towering over a turquoise 
crescent-shaped lake. Lone camel caravan silhouette walks along 
the dune ridge.

Setting: vast Gobi desert stretching to the horizon, ancient Silk 
Road atmosphere.

Lighting: golden hour sunrise casting long shadows, illuminating 
the amber dunes with warm tonal light.

Composition: cinematic wide-angle, dune in upper 1/3, lake in 
lower-left third, camel caravan on the right ridge.

Color palette: amber 50%, turquoise 15%, deep purple shadows 20%,
sky gradient 15%.

Style: National Geographic photography, 35mm medium-format film, 
muted warm palette, ancient Silk Road romanticism.

Aspect ratio: 16:9 cinematic widescreen. Photorealistic. 8K.
```

### 各模型针对性调整

#### 🤖 1 · GPT Image 2 — narrative
```text
A breathtaking cinematic moment at Mingsha Dunes outside Dunhuang, 
Gansu, China. The first golden rays of sunrise pour over a massive 
crescent-shaped sand dune, casting the entire dune in warm amber 
light. Tucked at its base, a small turquoise crescent-shaped lake 
glows like a jewel against the surrounding sand. A lone camel 
caravan—three camels led by a Silk Road merchant—walks slowly 
along the dune ridge, their long shadows stretching across the 
sand. The vast Gobi desert extends to the horizon, an ancient 
silence broken only by the wind. Captured in the style of National 
Geographic adventure photography, medium-format film grain, warm 
muted palette.

Aspect ratio: 16:9.
```

#### 🎨 4 · Seedream 5.0 — 中文
```text
敦煌鸣沙山月牙泉日出，巨大月牙形沙丘环抱绿松石色的月牙泉，
清晨金色阳光（golden sunrise）斜射沙丘，驼队剪影（camel 
caravan silhouette）沿着沙脊行走，史诗级电影感宽幅（cinematic 
wide-angle composition），沙漠辽阔延伸到地平线，暖琥珀色调
（amber palette），国家地理摄影（National Geographic photography），
超清 8K。
```

#### 🍌 10 · nano-banana（= Gemini Pro Image via OpenRouter）
```text
See Gemini 3 Pro Image prompt. OpenRouter accepts identical 
payload, no need to change anything but the base URL.
```

> 📝 **每个模型的完整 prompt 写法见 `references/image-models-optimization.md`。本文件专注"跨模型同一目标"的对比。**

---

## 📋 测试场景 C：大理洱海环湖（治愈系）

### 通用骨架
```
A lone cyclist silhouette riding along the quiet Erhai Lake 
shoreline road in Dali, Yunnan, China. Early morning mist drifting 
across mirror-like turquoise lake water. Snow-capped Cangshan 
mountain range in background catches soft golden sunrise light. 
White Bai ethnic minority village houses with grey tile roofs 
along the shore.

Composition: wide-angle from slight elevation, road in foreground
curving through middle ground into distance.

Color palette: cyan/teal 60%, warm gold 20%, misty white 15%, 
subtle earth tones 5%.

Style: cinematic travel photography, medium-format film aesthetic,
peaceful and contemplative atmosphere. In the style of National 
Geographic Asia edition.

Aspect ratio: 16:9 (cinematic widescreen). 8K ultra detail.
```

### 治愈系特定调整：偏向中文
```text
# Seedream / Hunyuan / GLM / 文心一格：
云南大理洱海环湖治愈系晨光，一位骑行者剪影（cyclist silhouette）
孤独前行，碧绿湖水如镜面，倒映苍山十九峰覆雪（snow-capped 
Cangshan mountain），湖面雾气飘过，路边一白族民居青瓦白墙，
电影感治愈系青色 + 暖金滤镜，国家地理亚洲版摄影。
```

---

## 🧮 11 模型对照决策矩阵

| 模型 | 跨模型对比特殊优势 | 适用 prompt 特点 |
|---|---|---|
| OpenAI GPT Image 2 | 极致写实 + narrative | 中长英文 prompt + 故事感 |
| Gemini 3 Pro Image | 极致理解 + 文字渲染 | 结构化段落 + aspect_ratio 显式 |
| Gemini 3.1 Flash | 同 Pro 但快 5× | 短 30% 也行 |
| Seedream 5.0 | **中文最佳** | 中文 prompt + 英文术语 |
| FLUX 2 Max | 保真度最高 | **超长 prompt（200-500 字）** |
| Hunyuan 3.0 | 国风水墨 | 中文 + Style 标签 |
| Qwen-Image 2.0 | 中文文字渲染 | 中文 + `prompt_extend:true` |
| 通义万相 | 商业海报 | 中文 + `style:"商业设计"` |
| GLM-Image | 合规稳定 | 中文优先 |
| **nano-banana** | OpenRouter 别名 = Gemini 3 Pro | 同 Gemini 3 Pro |
| MiniMax-Image-01 | 史诗戏剧光影 | 英文 + cinematic |
| 文心一格 2.0 | 国潮工笔 | 中文 |

---

## 🎯 推荐组合策略

### 🎯 组合 1：极致写实 + 多模型 A/B
- **首选**：GPT Image 2（主测试）
- **A/B**：Gemini 3 Pro + FLUX 2 Max + nano-banana
- 视觉评估：保留 1 张最满意

### 🎯 组合 2：国风 / 中文场景
- **首选**：Seedream 5.0（中文 prompt 强）
- **A/B**：Hunyuan 3.0 + 文心一格 2.0 + Qwen-Image 2.0

### 🎯 组合 3：商业海报 / 文字密集
- **首选**：Qwen-Image 2.0（中文文字 SOTA）
- **A/B**：通义万相 + Gemini 3 Pro + FLUX 2 Max

### 🎯 组合 4：史诗 / 电影感
- **首选**：MiniMax-Image-01（戏剧光影）
- **A/B**：GPT Image 2 + FLUX 2 Max + Gemini 3 Pro

### 🎯 组合 5：成本优化（多模型对比）
- **首选**：OpenRouter（统一 key）
- **一次性**：同 prompt 喂 4-5 个模型，保留最佳

---

## 💡 实测小贴士

1. **同 prompt 多次跑**：即使是同模型，**固定 seed 跑 3-4 次** 取最佳
2. **关键元素分段测试**：先测"光影"、再测"构图"、再测"风格"，逐步叠加
3. **A/B 命名规则**：`my-project_v01_01_gemini-pro.png` 方便对照
4. **保存所有 prompt 到日志**：1 个月后回头看 = 自动进化自己的工作流

---

## 📚 相关文件

- [`references/image-models-optimization.md`](../references/image-models-optimization.md) — 各模型的 prompt 写法、优势短板、参数体系
- [`examples/using-image-apis.md`](using-image-apis.md) — 怎么获取 key + 实操调用
- [`scripts/api/image_adapter.py`](../scripts/api/image_adapter.py) — 代码层 4 provider 统一接口
