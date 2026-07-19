"""Image generation adapter — unified interface across 6 providers.

Auto-detected from environment variables (in priority order):
  1. GOOGLE_API_KEY       → Gemini 3 Pro Image / Imagen 4
  2. OPENAI_API_KEY       → GPT Image 2 / DALL-E 3
  3. BAILIAN_API_KEY      → 阿里云百炼 DashScope Qwen-Image / Wanxiang  ⭐ NEW
  4. ZHIPU_API_KEY        → 智谱 BigModel CogView / GLM-Image              ⭐ NEW
  5. OPENROUTER_API_KEY   → 100+ models via unified OpenAI-compatible endpoint
  6. (none)               → raises ImageNotConfiguredError

Usage:
    >>> from scripts.api.image_adapter import ImageAdapter, ImageRequest
    >>> adapter = ImageAdapter()
    >>> req = ImageRequest(prompt="Mount Hua at sunrise", aspect_ratio="16:9")
    >>> png_bytes = adapter.generate(req)

Override detection via TSC_IMAGE_PROVIDER env var:
    TSC_IMAGE_PROVIDER=bailian|google|openai|openrouter|zhipu
"""
from __future__ import annotations

import base64
import json
import os
import urllib.error
import urllib.request
from dataclasses import dataclass
from enum import Enum
from typing import Optional

try:
    import httpx  # type: ignore
except ImportError:
    httpx = None

    import json as _json_lib  # local alias — never collide with method param 'json'

    class _UrllibClient:
        """Minimal httpx-like client using urllib (no external deps)."""

        def __init__(self, timeout: int = 60):
            self.timeout = timeout

        def post(self, url, headers=None, json=None, timeout=None):
            payload = json
            headers = dict(headers or {})
            if payload is not None:
                body = _json_lib.dumps(payload).encode("utf-8")
                req = urllib.request.Request(url, headers=headers, method="POST")
                req.add_header("Content-Type", "application/json")
            else:
                req = urllib.request.Request(url, headers=headers, method="POST")
                body = None
            try:
                resp = urllib.request.urlopen(req, data=body, timeout=timeout or self.timeout)
                return _Resp(resp.status, resp.read(), dict(resp.headers))
            except urllib.error.HTTPError as e:
                return _Resp(e.code, e.read(), dict(e.headers or {}))

        def get(self, url, timeout=60):
            try:
                resp = urllib.request.urlopen(url, timeout=timeout)
                return _Resp(resp.status, resp.read(), dict(resp.headers))
            except urllib.error.HTTPError as e:
                return _Resp(e.code, e.read(), dict(e.headers or {}))

        def __enter__(self):
            return self

        def __exit__(self, *a):
            return False

    class _Resp:
        def __init__(self, status_code, content, headers):
            self.status_code = status_code
            self._content = content
            self.headers = headers

        def json(self):
            return _json_lib.loads(self._content)

        def raise_for_status(self):
            if self.status_code >= 400:
                raise RuntimeError(f"HTTP {self.status_code}: {self._content!r}")

        @property
        def content(self):
            return self._content

    class _HttpxNamespace:
        Client = _UrllibClient

        @staticmethod
        def get(url, timeout=60):
            return _UrllibClient().get(url, timeout=timeout)

    httpx = _HttpxNamespace()  # type: ignore


class ImageNotConfiguredError(RuntimeError):
    """Raised when no image-generation API key is configured."""


class Provider(str, Enum):
    openai = "openai"
    google = "google"
    openrouter = "openrouter"
    bailian = "bailian"   # 🆕 阿里云百炼 DashScope (OpenAI 兼容)
    zhipu = "zhipu"       # 🆕 智谱 BigModel (ZhipuAI)


@dataclass
class ImageRequest:
    prompt: str
    aspect_ratio: str = "1:1"
    quality: str = "high"
    n: int = 1
    model: Optional[str] = None       # auto-pick by provider if None
    negative_prompt: Optional[str] = None


@dataclass
class ImageResult:
    png_bytes: bytes
    provider: Provider
    model: str
    used_aspect_ratio: str
    used_quality: str
    cost_estimate_usd: float = 0.0


