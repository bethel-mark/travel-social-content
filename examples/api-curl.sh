#!/usr/bin/env bash
# api-curl.sh — 5 个 API 端点的 curl 测试用例
#
# 先启动服务：
#   cd /path/to/travel-social-content
#   python scripts/api/server.py     # 或者 docker compose up -d
#
# 然后跑：
#   bash examples/api-curl.sh

set -e

BASE="${API_BASE:-http://localhost:8000}"

echo "🩺 1/5  GET /health"
curl -fsS "$BASE/health" | python3 -m json.tool
echo ""

echo "📋 2/5  GET /api/v1/destinations（速查城市）"
curl -fsS "$BASE/api/v1/destinations" | python3 -c "import sys, json; d=json.load(sys.stdin); print('已收录目的地:', len(d['destinations'])); print('前 5:', d['destinations'][:5])"
echo ""

echo "🚀 3/5  POST /api/v1/generate (无 LLM key 时返回 prompt)"
curl -fsS -X POST "$BASE/api/v1/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "destination": "敦煌",
    "platform": "xiaohongshu",
    "style": "反差吸引型",
    "secondary_styles": ["情绪共鸣型", "数字攻略型"],
    "num_image_prompts": 3,
    "language": "zh"
  }' | python3 -c "import sys, json; d=json.load(sys.stdin); print('status:', d['status']); print('prompt 长度:', len(d.get('prompt_to_llm') or '')); print('warnings:', d.get('warnings', [])[:1])"
echo ""

echo "📷 4/5  POST /api/v1/generate (Instagram)"
curl -fsS -X POST "$BASE/api/v1/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "destination": "冰岛",
    "platform": "instagram",
    "style": "情绪共鸣型",
    "secondary_styles": ["反差吸引型"],
    "language": "both"
  }' | python3 -c "import sys, json; d=json.load(sys.stdin); print('status:', d['status']); print('destination:', d['destination'])"
echo ""

echo "🇨🇳 5/5  POST /api/v1/generate (北京 朋友圈)"
curl -fsS -X POST "$BASE/api/v1/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "destination": "北京",
    "platform": "wechat_moments",
    "style": "情绪共鸣型",
    "num_image_prompts": 1,
    "include_search": true
  }' | python3 -c "import sys, json; d=json.load(sys.stdin); print('status:', d['status'])"
echo ""

echo "✅ 全部端点测试完成。如需 markdown 内容，请配置 ANTHROPIC_API_KEY / OPENAI_API_KEY 后重启服务。"
