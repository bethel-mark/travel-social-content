"""LLM adapter — supports multiple providers with graceful fallback.

Order of detection (env vars):
  1. ANTHROPIC_API_KEY  → Anthropic Claude
  2. OPENAI_API_KEY     → OpenAI gpt-4o-mini / gpt-4o
  3. DEEPSEEK_API_KEY   → DeepSeek
  4. (none of above)    → 'needs_llm' mode, return prompt string
"""
from __future__ import annotations

import os
import sys
from dataclasses import dataclass


@dataclass
class LLMConfig:
    provider: str          # 'anthropic' | 'openai' | 'deepseek' | 'none'
    model: str
    api_key: str
    base_url: str | None = None


def detect_llm() -> LLMConfig:
    """Pick the best available LLM config from environment variables."""
    if os.getenv("ANTHROPIC_API_KEY"):
        return LLMConfig(
            provider="anthropic",
            model=os.getenv("ANTHROPIC_MODEL", "claude-3-5-sonnet-latest"),
            api_key=os.environ["ANTHROPIC_API_KEY"],
        )
    if os.getenv("OPENAI_API_KEY"):
        return LLMConfig(
            provider="openai",
            model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            api_key=os.environ["OPENAI_API_KEY"],
            base_url=os.getenv("OPENAI_BASE_URL"),
        )
    if os.getenv("DEEPSEEK_API_KEY"):
        return LLMConfig(
            provider="deepseek",
            model=os.getenv("DEEPSEEK_MODEL", "deepseek-chat"),
            api_key=os.environ["DEEPSEEK_API_KEY"],
            base_url=os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com/v1"),
        )
    return LLMConfig(provider="none", model="", api_key="")


def generate(prompt: str, cfg: LLMConfig, max_tokens: int = 4096) -> str:
    """Call the configured LLM and return the response text.

    Raises ImportError or RuntimeError if provider package is missing.
    """
    if cfg.provider == "none":
        raise RuntimeError(
            "No LLM configured. Set ANTHROPIC_API_KEY / OPENAI_API_KEY / "
            "DEEPSEEK_API_KEY or use 'needs_llm' mode."
        )

    if cfg.provider == "anthropic":
        try:
            import anthropic  # type: ignore
        except ImportError as e:
            raise ImportError("anthropic package missing: pip install anthropic") from e
        client = anthropic.Anthropic(api_key=cfg.api_key)
        msg = client.messages.create(
            model=cfg.model,
            max_tokens=max_tokens,
            messages=[{"role": "user", "content": prompt}],
        )
        return msg.content[0].text  # type: ignore[return-value]

    if cfg.provider == "openai":
        try:
            import openai  # type: ignore
        except ImportError as e:
            raise ImportError("openai package missing: pip install openai") from e
        client = openai.OpenAI(api_key=cfg.api_key, base_url=cfg.base_url)
        chat = client.chat.completions.create(
            model=cfg.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
        )
        return chat.choices[0].message.content or ""

    if cfg.provider == "deepseek":
        try:
            import openai  # type: ignore
        except ImportError as e:
            raise ImportError("openai package missing (DeepSeek uses OpenAI SDK): pip install openai") from e
        client = openai.OpenAI(api_key=cfg.api_key, base_url=cfg.base_url)
        chat = client.chat.completions.create(
            model=cfg.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
        )
        return chat.choices[0].message.content or ""

    raise RuntimeError(f"Unsupported provider: {cfg.provider}")


if __name__ == "__main__":
    cfg = detect_llm()
    print(f"provider={cfg.provider} model={cfg.model}", file=sys.stderr)
