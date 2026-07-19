# 🧪 真实 API 实测报告

> **2026-07-19 16:40 实时测试 · chat + 图片生成端点**

本报告记录用户提供的 4 个 LLM API Key 真实调用结果，用于验证 `image_adapter.py` + `llm_adapter.py` 的端到端可用性。

---

## 📊 Key 状态总览

| Provider | Key 截断 | Models GET | 实测调用 | 综合结论 |
|---|---|---|---|---|
| **Zhipu GLM** | `594db1c9...dRYD` | ✅ 200 | ✅ 出图成功 | **🟢 完整可用** |
| **Kimi (Moonshot)** | `sk-oclPL...kEyW` | ❌ 401 | ❌ 401 Invalid Authentication | **🔴 Key 无效** |
| **Bailian (百炼)** | （未提供） | — | — | **🟡 需提供 Key** |
| **DeepSeek** | `sk-53a70...b1e9` | ✅ 200 | ⚠️ Insufficient Balance | **🟡 Key 有效但余额 0** |

---

## 🟢 Zhipu GLM 完整测试

### Models List
```bash
curl https://open.bigmodel.cn/api/paas/v4/models \
  -H "Authorization: Bearer 594db1c9...dRYD"
# → HTTP 200 (可用)
```

### Chat Completion
```bash
curl -X POST https://open.bigmodel.cn/api/paas/v4/chat/completions \
  -H "Authorization: Bearer 594db1c9...dRYD" \
  -d '{"model":"glm-4-flash","messages":[{"role":"user","content":"回 1 字"}],"max_tokens":5}'
```
**响应**：
```json
{
  "choices": [{"message": {"content": "回", "role": "assistant"}, "index": 0, "finish_reason": "stop"}],
  "model": "glm-4-flash",
  "usage": {"prompt_tokens": 9, "completion_tokens": 3, "total_tokens": 12}
}
```
**延迟**：~2 秒 ✅

### Image Generation × 2 Models

#### CogView-3（快速版）
```bash
curl -X POST https://open.bigmodel.cn/api/paas/v4/images/generations \
  -H "Authorization: Bearer 594db1c9...dRYD" \
  -d '{
    "model": "cogview-3",
    "prompt": "Cinematic wide-angle museum photograph inside Pit No.1 of the Terracotta Army in Xi'an...",
    "size": "1024x1024"
  }'
```
**延迟**：~10 秒 ✅
**响应**：URL 已生成（智谱默认带水印）
**保存图**：[`assets/generated-samples/terracotta_cogview3_zhipu_1024.png`](../assets/generated-samples/terracotta_cogview3_zhipu_1024.png) (120 KB JPEG)

#### GLM-Image（高质量版）
```bash
# 同样调用，仅 model 改为 "glm-image"
```
**延迟**：~32 秒 ✅
**保存图**：见 `/tmp/test_apple.png` (110 KB JPEG)

### 可用尺寸（已实测）
| Aspect | Size | 32 倍数 | 可用 |
|---|---|---|---|
| 1:1 | 1024x1024 | ✅ | ✅ |
| 16:9 | 1344x768 | ✅ | ✅（新增！） |
| 9:16 | 768x1344 | ✅ | ✅（新增！） |
| 4:3 | 1152x864 | ✅ | ✅（新增！） |

⚠️ **720 / 1280 不是 32 倍数**，错误信息：`size 的长宽均需满足 512px-2880px 之间, 且为 32 整数倍`

---

## 🔴 Kimi (Moonshot) - Key 无效

```bash
curl https://api.moonshot.cn/v1/models \
  -H "Authorization: Bearer sk-oclPL...kEyW"
# → HTTP 401 Invalid Authentication

curl -X POST https://api.moonshot.cn/v1/chat/completions \
  -H "Authorization: Bearer sk-oclPL...kEyW" \
  -d '{"model":"moonshot-v1-8k","messages":[{"role":"user","content":"回 1"}],"max_tokens":5}'
# → {"error":{"message":"Invalid Authentication","type":"invalid_authentication_error"}}
```

**结论**：Key 在 Moonshot 后台校验失败。可能原因：
- Key 被复制时包含多余空格 / 引号
- Key 已被撤销或过期
- Key 实际属于另一个项目