def detect_provider() -> Provider:
    forced = os.getenv("TSC_IMAGE_PROVIDER", "").lower().strip()
    if forced in {p.value for p in Provider}:
        return Provider(forced)
    # 优先级：Google > OpenAI > Bailian > Zhipu > OpenRouter
    if os.getenv("GOOGLE_API_KEY"):
        return Provider.google
    if os.getenv("OPENAI_API_KEY"):
        return Provider.openai
    if os.getenv("BAILIAN_API_KEY"):
        return Provider.bailian
    if os.getenv("ZHIPU_API_KEY"):
        return Provider.zhipu
    if os.getenv("OPENROUTER_API_KEY"):
        return Provider.openrouter
    raise ImageNotConfiguredError(
        "No image-generation key found. Set one of:\n"
        "  GOOGLE_API_KEY (Gemini/Imagen)\n"
        "  OPENAI_API_KEY (GPT Image 2/DALL-E 3)\n"
        "  BAILIAN_API_KEY (Qwen-Image / Wanxiang)\n"
        "  ZHIPU_API_KEY (CogView / GLM-Image)\n"
        "  OPENROUTER_API_KEY (100+ models)\n"
        "Or override via TSC_IMAGE_PROVIDER env."
    )


# Model alias tables
GOOGLE_MODELS = {
    "auto":                "gemini-3-pro-image-preview",
    "nano-banana":         "gemini-3-pro-image-preview",
    "gemini-3-pro":        "gemini-3-pro-image-preview",
    "gemini-3-flash":      "gemini-3.1-flash-image-preview",
    "imagen-4":            "imagen-4.0-generate-001",
}

OPENAI_MODELS = {
    "auto":         "gpt-image-2",
    "gpt-img-2":    "gpt-image-2",
    "gpt-image-2":  "gpt-image-2",
    "dall-e-3":     "dall-e-3",
}

# 🆕 阿里云百炼 DashScope OpenAI 兼容模式（compatible-mode）
# 模型名遵循 `qwen-image-...` 或 `wanx-...`（通义万相）
BAILIAN_MODELS = {
    "auto":        "qwen-image-2",           # 默认
    "qwen-image":  "qwen-image-2",
    "qwen-image-2":"qwen-image-2",
    "qwen-image-1":"qwen-image-1",
    "wanx-v1":     "wanx-v1",
    "wanxiang":    "wanx-v1",
}

# 🆕 智谱 BigModel 图像生成（CogView / GLM-Image）
# API: https://open.bigmodel.cn/api/paas/v4/images/generations
# Zhipu 实际能用的 2 个生图 model（已实测）
# cogview-3 = 快（~10s）+ 1024x1024 ✅
# glm-image  = 高质量（~30s）+ 1024x1024 ✅
ZHIPU_MODELS = {
    "auto":         "cogview-3",                  # 默认走最快的
    "cogview-3":    "cogview-3",
    "glm-image":    "glm-image",
    "cogview-2":    "cogview-2",
}

OPENROUTER_MODELS = {
    "auto":            "google/gemini-3-pro-image-preview",
    "nano-banana":     "google/gemini-3-pro-image-preview",
    "gemini-3-pro":    "google/gemini-3-pro-image-preview",
    "gemini-3-flash":  "google/gemini-3.1-flash-image-preview",
    "gpt-image-2":     "openai/gpt-image-2",
    "flux-2-max":      "black-forest-labs/flux-2-max",
    "imagen-4":        "google/imagen-4.0-generate-001",
    # 🆕 第三方也可调 Qwen / Zhipu via OpenRouter
    "qwen-image":      "qwen/qwen-image-2",
    "cogview-3":       "thudm/cogview-3",
}

PROVIDER_MODELS = {
    Provider.openai: OPENAI_MODELS,
    Provider.google: GOOGLE_MODELS,
    Provider.bailian: BAILIAN_MODELS,
    Provider.zhipu: ZHIPU_MODELS,
    Provider.openrouter: OPENROUTER_MODELS,
}


def resolve_model(provider: Provider, requested: Optional[str]) -> str:
    table = PROVIDER_MODELS.get(provider, {})
    key = requested or "auto"
    if key in table:
        return table[key]
    # 用户写出了完整 model id，原样传递
    return requested


# ===================== Provider dispatch =====================

