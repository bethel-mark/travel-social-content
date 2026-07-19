# 🔌 4 大图像生成 API 实操指南

> 通用 prompt 写法（每个模型怎么写）见 [`references/image-models-optimization.md`](../references/image-models-optimization.md)。  
> **本文件专注：怎么实操获取生图能力** —— key 怎么拿、怎么调、怎么接入 skill。

---

## 📋 速查表（4 大接入方式）

| # | 接入方式 | 提供模型 | Key 申请 | 难度 | 推荐场景 |
|---|---|---|---|---|---|
| 1 | **OpenAI API** | GPT Image 2 / DALL·E 3 | platform.openai.com | 🟢 简单 | GPT-Image-2 实测 |
| 2 | **Google AI Studio** | Gemini 3 Pro Image / Gemini 3.1 Flash / Imagen 4 | aistudio.google.com | 🟢 简单 | Gemini、Imagen 实测 |
| 3 | **Vertex AI** | Imagen 4 / Imagen 3 / Gemini 全系 | Google Cloud Console | 🟡 中等 | 企业生产、批量 |
| 4 | **OpenRouter** | 100+ 模型一站式（含 nano-banana、Flux、SDXL） | openrouter.ai | 🟢 简单 | 多模型对比 |

---

## 1️⃣ OpenAI（GPT Image 2）— 最简单

### 适用模型
- `gpt-image-2`（本指南命名为 GPT Image 2，对应 OpenAI 官方当前最强生图模型）
- `dall-e-3`
- `dall-e-2`（基础款，少用）

