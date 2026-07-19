#!/usr/bin/env bash
# search-destination.sh — 命令行检索目的地信息
#
# 用法：
#   ./search-destination.sh "<目的地名>" [--save|--print]
#
# 输出：
#   默认打印到 stdout；--save 写入 cache/<目的地>-raw.md
#
# 依赖：
#   - curl（系统自带）
#   - DuckDuckGo HTML 搜索引擎（无需 API key）
#
# 注意：
#   这是「离线脚本」的参考实现。当作为 Codex Skill 使用时，
#   实际搜索通过宿主平台的内建 web search 工具完成，
#   本脚本仅作为可移植的 CLI 替代方案存在。

set -euo pipefail

DEST="${1:-}"
ACTION="${2:-print}"

if [[ -z "$DEST" ]]; then
  cat << EOF
Usage: $0 <destination-name> [print|save]

Examples:
  $0 "稻城亚丁"
  $0 "九寨沟" save
  $0 "敦煌" --save
EOF
  exit 1
fi

# 解析 cache 目录（绝对路径）
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
CACHE_DIR="$ROOT_DIR/cache"
mkdir -p "$CACHE_DIR"

# URL 编码
ENCODED=$(printf '%s' "$DEST" | python3 -c "import sys, urllib.parse; print(urllib.parse.quote(sys.stdin.read()))")

# DuckDuckGo HTML 搜索（无需 key）
URL="https://html.duckduckgo.com/html/?q=${ENCODED}+旅游+攻略+门票+开放时间"

echo "🔍 检索: $DEST" >&2
echo "🔗 目标: $URL" >&2
echo "" >&2

RAW=$(curl -sS \
  -A "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36" \
  "$URL" 2>&1 | sed 's/<[^>]*>/ /g' | tr -s ' \n' ' ' | head -c 8000)

# 提取引擎结果片段
CLEANED=$(echo "$RAW" | tr ' ' '\n' | grep -v '^$' | head -200)

OUTPUT="# $DEST · 原始搜索摘要

> ⏱ 生成时间: $(date '+%Y-%m-%d %H:%M:%S')
> 🔍 检索引擎: DuckDuckGo HTML
> 🎯 查询关键词: $DEST 旅游 攻略 门票 开放时间

---

## 关键搜索片段

$CLEANED

---

*本片段由 search-destination.sh 自动检索得到。正式方案请结合以下权威来源验证：*
- 当地文旅局官方公众号
- 国家 A 级景区官方小程序
- 大众点评 / 小红书最新 UGC
- 12306 / 各 OTA 平台票务页
"

if [[ "$ACTION" == "save" ]] || [[ "$ACTION" == "--save" ]]; then
  OUTFILE="$CACHE_DIR/$(echo "$DEST" | tr ' ' '_')-raw.md"
  echo "$OUTPUT" > "$OUTFILE"
  echo "✅ 已保存到: $OUTFILE" >&2
else
  echo "$OUTPUT"
fi
