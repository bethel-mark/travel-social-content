#!/usr/bin/env bash
# install.sh — 一键安装 travel-social-content Skill
# 用法: ./scripts/install.sh symlink | copy | uninstall

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
SKILL_NAME="$(basename "$SKILL_ROOT")"

CODEX_SKILLS_DIR="${CODEX_SKILLS_DIR:-$HOME/.codex/skills}"
CLAUDE_SKILLS_DIR="${CLAUDE_SKILLS_DIR:-$HOME/.claude/skills}"

print_a() { printf "\033[1;36m▶\033[0m %s\n" "$*"; }
print_s() { printf "\033[1;32m✓\033[0m %s\n" "$*"; }
print_w() { printf "\033[1;33m⚠\033[0m %s\n" "$*"; }
print_e() { printf "\033[1;31m✗\033[0m %s\n" "$*"; }

MODE="${1:-symlink}"

case "$MODE" in
    symlink)
        print_a "symlink 模式（开发模式，仓库改动即时生效）"
        # 容错：可能没有 ~.claude 写入权限
        mkdir -p "$CODEX_SKILLS_DIR" 2>/dev/null || true
        mkdir -p "$CLAUDE_SKILLS_DIR" 2>/dev/null || true
        for td in "$CODEX_SKILLS_DIR" "$CLAUDE_SKILLS_DIR"; do
            target="$td/$SKILL_NAME"
            rm -rf "$target" 2>/dev/null || true
            if ln -sf "$SKILL_ROOT" "$target" 2>/dev/null; then
                print_s "$target → $SKILL_ROOT"
            else
                print_w "$td 没有写入权限, 跳过 (单独装 Codex)"
            fi
        done
        ;;
    copy)
        print_a "copy 模式（生产模式，与源独立）"
        if mkdir -p "$CODEX_SKILLS_DIR" 2>/dev/null; then
            target="$CODEX_SKILLS_DIR/$SKILL_NAME"
            rm -rf "$target" 2>/dev/null || true
            cp -R "$SKILL_ROOT" "$target"
            print_s "$target"
        else
            print_e "无法创建 $CODEX_SKILLS_DIR"
            exit 1
        fi
        ;;
    uninstall)
        print_a "卸载"
        for td in "$CODEX_SKILLS_DIR" "$CLAUDE_SKILLS_DIR"; do
            target="$td/$SKILL_NAME"
            if [ -L "$target" ] || [ -d "$target" ]; then
                rm -rf "$target"
                print_s "deleted $target"
            fi
        done
        ;;
    *)
        echo "用法: $0 {symlink|copy|uninstall}"
        exit 1
        ;;
esac

echo ""
print_a "验证"
entry="$CODEX_SKILLS_DIR/$SKILL_NAME/SKILL.md"
if [ -e "$entry" ]; then
    nm=$(awk '/^name:/{print $2; exit}' "$entry")
    print_s "Skill '$nm' 已可用 at $entry"
fi

echo ""
print_a "下次怎么用?"
cat <<EOX
  在 Codex / Claude Code 输入:
    用 $SKILL_NAME skill 为「敦煌」出一份小红书风格内容方案
EOX
