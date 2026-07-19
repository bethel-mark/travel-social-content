# 🎨 AI 生图 Prompt 速查手册 · 通用 + Midjourney v6.2 / DALL-E / 即梦 / SDXL

> 📌 **本文件覆盖**：通用 prompt 公式、Midjourney v6.2 / DALL-E 3 / 即梦 / 豆包 / Stable Diffusion XL 5 个模型 + 10 个景点模板。
>
> 📚 **新文件**：要看 **GPT Image 2 / Gemini 3 Pro / Seedream 5.0 / FLUX 2 Max / Hunyuan 3.0 / Qwen-Image 2.0 / 通义万相 / GLM-Image / MiniMax-Image-01 / 文心一格 2.0** 等 11 大模型的专项优化 → [`image-models-optimization.md`](image-models-optimization.md)。


> Skill 输出 Step 5「生成 AI 生图 Prompt 套件」的执行手册。

---

## 🎯 通用公式

```
[主体] + [环境/季节/天气] + [光线/色调] + [构图/视角] + [风格/参考] + [参数]
```

**填空示例**：

```
Yading Holy Mountain in Sichuan during golden sunrise,
with turquoise Milk Lake reflection in foreground,
golden hour side light, cinematic wide composition 3:2,
National Geographic photography style, 8K ultra detail,
--ar 3:2 --style raw --s 200 --v 6.2
```

---

## 🛠️ 各平台参数速查

### Midjourney v6.2

| 参数 | 含义 | 常用值 |
|---|---|---|
| `--ar` | 画幅 | `9:16`（小红书/Reel）/ `1:1`（朋友圈）/ `16:9`（横版）|
| `--v 6.2` | 版本号 | 6.2（最新）|
| `--style raw` | 减少 MJ 风格化（更真实）| 长旅游场景建议开 |
| `--s` | 风格化强度 | 0-1000，默认 100。**真实感场景用 100-250** |
| `--c` | 抽象程度 | 0-100，越大越怪诞（旅游图不调） |
| `--q` | 质量 | 0.25 / 0.5 / 1 / 2，默认 1 |
| `--no` | 负面提示 | `--no people, text` |
| `--seed` | 固定种子 | 用于复现 |

### DALL-E 3

```
A photo of <subject>, <setting>, <lighting>, <style reference>
```

- 自动加 `professional photography` 风格
- 默认 1024×1024，可改 1792×1024 / 1024×1792

### 即梦 / 豆包（国产）

- 中文 prompt 直接可用
- 推荐格式：「xxx 摄影，xxx 风格，xxx 光线，xx 镜头」
- 比例支持 1:1 / 3:4 / 4:3 / 9:16 / 16:9

### Stable Diffusion XL

```yaml
prompt: "english positive prompt"
negative_prompt: "low quality, blurry, text, watermark"
sampler: DPM++ 2M Karras
steps: 30
cfg_scale: 7
size: 1024x1024
```

---

## 📐 画幅选择

| 平台 | 推荐比例 | 用途 |
|---|---|---|
| 小红书 | **3:4 或 4:5** | 竖图 + 9 宫格 |
| 抖音 / Reel | **9:16** | 全屏竖屏 |
| 朋友圈 | **1:1** | 正方形首图 |
| Instagram Feed | **1:1 或 4:5** | 主流 |
| B 站封面 | **16:9** | 横版 |
| 微博头图 | **16:9** | 横向 |

---

## 🎨 8 大景点 Prompt 模板库

### 1 · 九寨沟 · 五花海

**主图（视觉冲击级）**：
```
Autumn multicolored travertine lake (Five Flower Sea / Wuhuahai) in
Jiuzhaigou Valley, Sichuan, mirror-clear reflection with red orange and
gold foliage surrounding, snow-capped ridges in background, mid-October
peak color, cinematic saturation, golden hour rim light,
wide-angle 3:2 composition, photorealistic, 8K.
--ar 3:2 --style raw --v 6.2
```

**备用 1（瀑布版）**：
```
Pearl Shoal Waterfall in Jiuzhaigou after autumn rain, wide curtain of
crystal water cascading over mossy travertine, sunbeam piercing mist,
surrounding forest ablaze in crimson and amber, long exposure silk water,
epic landscape photography.
--ar 16:9 --style raw --v 6.2
```

**备用 2（人物大片）**：
```
Woman in burgundy scarf standing on wooden trail by Five Flower Lake,
back to camera, dwarfed 1:6 by towering autumn forest reflection,
meditative, misty dawn light, cinematic shallow DOF, medium format
film grain.
--ar 9:16 --style raw --s 200 --v 6.2
```

### 2 · 稻城亚丁 · 牛奶海

```
Milk-blue alpine lake (Milk Sea / Niunaihai) at Yading Holy Mountain,
foreground pierces Daocheng's three sacred peaks above 6000m, glacial
sediment turquoise water so clear stones visible, golden hour rim light
on snow pyramid peak of Mt. Yangmaiyong, low mist in valley, epic
cinematic wide composition, 8K ultra detail, no people.
--ar 3:2 --style raw --s 200 --v 6.2
```