**用户可做**：
1. 重新从 [Moonshot 控制台](https://platform.moonshot.cn/) 复制
2. 检查账户余额
3. 联系 Moonshot 技术支持

**框架仍支持**：用户补一个有效 key 就能立即工作。

---

## 🟡 Bailian (阿里云百炼) - 缺 Key

用户提供的：
```
base_url: https://ws-a57qq9t2s2olw78k.cn-beijing.maas.aliyuncs.com/compatible-mode/v1
key:      （未提供）
```

框架已完整支持 Bailian（OpenAI 兼容模式，可调 Qwen-Image / Wanxiang），只需提供 `BAILIAN_API_KEY`。

---

## 🟡 DeepSeek - Key 有效但余额 0

```bash
curl https://api.deepseek.com/v1/models \
  -H "Authorization: Bearer sk-53a70...b1e9"
# → HTTP 200 (key valid)

curl -X POST https://api.deepseek.com/v1/chat/completions \
  -H "Authorization: Bearer sk-53a70...b1e9" \
  -d '{"model":"deepseek-chat","messages":[{"role":"user","content":"回 1 字"}],"max_tokens":5}'
# → {"error":{"message":"Insufficient Balance","code":"invalid_request_error"}}
```

**结论**：Key 在 DeepSeek 后台合法，但账户余额为 0 元。
**修复**：在 [DeepSeek 控制台](https://platform.deepseek.com) 充值即可。

---

## 🔌 集成状态

| 文件 | 已更新支持 |
|---|---|
| `scripts/api/llm_adapter.py` | **6 个** provider：anthropic / openai / deepseek / **kimi** / **bailian** / **zhipu** |
| `scripts/api/image_adapter.py` | **5 个** provider：openai / google / openrouter / **bailian** / **zhipu** |
| `scripts/api/server.py` | 新端点 `POST /api/v1/generate-image`，可选 `provider` 参数 |
| `examples/check_apis.sh` | 一键探测 4 大 provider 的连通性（不消耗 token）|
| `.env.example` | 含 6 个 provider 的 env 变量模板 |

### 优先级 fallback 链
```
LLM:  anthropic > openai > deepseek > kimi > bailian > zhipu
Image: google > openai > bailian > zhipu > openrouter
```

自动选第一个有 key 的，无须手动配置。

---

## 🎯 兵马俑示例图（cogview-3 生成）

![兵马俑 Zhipu CogView-3 生成示例](../assets/generated-samples/terracotta_cogview3_zhipu_1024.png)

这张图：
- 由 `cogview-3` 在 ~10 秒内生成
- 1024x1024 像素 JPEG（120 KB）
- prompt：`"Cinematic wide-angle museum photograph inside Pit No.1 of the Terracotta Army in Xi'an, hundreds of Qin Dynasty warriors in silent battle formation, dramatic single shaft of warm sunlight pouring through a high museum window onto the front rank of generals, weathered solemn faces gazing forward across 22 centuries, deep rows receding into atmospheric haze, National Geographic archaeology feature, photorealistic, 8K ultra detail"`
- 完全匹配 [`references/image-models-optimization.md`](../references/image-models-optimization.md) 中写出的"兵马俑 prompt 公式"

右下角"AI 生成"水印是智谱服务自带，不可去除，但**符合《人工智能生成合成内容标识办法》合规要求**。

---

## 💡 用户行动建议

| 问题 | 推荐操作 |
|---|---|
| Kimi 401 | 在 [Moonshot 控制台](https://platform.moonshot.cn/) 重新拿 Key 后填到 `KIMI_API_KEY` |
| DeepSeek 余额 0 | 在 [DeepSeek 控制台](https://platform.deepseek.com) 充值后立即恢复 |
| Bailian 缺 Key | 在 [阿里云百炼](https://bailian.console.aliyun.com/) 申请 Key → 填 `BAILIAN_API_KEY`（也支持 `BAILIAN_BASE_URL` 自定义） |
| Zhipu 可用 ✅ | 已有，无须操作 |

---

## 🔄 复现测试（任何人可执行）

```bash
export ZHIPU_API_KEY="<your-key>"
python -c "
import sys; sys.path.insert(0, 'scripts/api')
from image_adapter import ImageAdapter, ImageRequest
import time
t0 = time.time()
result = ImageAdapter().generate(ImageRequest(
    prompt='a single red apple on a wooden table',
    model='cogview-3',
    aspect_ratio='1:1',
))
print(f'{time.time()-t0:.1f}s  {len(result.png_bytes):,} bytes  {result.model}')
open('/tmp/test.png', 'wb').write(result.png_bytes)
"
```
