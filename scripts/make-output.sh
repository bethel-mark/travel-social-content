#!/usr/bin/env bash
# make-output.sh — 一键组装最终社媒方案（通过 LLM CLI）
#
# 用法：
#   ./make-output.sh "<目的地>" --platform <p> --style <s>
#
# 工作流：
#   1. 调用 search-destination.sh 拉取原始检索结果
#   2. 拼接 SKILL.md 的执行流程作为 prompt
#   3. 通过 LLM CLI（qwen / claude / openai）生成最终方案
#   4. 输出到 examples/<目的地>-output.md
#
# 依赖（任选其一）：
#   - qwen CLI（Qwen-CLI，免费）           → https://github.com/QwenLM/Qwen-Agent
#   - claude CLI（需 API key）              → https://docs.anthropic.com
#   - openai CLI（需 OPENAI_API_KEY）       → https://platform.openai.com
#
# 不配置 LLM CLI 时，本脚本会打印完整的 prompt 供你复制到任意 AI 助手。

set -euo pipefail

DEST="${1:-}"

if [[ -z "$DEST" ]]; then
  echo "Usage: $0 <destination-name> [--platform <p>] [--style <s>]" >&2
  echo "" >&2
  echo "Examples:" >&2
  echo "  $0 '稻城亚丁' --platform xiaohongshu --style '反差吸引型'" >&2
  echo "  $0 '敦煌' --platform weibo --style '数字攻略型'" >&2
  echo "" >&2
  echo "Note: 输出目录 examples/<destination>-output.md" >&2
  exit 1
fi

PLATFORM="xiaohongshu"
STYLE="反差吸引型"

shift
while [[ $# -gt 0 ]]; do
  case "$1" in
    --platform) PLATFORM="$2"; shift 2 ;;
    --style)    STYLE="$2"; shift 2 ;;
    *)          echo "Unknown option: $1" >&2; exit 1 ;;
  esac
done

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
SKILL_FILE="$ROOT_DIR/SKILL.md"
REF_FILE="$ROOT_DIR/references/output-template.md"
DEST_REF="$ROOT_DIR/references/destinations.md"

# Step 1: 拉搜索摘要
RAW_CACHE="$ROOT_DIR/cache/$(echo "$DEST" | tr ' ' '_')-raw.md"
echo "📡 Step 1/3  拉取原始检索..." >&2
"$SCRIPT_DIR/search-destination.sh" "$DEST" --save > /dev/null 2>&1

if [[ ! -f "$RAW_CACHE" ]]; then
  RAW_CACHE_CONTENT="（未取得原始检索结果，依赖模型自身知识储备）"
else
  RAW_CACHE_CONTENT=$(cat "$RAW_CACHE")
fi

# Step 2: 拼接 prompt
PROMPT="# 任务：生成《${DEST}》社交媒体内容方案

## 平台：${PLATFORM}
## 风格：${STYLE}

---

## 角色
你是一名资深文旅社媒内容运营，熟悉小红书/Instagram/微博/朋友圈的算法规律。

## Skill 主入口（请严格遵循）
$(cat "$SKILL_FILE")

## 输出模板（严格按章节顺序）
$(cat "$REF_FILE")

## 速查档案（如果 ${DEST} 在内可直接调用）
$(cat "$DEST_REF")

## 原始检索结果（来自 DuckDuckGo，仅作参考）
$RAW_CACHE_CONTENT

---

## 请现在生成完整方案，保存到 examples/$(echo "$DEST" | tr ' ' '_')-output.md
"

# Step 3: 通过 LLM CLI 生成
OUTFILE="$ROOT_DIR/examples/$(echo "$DEST" | tr ' ' '_')-output.md"
mkdir -p "$(dirname "$OUTFILE")"

if command -v qwen >/dev/null 2>&1; then
  echo "🤖 Step 3/3  使用 qwen CLI 生成..." >&2
  qwen chat "$PROMPT" > "$OUTFILE"
  echo "✅ 已保存到: $OUTFILE" >&2
elif command -v claude >/dev/null 2>&1; then
  echo "🤖 Step 3/3  使用 claude CLI 生成..." >&2
  claude chat "$PROMPT" > "$OUTFILE"
  echo "✅ 已保存到: $OUTFILE" >&2
elif command -v openai >/dev/null 2>&1; then
  echo "🤖 Step 3/3  使用 openai CLI 生成..." >&2
  openai chat "$PROMPT" > "$OUTFILE"
  echo "✅ 已保存到: $OUTFILE" >&2
else
  echo "⚠️  未检测到 LLM CLI（qwen/claude/openai 任一）" >&2
  echo "" >&2
  echo "📋 完整 prompt 已生成，请复制下方代码块内容到任意 AI 助手（ChatGPT / Claude / Kimi 等）使用：" >&2
  echo "" >&2
  echo "==========================================" >&2
  echo "$PROMPT" >&2
  echo "==========================================" >&2
  echo "" >&2
  echo "💾 之后把 AI 输出保存到: $OUTFILE" >&2
fi