### 3 · 黄龙 · 五彩池

```
Layered travertine terraces of Huanglong in Sichuan, cascading turquoise
and emerald calcite pools, golden calcium sand along edges, snow-capped
Min Mountain backdrop, autumn mountain forest, aerial drone perspective,
hyper-real natural wonder, vibrant saturated mineral colors.
--ar 4:5 --style raw --v 6.2
```

### 4 · 峨眉山 · 金顶日出

```
Golden 48-meter Samantabhadra statue at summit of Mount Emei at sunrise,
above an infinite sea of clouds, crimson and gold horizon, dramatic
Buddhist temple silhouette, telephoto lens compression, warm golden
hour volumetric light, epic mountainous spirituality, photorealistic.
--ar 3:2 --style raw --s 250 --v 6.2
```

### 5 · 四姑娘山 · 双桥沟

```
Four Girls Mountain (Siguniang) in autumn, snow-capped peaks perfectly
mirrored in calm alpine lake, foreground of golden larch and red
birch forest, S-curving mountain road in distance, dramatic sky with
god rays piercing clouds, high-saturation autumn, serene mountain
tranquility, 8K ultra detailed.
--ar 16:9 --style raw --v 6.2
```

### 6 · 若尔盖 · 黄河九曲

```
First Great Bend of Yellow River at Zoige Grassland, Sichuan, golden
sunset light spreading across winding turquoise river, vast green
grassland dotted with grazing yaks, dramatic orange-purple cloudscape,
yurt camp wisps of smoke, epic landscape, peaceful and majestic.
--ar 3:2 --style raw --v 6.2
```

### 7 · 三星堆 · 青铜面具

```
Ancient bronze ritual mask from Sanxingdui Museum, Sichuan, mysterious
protruding eyes and geometric features, dramatic low-key lighting
against black museum background, 24mm wide angle close-up, ancient
Shu civilization atmosphere, cinematic color grading (cyan & amber),
museum editorial photography, 8K ultra detail.
--ar 4:5 --style raw --v 6.2
```

### 8 · 都江堰 · 鱼嘴分水

```
Dujiangyan ancient irrigation system fish-mouth levee at Sichuan,
turquoise Min River water splitting around engineered stone dam,
traditional Qing-dynasty Nanqiao Bridge in background, late afternoon
warm light, aerial wide composition, showcasing 2000-year engineering
wisdom, photorealistic, sharp details.
--ar 16:9 --style raw --v 6.2
```

### 9 · 乐山大佛

```
Magnificent 71-meter stone Buddha statue (Maitreya) carved into a
red cliff face at the confluence of three rivers in Leshan, Sichuan,
ancient Tang Dynasty sculpture detail visible from riverboat below,
lush green mountains surrounding, river mist in foreground,
golden sunset light, low angle wide shot, photorealistic, 8K,
national geographic style.
--ar 3:2 --style raw --s 200 --v 6.2
```

### 10 · 蜀南竹海

```
Aerial view of Shunan Bamboo Sea in Yibin, Sichuan, endless waves of
emerald bamboo canopy stretching to misty mountains, traditional
corridor cutting through sea of green, morning light filtering
through bamboo leaves creating light columns, cinematic atmosphere,
vast scale, photography style, 8K.
--ar 3:2 --style raw --v 6.2
```

---

## ⚠️ 避坑清单

### ❌ 禁用词
- `a photo of`（NSFW 触发）
- `perfect`, `stunning`, `amazing`（过于抽象）
- 任何**真人姓名**（版权 / 肖像）
- 任何品牌**logo**（侵权）
- `by <author>` 之类的署名（违规）

### ✅ 推荐词
- `photorealistic, cinematic, 8K ultra detail`
- `national geographic style`
- `golden hour, dramatic lighting, volumetric light`
- `film grain, medium format`
- 风格参考：`in the style of National Geographic / Lonely Planet / 视觉中国`

### 细节检查
- **人脸**：3 人以上易崩，建议用「背影 + 极小比例」
- **文字**：AI 易生成乱码，建议 `no text, no watermark`
- **建筑**：中国古建避免现代元素混搭
- **宗教**：避免神圣符号商品化（如佛像抱奶茶）
- **少数民族**：避免服饰错乱、用错图腾

---

## 🧪 测试 3 步：如何判断生成的 Prompt 好不好

1. **结构检查**：主体 / 环境 / 光线 / 构图 / 风格 / 参数 是否齐全
2. **可替换性**：把景点名替换成同类景点（如「五花海→镜海」）是否仍通顺
3. **视觉预演**：在脑中（或 AI 草稿中）能否浮现明确画面

如果不达标，至少重写 1 个元素（如把「spring」改为「late autumn」）。

---

## 📚 进阶资源

- Midjourney 官方文档：https://docs.midjourney.com
- Stable Diffusion Prompt 指南：https://prompthero.com
- 即梦 / 豆包官方教程：见各平台官网
- 摄影构图速查：三分法 / 对角线 / 留白 / 引导线

---

> **本速查基于 2026 年 AI 生图主流模型能力整理。模型升级时需要 PR 同步更新。**