def _google_generate(req, model, api_key):
    is_imagen = model.startswith("imagen-")
    if is_imagen:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:predict"
        aspect = {"1:1": "1:1", "16:9": "16:9", "9:16": "9:16", "4:3": "4:3", "3:4": "3:4"}.get(req.aspect_ratio, "1:1")
        payload = {"instances": [{"prompt": req.prompt}],
                   "parameters": {"sampleCount": req.n, "aspectRatio": aspect, "personGeneration": "dont_allow"}}
        cost = 0.04 * req.n
    else:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
        payload = {"contents": [{"parts": [{"text": req.prompt}]}],
                   "generationConfig": {"responseModalities": ["TEXT", "IMAGE"]}}
        cost = 0.04 * req.n
    with httpx.Client(timeout=180) as cli:
        r = cli.post(url, headers={"x-goog-api-key": api_key, "Content-Type": "application/json"}, json=payload)
    r.raise_for_status()
    data = r.json()
    if is_imagen:
        png = base64.b64decode(data["predictions"][0]["bytesBase64Encoded"])
    else:
        png = None
        for p in data["candidates"][0]["content"]["parts"]:
            if "inlineData" in p:
                png = base64.b64decode(p["inlineData"]["data"])
                break
        if png is None:
            raise RuntimeError(f"Google response missing image: {data}")
    return ImageResult(png_bytes=png, provider=Provider.google, model=model,
                       used_aspect_ratio=req.aspect_ratio, used_quality=req.quality,
                       cost_estimate_usd=cost)


def _openai_generate(req, model, api_key):
    url = "https://api.openai.com/v1/images/generations"
    size = {"1:1": "1024x1024", "16:9": "1536x1024", "9:16": "1024x1536",
            "4:3": "1536x1024", "3:4": "1024x1536", "21:9": "1792x768"}.get(req.aspect_ratio, "1024x1024")
    payload = {"model": model, "prompt": req.prompt, "size": size,
               "quality": req.quality, "n": req.n if model != "dall-e-3" else 1}
    with httpx.Client(timeout=180) as cli:
        r = cli.post(url, headers={"Authorization": f"Bearer {api_key}"}, json=payload)
    r.raise_for_status()
    items = r.json()["data"]
    first = items[0]
    png = base64.b64decode(first["b64_json"]) if "b64_json" in first else httpx.get(first["url"], timeout=60).content
    cost = 0.08 if (model != "dall-e-3" or req.quality == "hd") else 0.04
    cost *= req.n
    return ImageResult(png_bytes=png, provider=Provider.openai, model=model,
                       used_aspect_ratio=req.aspect_ratio, used_quality=req.quality,
                       cost_estimate_usd=cost)


def _openrouter_generate(req, model, api_key):
    url = "https://openrouter.ai/api/v1/images/generations"
    payload = {"model": model, "prompt": req.prompt, "size": "1024x1024", "n": req.n}
    with httpx.Client(timeout=180) as cli:
        r = cli.post(url, headers={"Authorization": f"Bearer {api_key}"}, json=payload)
    r.raise_for_status()
    data = r.json()
    first = data["data"][0]
    png = base64.b64decode(first["b64_json"]) if "b64_json" in first else httpx.get(first["url"], timeout=60).content
    return ImageResult(png_bytes=png, provider=Provider.openrouter, model=model,
                       used_aspect_ratio=req.aspect_ratio, used_quality=req.quality,
                       cost_estimate_usd=0.04 * req.n)


# 🆕 阿里云百炼 DashScope — OpenAI 兼容接口 `/compatible-mode/v1`
def _bailian_generate(req, model, api_key):
    # 用户可自定义 BAILIAN_BASE_URL（如用户提供的是北京 region）
    base_url = os.getenv("BAILIAN_BASE_URL", "https://dashscope.aliyuncs.com/compatible-mode/v1").rstrip("/")
    url = f"{base_url}/images/generations"
    # 百炼兼容 OpenAI size 参数
    size = {"1:1": "1024x1024", "16:9": "1280x720", "9:16": "720x1280",
            "4:3": "1280x960", "3:4": "960x1280"}.get(req.aspect_ratio, "1024x1024")
    payload = {"model": model, "prompt": req.prompt, "size": size, "n": req.n}
    with httpx.Client(timeout=180) as cli:
        r = cli.post(url, headers={"Authorization": f"Bearer {api_key}"}, json=payload)
    r.raise_for_status()
    data = r.json()
    first = data["data"][0]
    # 百炼兼容模式可能返回 url 或 b64_json
    if "b64_json" in first:
        png = base64.b64decode(first["b64_json"])
    else:
        png = httpx.get(first["url"], timeout=60).content
    # 百炼定价参考：qwen-image 系列约 $0.04/张
    cost = 0.04 * req.n
    return ImageResult(png_bytes=png, provider=Provider.bailian, model=model,
                       used_aspect_ratio=req.aspect_ratio, used_quality=req.quality,
                       cost_estimate_usd=cost)