### 获取 API Key
1. 访问 [platform.openai.com](https://platform.openai.com)
2. 注册 → 完成账单（**需要预付 5 美元起**）
3. → API Keys → Create new secret key
4. 复制 `sk-proj-xxx...` 或 `sk-xxx...`
5. 写入环境变量：
   ```bash
   export OPENAI_API_KEY="sk-proj-xxx..."
   ```

### 调用方式（curl）
```bash
# 1 张 1024x1024 图
curl -X POST "https://api.openai.com/v1/images/generations" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-image-2",
    "prompt": "Cinematic wide photograph of Mount Hua summit at sunrise, sea of clouds rolling beneath the ridge, snow-capped Minya Konka on the horizon, warm golden hour light, National Geographic photography, 8K ultra detail",
    "size": "1536x1024",
    "quality": "high",
    "n": 1
  }' | tee openai_response.json

# 提取 URL
URL=$(cat openai_response.json | python3 -c "import sys, json; print(json.load(sys.stdin)['data'][0]['url'])")
curl -o output.png "$URL"
```

### 价格（2026-Q3 公开价）
| 模型 | 1024² | 1024×1536 / 1536×1024 |
|---|---|---|
| GPT Image 2 | $0.040 / 张 | $0.080 / 张 |
| DALL·E 3 | $0.040 / 张 (std) / $0.080 (hd) | $0.080 / $0.120 / 张 |

### Python SDK 调用
```python
from openai import OpenAI
client = OpenAI(api_key="sk-xxx")

resp = client.images.generate(
    model="gpt-image-2",
    prompt="Cinematic photograph of Pit No.1 at the Terracotta Army...",
    size="1536x1024",
    quality="high",
    n=1,
)
url = resp.data[0].url
# 下载
import httpx
httpx.get(url).raise_for_status()
```

### 🎯 推荐用途
- 单张出图、极致写实
- 与 GPT-4o 文本模型联动（"先写场景文本，再丢给 GPT Image 2 出图"）

---

## 2️⃣ Google AI Studio（Imagen + Gemini）— 免费入门首选

### 适用模型
- `imagen-4.0-generate-001`（**Imagen 4** 旗舰）
- `imagen-4.0-fast-generate-001`（Imagen 4 Fast，~3× 快）
- `imagen-3.0-generate-001`
- `gemini-3-pro-image-preview`（多模态生图）
- `gemini-3.1-flash-image-preview`（速度版）

### 获取 API Key（**免费试用**）
1. 访问 [aistudio.google.com](https://aistudio.google.com)
2. Google 账号登录
3. → Get API key → Create API key in new project
4. 复制 `AIza-xxx...`
5. 写入环境变量：
   ```bash
   export GOOGLE_API_KEY="AIza-xxx..."
   ```

### 🎯 GeminiNano-banana 的获取方式

坊间传闻的 "Nano-Banana"（Nano Banana）是 **Gemini 3 Pro Image Preview 的内部代号**，已在 Google AI Studio 上公开发布：

```bash
# 通过 Google AI Studio API（基础路径，推荐个人）
curl -X POST \
  "https://generativelanguage.googleapis.com/v1beta/models/gemini-3-pro-image-preview:generateContent" \
  -H "x-goog-api-key: $GOOGLE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "contents": [{
      "parts": [{
        "text": "Cinematic wide photograph of Mount Hua at sunrise..."
      }]
    }],
    "generationConfig": {
      "responseModalities": ["TEXT", "IMAGE"]
    }
  }' > gemini_response.json

# 提取 base64 image
python3 -c "
import json, base64
d = json.load(open('gemini_response.json'))
parts = d['candidates'][0]['content']['parts']
for p in parts:
    if 'inlineData' in p:
        img = base64.b64decode(p['inlineData']['data'])
        open('output.png', 'wb').write(img)
        print('Saved output.png', len(img), 'bytes')
        break
"
```

### Imagen 4（更高写实质量）
```bash
curl -X POST \
  "https://generativelanguage.googleapis.com/v1beta/models/imagen-4.0-generate-001:predict" \
  -H "x-goog-api-key: $GOOGLE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "instances": [{"prompt": "Mount Hua sunrise..."}],
    "parameters": {
      "sampleCount": 1,
      "aspectRatio": "16:9",
      "personGeneration": "dont_allow"
    }
  }' > imagen_response.json

# 提取
python3 -c "
import json, base64
d = json.load(open('imagen_response.json'))
img = base64.b64decode(d['predictions'][0]['bytesBase64Encoded'])
open('output.png', 'wb').write(img)
"
```

### 价格（Google AI Studio 公开价）
| 模型 | 价格 |
|---|---|
| Imagen 4 | $0.04 / 张（1024²）|
| Imagen 4 Fast | $0.02 / 张 |
| Gemini 3 Pro Image | $1.25 / 1M 输出 token（含图）|

### 🎯 推荐用途
- ✅ **完全免费试用**（每分钟限速）—— 立刻上手
- 中文 prompt 强（适合 GBK 场景）
- ✅ nano-banana / Gemini 3 Pro Image 直接测

---

## 3️⃣ Vertex AI（企业生产 / Imagen 4 + Gemini 全系）

### 适用模型
- Imagen 4 / Imagen 3 全系
- Gemini 3 Pro Image 全系
- 与 Google AI Studio 模型一致，但**走 Google Cloud 认证**

### 获取认证（多步，比 AI Studio 复杂）
```bash
# 1. 安装 gcloud CLI（macOS）
brew install --cask google-cloud-sdk

# 2. 登录
gcloud auth login
gcloud auth application-default login   # ADC for API 调用

# 3. 创建 / 选择项目
gcloud projects create my-travel-images --name="Travel Images"
gcloud config set project my-travel-images

# 4. 启用 API
gcloud services enable \
  aiplatform.googleapis.com \
  generativelanguage.googleapis.com

# 5. 设置默认 region（推荐 us-central1）
gcloud config set compute/region us-central1

# 6. 服务账号（生产用）
gcloud iam service-accounts create sa-travel-image \
  --display-name="Travel Image Gen"
```

### 调用方式（Python SDK）
```python
import vertexai
from vertexai.preview.vision_models import ImageGenerationModel

vertexai.init(project="my-travel-images", location="us-central1")

model = ImageGenerationModel.from_pretrained("imagen-4.0-generate-001")
images = model.generate_images(
    prompt="Mount Hua sunrise, sea of clouds...",
    number_of_images=1,
    aspect_ratio="16:9",
    safety_filter_level="block_few",
    person_generation="dont_allow",
)
images[0].save(location="output.png")
```

### 价格
与 Google AI Studio 一致，**但走企业结算**

### 🎯 推荐用途
- 企业 / 高 QPS / 多项目共用
- 需要 VPC 隔离 / IAM 权限管理
- Imagen 4 + Gemini 全系统一管理

---

## 4️⃣ OpenRouter（一站式 100+ 模型）— 多模型对比首选

### 适用模型
- 100+ 模型即点即用，包括：
  - **nano-banana**（Gemini 3 Pro Image Preview 的 OpenRouter 别名）
  - `google/gemini-3-pro-image-preview`
  - `google/gemini-3.1-flash-image-preview`
  - `openai/gpt-image-2`
  - `black-forest-labs/flux-2-max`
  - `stability/stable-diffusion-3.5-large`
  - `xai/grok-2-image`
  - 各类国内模型（DeepSeek、Qwen-VL）
  - **统一一个 key 调全部**

### 获取 API Key
1. 访问 [openrouter.ai](https://openrouter.ai)
2. Google / GitHub 账号登录
3. → Keys → Create Key
4. 复制 `sk-or-v1-xxx...`
5. 写入环境变量：
   ```bash
   export OPENROUTER_API_KEY="sk-or-v1-xxx..."
   ```

### 调用方式（与 OpenAI 100% 兼容）
```bash
# 同样的接口，同样的 payload，只是换 base_url + key
curl -X POST "https://openrouter.ai/api/v1/images/generations" \
  -H "Authorization: Bearer $OPENROUTER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "google/gemini-3-pro-image-preview",
    "prompt": "Mount Hua at sunrise...",
    "size": "1536x1024",
    "n": 1
  }' > or_response.json
```

### 价格（OpenRouter 加 5% 服务费，部分模型更便宜）
| 模型 | 价格 |
|---|---|
| Gemini 3 Pro Image | ~ $0.04 / 张 |
| GPT Image 2 | ~ $0.04 / 张 |
| FLUX 2 Max | ~ $0.05 / 张 |
| Stable Diffusion 3.5 | ~ $0.03 / 张 |

### 核心优势
- 🎯 **一 key 调所有模型** —— 多模型对比成本最低
- 🎯 **统一 rate limit** —— 比直接调各厂商 API 限速更宽松
- 🎯 **支持 nano-banana 别名**（= Gemini 3 Pro Image，但调用名友好）

### 🎯 推荐用途
- ✅ 多模型 A/B 测试（同 prompt 喂 5+ 模型）
- ✅ 国外模型按量付费、不绑定单一厂商
- ✅ nano-banana / FLUX / Stable Diffusion 等小众模型

---

## 5️⃣ 接入到 travel-social-content 服务（标准化）

`scripts/api/image_adapter.py` 提供 4 个主流 API 的**统一接口**：

```python
from scripts.api.image_adapter import ImageAdapter, ImageRequest

# 自动检测环境变量并选择 provider
adapter = ImageAdapter()  # 4 个 key 任一个即可

req = ImageRequest(
    prompt="Mount Hua sunrise, sea of clouds, 8K cinematic",
    aspect_ratio="16:9",
    quality="high",
    n=1,
)

img_bytes = adapter.generate(req)
# img_bytes 是 PNG bytes，可以：
# 1. 返回给前端展示
# 2. 保存到本地
# 3. 进一步传给其他工具
```

**FastAPI 端点**：
```bash
curl -X POST http://localhost:8000/api/v1/generate-image \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Mount Hua sunrise...",
    "model_hint": "nano-banana",   # 可选：自动落到 openrouter
    "aspect_ratio": "16:9"
  }'
```

**详见 `scripts/api/image_adapter.py` 实现**（Provider 自动 fallback 链）：
```
按优先级检测：
  1. GOOGLE_API_KEY → Gemini 3 Pro Image / Imagen 4
  2. OPENAI_API_KEY → GPT Image 2 / DALL-E 3
  3. OPENROUTER_API_KEY → 100+ 模型
  4. (无 key) → 返回 prompt，让用户手动调
```

---

## 💰 价格对比（4 大接入）

| 模型 | OpenAI 直 | Google AI | OpenRouter | 推荐 |
|---|---|---|---|---|
| GPT Image 2 | $0.04-0.08 | ❌ | $0.04 | OpenAI 直 |
| DALL·E 3 | $0.04-0.12 | ❌ | $0.04 | OpenAI 直 |
| Gemini 3 Pro Image | ❌ | $1.25/M token | $0.04 | **OpenRouter（便宜 30×）** |
| Imagen 4 | ❌ | $0.04 | $0.02 | Google AI 直 |
| FLUX 2 Max | ❌ | ❌ | $0.05 | OpenRouter |
| nano-banana | ❌ | ✅ | ✅ | **OpenRouter（最简）** |

💡 **结论**：
- 单模型用 → **直接调对应厂商 API**（最便宜 + 最高速率）
- 多模型对比 → **OpenRouter** 一个 key 搞定

---

## 🚀 一键测试：4 个 API 哪些能用

写一个 `/tmp/check_apis.sh`：

```bash
#!/bin/bash
# check_apis.sh - 测试你现有的 API key 哪些能调用生图 API

echo "🔑 4 大生图 API 状态检测"
echo "===================================="

# OpenAI
if [ -n "$OPENAI_API_KEY" ]; then
  STATUS=$(curl -s -o /dev/null -w '%{http_code}' \
    -H "Authorization: Bearer $OPENAI_API_KEY" \
    "https://api.openai.com/v1/models")
  echo "OpenAI:        $STATUS ($( [ "$STATUS" = "200" ] && echo "✅ OK" || echo "❌ FAIL" ))"
else
  echo "OpenAI:        ⏸️  (无 OPENAI_API_KEY)"
fi

# Google AI
if [ -n "$GOOGLE_API_KEY" ]; then
  STATUS=$(curl -s -o /dev/null -w '%{http_code}' \
    -H "x-goog-api-key: $GOOGLE_API_KEY" \
    "https://generativelanguage.googleapis.com/v1beta/models")
  echo "Google AI:     $STATUS ($( [ "$STATUS" = "200" ] && echo "✅ OK" || echo "❌ FAIL" ))"
else
  echo "Google AI:     ⏸️  (无 GOOGLE_API_KEY)"
fi

# Vertex AI（看 ADC 是否配置）
if gcloud auth application-default print-access-token >/dev/null 2>&1; then
  echo "Vertex AI:     ✅ gcloud ADC 已配置"
else
  echo "Vertex AI:     ⏸️  (无 gcloud auth)"
fi

# OpenRouter
if [ -n "$OPENROUTER_API_KEY" ]; then
  STATUS=$(curl -s -o /dev/null -w '%{http_code}' \
    -H "Authorization: Bearer $OPENROUTER_API_KEY" \
    "https://openrouter.ai/api/v1/models")
  echo "OpenRouter:    $STATUS ($( [ "$STATUS" = "200" ] && echo "✅ OK" || echo "❌ FAIL" ))"
else
  echo "OpenRouter:    ⏸️  (无 OPENROUTER_API_KEY)"
fi

echo "===================================="
```

输出示例：
```
🔑 4 大生图 API 状态检测
====================================
OpenAI:        200 ✅ OK
Google AI:     200 ✅ OK
Vertex AI:     ✅ gcloud ADC 已配置
OpenRouter:    ⏸️  (无 OPENROUTER_API_KEY)
====================================
```

---

## 📚 进一步参考

- OpenAI Image API：https://platform.openai.com/docs/api-reference/images
- Google AI Studio：https://aistudio.google.com
- Vertex AI Imagen：https://cloud.google.com/vertex-ai/generative-ai/docs/image/overview
- OpenRouter Models：https://openrouter.ai/models
- Prompt 写法：见仓库 [`references/image-models-optimization.md`](../references/image-models-optimization.md)
- 跨 11 模型对比输出：见 [`examples/cross-models-comparison.md`](cross-models-comparison.md)
