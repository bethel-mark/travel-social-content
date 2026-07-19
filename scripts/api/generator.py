"""Build a final prompt for the destination + run search via shell helper.

This module does NOT call any LLM directly — the caller decides whether
to invoke llm_adapter.generate() or to surface the prompt for the user
to paste manually.
"""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path
from typing import Optional

# Resolve repo paths at import time
ROOT = Path(__file__).resolve().parents[2]
SKILL_PATH = ROOT / "SKILL.md"
TEMPLATE_PATH = ROOT / "references" / "output-template.md"
DESTINATIONS_PATH = ROOT / "references" / "destinations.md"
SEARCH_SCRIPT = ROOT / "scripts" / "search-destination.sh"

DEFAULT_PLATFORMS = "小红书 / Instagram / 朋友圈 / 微博"
DEFAULT_STYLE_NOTE = "默认情绪共鸣型 + 反差吸引型 + 数字攻略型"


def read_file(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return ""


def run_search(destination: str) -> tuple[bool, str]:
    """Invoke scripts/search-destination.sh and capture the raw cache file."""
    if not SEARCH_SCRIPT.exists():
        return False, ""
    try:
        subprocess.run(
            ["bash", str(SEARCH_SCRIPT), destination, "--save"],
            check=False, capture_output=True, text=True, timeout=20,
        )
    except (subprocess.TimeoutExpired, FileNotFoundError) as exc:
        return False, f"search error: {exc}"
    cache_file = ROOT / "cache" / f"{destination.replace(' ', '_')}-raw.md"
    if cache_file.exists():
        return True, cache_file.read_text(encoding="utf-8")
    return False, ""


def build_prompt(destination: str, platform: str, style: str,
                  secondary_styles: Optional[list[str]] = None,
                  num_image_prompts: int = 3,
                  language: str = "zh") -> str:
    """Compose the final prompt that should be sent to the LLM."""
    skill_text = read_file(SKILL_PATH)
    template_text = read_file(TEMPLATE_PATH)
    destinations_text = read_file(DESTINATIONS_PATH)

    extras = ""
    if secondary_styles:
        extras = "\n## 附加风格：" + "、".join(secondary_styles) + "\n"

    return f"""# 任务：生成《{destination}》社交媒体内容方案

## 平台：{platform}
## 主风格：{style}
## AI 生图 Prompt 数量：每子景点 {num_image_prompts} 个
## 语言：{language}{extras}

---

## 角色
你是一名资深文旅社媒内容运营，熟悉小红书 / Instagram / 微博 / 朋友圈的算法规律。

## ⚠️ 严格遵循 Skill 主入口
以下是 SKILL.md 的完整内容（请逐条对齐）：

```
{skill_text}
```

## ⚠️ 严格按输出模板输出
以下是 references/output-template.md 的章节模板（请不要漏章节）：

```
{template_text}
```

## 📚 速查档案（如适用）
{destinations_text}

---

## 📋 你的输出必须满足：
1. **结构**：8 个标准章节（目的地简述 / 景点详细方案 / 发布建议 / 热门趋势 / 系列化建议 / 参考来源 / 合规提示 / AI 协作声明）
2. **子景点数**：3-6 个（每个子景点配 AI prompt × {num_image_prompts}）
3. **覆盖类型**：自然 / 人文 / 美食 / 季节 / 夜景 / 小众 至少 3 种
4. **文案风格**：除主风格外，至少再附 2 种（系列打卡 + 反差吸引必备）
5. **AI prompt 中英双语**，每个带 `--ar / --v 6.2` 参数
6. **实用信息**：所有价格 / 时间 / 距离必须是具体数字
7. **参考链接**：≥ 3 条编号
8. **合规**：末段需有「AI 协作生成」标识

---

## 现在请开始输出完整方案。
"""


def assemble_full_prompt_only(destination: str, platform: str, style: str,
                                secondary_styles: Optional[list[str]] = None,
                                num_image_prompts: int = 3,
                                language: str = "zh",
                                include_search: bool = True) -> dict:
    """Build the prompt + optionally attach raw search results."""
    prompt = build_prompt(
        destination=destination,
        platform=platform,
        style=style,
        secondary_styles=secondary_styles,
        num_image_prompts=num_image_prompts,
        language=language,
    )
    raw_search = ""
    if include_search:
        ok, content = run_search(destination)
        if ok:
            raw_search = content
            prompt += "\n\n---\n## 原始检索结果（参考用）\n\n" + content

    return {"prompt": prompt, "raw_search": raw_search}
