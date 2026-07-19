"""LLM adapter — supports 6 providers with graceful fallback.

Order of detection (env vars):
  1. ANTHROPIC_API_KEY  → Anthropic Claude
  2. OPENAI_API_KEY     → OpenAI gpt-4o-mini / gpt-4o
  3. DEEPSEEK_API_KEY   → DeepSeek
  4. KIMI_API_KEY       → Moonshot Kimi (月之暗面)
  5. BAILIAN_API_KEY    → 阿里云百炼 DashScope (通义千问 Qwen)
  6. ZHIPU_API_KEY      → 智谱 BigModel (GLM-4 系列)
  7. (none of above)    → 'needs_llm' mode, return prompt string
"""
from __future__ import annotations

import os
import sys
from dataclasses import dataclass


@dataclass
class LLMConfig:
    provider: str          # 'anthropic' | 'openai' | 'deepseek' | 'kimi' | 'bailian' | 'zhipu' | 'none'
    model: str
    api_key: str
    base_url: str | None = None


# 6 个 Provider 的元数据：base_url + 默认 model + env var
PROVIDER_REGISTRY = {
    "anthropic": {
        "env": "ANTHROPIC_API_KEY",
        "default_model": "claude-3-5-sonnet-latest",
        "base_url": None,                                  # 使用 SDK 默认
        "openai_compat": False,
        "sdk": "anthropic",
    },
    "openai": {
        "env": "OPENAI_API_KEY",
        "default_model": "gpt-4o-mini",
        "base_url": None,
        "openai_compat": True,
        "sdk": "openai",
    },
    "deepseek": {
        "env": "DEEPSEEK_API_KEY",
        "default_model": "deepseek-chat",
        "base_url": "https://api.deepseek.com/v1",
        "openai_compat": True,
        "sdk": "openai",
    },
    # 🆕 Kimi (Moonshot) — 已 401 暂记，待用户补 key
    "kimi": {
        "env": "KIMI_API_KEY",
        "default_model": "moonshot-v1-8k",
        "base_url": "https://api.moonshot.cn/v1",
        "openai_compat": True,
        "sdk": "openai",
    },
    # 🆕 Bailian (阿里云百炼 DashScope) — OpenAI 兼容 endpoint
    "bailian": {
        "env": "BAILIAN_API_KEY",
        "default_model": "qwen-plus",
        "base_url_env": "BAILIAN_BASE_URL",
        "default_base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1",
        "openai_compat": True,
        "sdk": "openai",
    },
    # 🆕 Zhipu (智谱 BigModel) — 自家 API，不是 OpenAI 兼容
    "zhipu": {
        "env": "ZHIPU_API_KEY",
        "default_model": "glm-4-flash",
        "base_url": "https://open.bigmodel.cn/api/paas/v4",
        "openai_compat": False,
        "sdk": "zhipu",
    },
}


def detect_llm() -> LLMConfig:
    """Pick the best available LLM config from environment variables."""
    for name, meta in PROVIDER_REGISTRY.items():
        if not os.getenv(meta["env"]):
            continue
        base_url = meta.get("base_url")
        if "base_url_env" in meta and os.getenv(meta["base_url_env"]):
            base_url = os.environ[meta["base_url_env"]]
        model = os.getenv(f"{name.upper()}_MODEL") or meta["default_model"]
        return LLMConfig(
            provider=name,
            model=model,
            api_key=os.environ[meta["env"]],
            base_url=base_url,
        )
    return LLMConfig(provider="none", model="", api_key="")


def list_configured_providers() -> list[str]:
    """Return the names of all providers that currently have keys set."""
    configured = []
    for name, meta in PROVIDER_REGISTRY.items():
        if os.getenv(meta["env"]):
            configured.append(name)
    return configured


def generate(prompt: str, cfg: LLMConfig, max_tokens: int = 4096) -> str:
    """Call the configured LLM and return the response text.

    Raises ImportError or RuntimeError if provider package is missing.
    """
    if cfg.provider == "none":
        raise RuntimeError(
            "No LLM configured. Set ANTHROPIC_API_KEY / OPENAI_API_KEY / "
            "DEEPSEEK_API_KEY / KIMI_API_KEY / BAILIAN_API_KEY / ZHIPU_API_KEY "
            "environment variable, or use 'needs_llm' mode."
        )

    # 1) Anthropic (自己 SDK)
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

    # 2) OpenAI 兼容家族：openai / deepseek / kimi / bailian
    if cfg.provider in {"openai", "deepseek", "kimi", "bailian"}:
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

    # 3) Zhipu (BigModel 自家 API)
    if cfg.provider == "zhipu":
        try:
            import httpx  # type: ignore
        except ImportError:
            import urllib.request, urllib.error, json as _json
            payload = {
                "model": cfg.model,
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": max_tokens,
            }
            req = urllib.request.Request(
                f"{cfg.base_url.rstrip('/')}/chat/completions",
                headers={
                    "Authorization": f"Bearer {cfg.api_key}",
                    "Content-Type": "application/json",
                },
                method="POST",
            )
            try:
                resp = urllib.request.urlopen(
                    req, data=_json.dumps(payload).encode(), timeout=120
                )
                data = _json.loads(resp.read())
                return data["choices"][0]["message"]["content"] or ""
            except urllib.error.HTTPError as e:
                raise RuntimeError(f"Zhipu HTTP {e.code}: {e.read().decode()}") from e
        import httpx as _httpx
        with _httpx.Client(timeout=120) as cli:
            r = cli.post(
                f"{cfg.base_url.rstrip('/')}/chat/completions",
                headers={"Authorization": f"Bearer {cfg.api_key}"},
                json={
                    "model": cfg.model,
                    "messages": [{"role": "user", "content": prompt}],
                    "max_tokens": max_tokens,
                },
            )
        r.raise_for_status()
        return r.json()["choices"][0]["message"]["content"] or ""

    raise RuntimeError(f"Unsupported provider: {cfg.provider}")


if __name__ == "__main__":
    cfg = detect_llm()
    configured = list_configured_providers()
    print(f"primary  : provider={cfg.provider} model={cfg.model}", file=sys.stderr)
    print(f"configured: {configured}", file=sys.stderr)
