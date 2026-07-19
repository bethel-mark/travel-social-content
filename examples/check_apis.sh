#!/usr/bin/env bash
# check_apis.sh — 测试你现有的 API key 哪些能调用生图 API
#
# 用法:
#   bash examples/check_apis.sh
#
# 输出:
#   每行显示一个 Provider 状态 (200/4xx/timeout)
#   "OK" 表示 key 有效，能调通 list endpoint（不消耗 token）

set +e

echo ""
echo "============================================="
echo "🔑 4 大生图 API 状态检测"
echo "============================================="

check() {
  local label="$1"; local url="$2"; local header="$3"
  local key_var="$4"
  local key="${!key_var}"
  if [ -z "$key" ]; then
    echo "  $label : ⏸️  (未配置 $key_var)"
    return
  fi
  local status=$(curl -s -o /dev/null -w '%{http_code}' --max-time 10 \
    -H "$header" "$url" 2>&1)
  case "$status" in
    200) echo "  $label : $status ✅ OK" ;;
    401) echo "  $label : $status ❌ key 无效" ;;
    429) echo "  $label : $status ⚠️  限流（但 key 有效）" ;;
    *)   echo "  $label : $status ❓ 异常" ;;
  esac
}

check "  OpenAI    "  "https://api.openai.com/v1/models"                         "Authorization: Bearer $OPENAI_API_KEY"         OPENAI_API_KEY
check "  Google AI "  "https://generativelanguage.googleapis.com/v1beta/models"   "x-goog-api-key: $GOOGLE_API_KEY"              GOOGLE_API_KEY
check "  OpenRouter"  "https://openrouter.ai/api/v1/models"                      "Authorization: Bearer $OPENROUTER_API_KEY"    OPENROUTER_API_KEY

# Vertex AI: 检查 gcloud ADC
echo ""
if command -v gcloud >/dev/null 2>&1; then
  if gcloud auth application-default print-access-token >/dev/null 2>&1; then
    echo "  Vertex AI : ✅ gcloud ADC 已配置"
  else
    echo "  Vertex AI : ⏸️  gcloud 已安装但未登录 ADC"
  fi
else
  echo "  Vertex AI : ⏸️  (未安装 gcloud CLI)"
fi

echo ""
echo "============================================="
echo "可用模型（基于已配置的 key）："
echo "============================================="
if [ -n "$GOOGLE_API_KEY" ]; then
  echo "  Google AI:  gemini-3-pro-image-preview (nano-banana) / imagen-4"
fi
if [ -n "$OPENAI_API_KEY" ]; then
  echo "  OpenAI:     gpt-image-2 / dall-e-3"
fi
if [ -n "$OPENROUTER_API_KEY" ]; then
  echo "  OpenRouter: 100+ models including nano-banana, flux-2-max, gpt-image-2"
fi
if command -v gcloud >/dev/null 2>&1 && gcloud auth application-default print-access-token >/dev/null 2>&1; then
  echo "  Vertex AI:  imagen-4 + gemini 全系"
fi
if [ -z "$GOOGLE_API_KEY$OPENAI_API_KEY$OPENROUTER_API_KEY" ]; then
  echo "  ⚠️  没有任何 key 配置！请看 examples/using-image-apis.md 获取指引"
fi
echo ""
