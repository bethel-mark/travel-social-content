# 🌐 travel-social-content API

> 把 SKILL.md 的 7 步流程暴露成 REST API，让任何 HTTP 客户端（CI 机器人、Notion 插件、Slack bot、JS 应用）都能即时拿到旅游社媒内容方案。

---

## ✨ 这是什么

一个**自带 LLM 接入**的 Python FastAPI 服务。当你给它一个城市名 + 平台 + 风格，它返回完整的 Markdown 方案（8 章节标准化输出）。

**两种模式**：
- **🟢 自动模式**：配置了 `ANTHROPIC_API_KEY` / `OPENAI_API_KEY` / `DEEPSEEK_API_KEY` 时，API 调 LLM 直接返回最终方案
- **🟡 Prompt 模式**：没配置 key 时，返回拼好的 prompt 字符串，你可以复制到任意 AI 助手（ChatGPT、Claude、Gemini、Kimi）

---

## 🚀 快速启动

### 方式 1：本地直接跑（推荐开发）

```bash
# 1. 装依赖
pip install -r requirements-api.txt

# 2. 设置至少一个 LLM key
export ANTHROPIC_API_KEY="sk-ant-xxx"   # or OPENAI_API_KEY / DEEPSEEK_API_KEY

# 3. 启动
cd /path/to/travel-social-content
python scripts/api/server.py
# → 服务跑在 http://localhost:8000
```

### 方式 2：Docker（推荐生产）

```bash
cp .env.example .env
vim .env       # 填入 key
docker compose up -d
# → 服务跑在 http://localhost:8000
```

### 方式 3：导入为 Python 包

```python
from scripts.api.generator import build_prompt
prompt = build_prompt(
    destination="敦煌",
    platform="xiaohongshu",
    style="反差吸引型",
)
print(prompt)
```

---

## 📚 API 文档

启动后访问 `http://localhost:8000/docs` 看到**完整的 Swagger UI**（FastAPI 自动生成）。下面给最常用的 3 个端点：

### `GET /health`

```bash
curl http://localhost:8000/health
```

```json
{
  "status": "ok",
  "version": "1.0.0",
  "llm_configured": true,
  "search_available": true
}
```

### `POST /api/v1/generate`

```bash
curl -X POST http://localhost:8000/api/v1/generate \
  -H "Content-Type: application/json" \
  -d '{
    "destination": "敦煌",
    "platform": "xiaohongshu",
    "style": "反差吸引型",
    "secondary_styles": ["情绪共鸣型", "数字攻略型"],
    "num_image_prompts": 3,
    "include_search": true,
    "language": "zh"
  }'
```

**有 LLM key 时返回**：

```json
{
  "status": "ok",
  "destination": "敦煌",
  "platform": "xiaohongshu",
  "style": "反差吸引型",
  "markdown": "# 敦煌市 旅游社交媒体内容方案\n\n...",
  "prompt_to_llm": null,
  "raw_search": "...",
  "skill_version": "1.0.0",
  "warnings": [],
  "references_used": ["SKILL.md", "references/output-template.md", "LLM: anthropic/claude-3-5-sonnet-latest"]
}
```

**无 LLM key 时返回**：

```json
{
  "status": "needs_llm",
  "destination": "敦煌",
  "markdown": null,
  "prompt_to_llm": "# 任务：生成《敦煌》...\n\n---\n\n## 角色\n你是一名资深文旅社媒...",
  "warnings": [
    "No LLM API key configured. Set ANTHROPIC_API_KEY...",
    "Otherwise copy `prompt_to_llm` into any AI assistant..."
  ]
}
```

### `GET /api/v1/destinations`

返回速查档案中已收录的目的地列表：

```json
{
  "destinations": [
    "四川省（已收录 8 大景点）",
    "成都",
    "杭州",
    "西安",
    "拉萨",
    "西双版纳",
    "大理",
    "敦煌",
    "..."
  ]
}
```

---

## 🧪 测试用例（curl）

`examples/api-curl.sh` 里放了**5 个测试**：

```bash
bash examples/api-curl.sh
```

---

## 🔌 接入现有 3 大 LLM 的对比

| Provider | 模型 | 优势 | 性价比 |
|---|---|---|---|
| Anthropic | `claude-3-5-sonnet-latest` | 文案 + 中文 prompt 质量最佳 | ⭐⭐⭐⭐ |
| OpenAI | `gpt-4o-mini` | 价格最低 / 速度快 | ⭐⭐⭐⭐⭐ |
| DeepSeek | `deepseek-chat` | 中文输出 / 极致便宜 | ⭐⭐⭐⭐⭐ |

**默认推荐**：个人 / 小流量 → `gpt-4o-mini`；团队 / 高质量 → `claude-3-5-sonnet`。

---

## 🚢 生产部署提示

1. **限流**：用 nginx / Cloudflare 把 `POST /api/v1/generate` 限到 30 req/min/IP
2. **缓存**：在 nginx 层加 `proxy_cache_valid 200 1h`，目的地被复用时响应毫秒级
3. **Auth**：当前是公开 API，**生产前**务必加 `Authorization: Bearer <token>` 校验
4. **异步**：当 LLM 慢时（Claude 30s+），可改 `/api/v1/generate` 为 job-id 模式 + webhook
5. **持久化**：把 `cache/` 目录挂载到 S3 / 阿里云 OSS，跨实例共享

---

## 📦 与 SKILL.md 关系

```
SKILL.md (主流程)
    ├── Step 1-4 →  reference/prompts/  (规则)
    ├── Step 5    →  schemas.py + generator.py
    ├── Step 6    →  llm_adapter.py (provider 切换)
    └── Step 7    →  output-template.md + examples/
```

API 服务**不是**替代 Skill，只是把 Skill 流程暴露给 HTTP 客户端。直连 Codex/Claude Code 仍是首选（更省 token）。