# 🆕 智谱 BigModel — 自家 API（GLM-Image / CogView 系列）
# 文档: https://bigmodel.cn/dev/api#cogview
# size 必须是 32 的整数倍像素，在 512-2048 px 之间
def _zhipu_generate(req, model, api_key):
    url = "https://open.bigmodel.cn/api/paas/v4/images/generations"
    # Zhipu 仅官方支持 3 个尺寸（实测）：
    #   1024x1024   1:1
    #   768x1344   9:16
    #   1344x768  16:9
    # 长宽必须是 32 的整数倍
    size_map = {
        "1:1":  "1024x1024",
        "16:9": "1344x768",
        "9:16": "768x1344",
        "4:3":  "1152x864",
        "3:4":  "864x1152",
    }
    size = size_map.get(req.aspect_ratio, "1024x1024")
    payload = {
        "model": model,
        "prompt": req.prompt,
        "size": size,
    }
    with httpx.Client(timeout=180) as cli:
        r = cli.post(url, headers={"Authorization": f"Bearer {api_key}"}, json=payload)
    r.raise_for_status()
    data = r.json()
    # 智谱返回结构：data[0].url 或 b64_json
    img_data = data.get("data", [{}])[0]
    if "b64_json" in img_data:
        png = base64.b64decode(img_data["b64_json"])
    else:
        png = httpx.get(img_data["url"], timeout=60).content
    # 智谱定价：CogView-3 约 ¥0.18/张 (≈ $0.025)
    cost = 0.025 * max(req.n, 1)
    return ImageResult(png_bytes=png, provider=Provider.zhipu, model=model,
                       used_aspect_ratio=req.aspect_ratio, used_quality=req.quality,
                       cost_estimate_usd=cost)


class ImageAdapter:
    def __init__(self, provider: Optional[Provider] = None):
        self.provider = provider or detect_provider()
        self._keys = self._load_keys()

    def _load_keys(self) -> dict:
        keys = {}
        env_map = {
            Provider.google:     "GOOGLE_API_KEY",
            Provider.openai:     "OPENAI_API_KEY",
            Provider.bailian:    "BAILIAN_API_KEY",
            Provider.zhipu:      "ZHIPU_API_KEY",
            Provider.openrouter: "OPENROUTER_API_KEY",
        }
        for provider, env_name in env_map.items():
            v = os.getenv(env_name)
            if v:
                keys[provider] = v
        return keys

    def available_providers(self) -> list:
        return list(self._keys.keys())

    def generate(self, req: ImageRequest) -> ImageResult:
        if self.provider not in self._keys:
            raise ImageNotConfiguredError(
                f"Provider {self.provider.value} has no key configured. "
                f"Available: {[p.value for p in self.available_providers()]}"
            )
        model = resolve_model(self.provider, req.model)
        api_key = self._keys[self.provider]
        dispatch = {
            Provider.google:     _google_generate,
            Provider.openai:     _openai_generate,
            Provider.openrouter: _openrouter_generate,
            Provider.bailian:    _bailian_generate,        # 🆕
            Provider.zhipu:      _zhipu_generate,          # 🆕
        }
        fn = dispatch.get(self.provider)
        if fn is None:
            raise RuntimeError(f"Unsupported provider: {self.provider}")
        return fn(req, model, api_key)


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(description="Quickly generate 1 image to verify API keys work.")
    ap.add_argument("--prompt", default="A lone cyclist on a quiet Erhai Lake road at dawn, misty turquoise water, snow-capped mountains, cinematic 8K.")
    ap.add_argument("--aspect-ratio", default="16:9")
    ap.add_argument("--provider", choices=["auto", "openai", "google", "openrouter", "bailian", "zhipu"], default="auto")
    ap.add_argument("--out", default="/tmp/tsc_test.png")
    ap.add_argument("--model", default=None)
    args = ap.parse_args()
    adapter = ImageAdapter(provider=Provider(args.provider)) if args.provider != "auto" else ImageAdapter()
    result = adapter.generate(ImageRequest(prompt=args.prompt, aspect_ratio=args.aspect_ratio, model=args.model))
    open(args.out, "wb").write(result.png_bytes)
    print(f"✅ {args.out} ({len(result.png_bytes):,} bytes) provider={result.provider.value} model={result.model} cost=${result.cost_estimate_usd:.3f}")
