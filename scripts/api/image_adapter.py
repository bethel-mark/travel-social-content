"""Image generation adapter — unified interface across 4 major providers.

Supported providers (auto-detected from environment variables):
  - OpenAI  (GPT Image 2 / DALL-E 3)
  - Google AI Studio (Gemini 3 Pro Image / Gemini 3.1 Flash / Imagen 4)
  - OpenRouter (100+ models via unified OpenAI-compatible endpoint)

Plus Vertex AI fallback documented in comment.

Usage:
    >>> from scripts.api.image_adapter import ImageAdapter, ImageRequest
    >>> adapter = ImageAdapter()
    >>> req = ImageRequest(
    ...     prompt="Mount Hua at sunrise, sea of clouds",
    ...     aspect_ratio="16:9",
    ...     quality="high",
    ...     n=1,
    ... )
    >>> png_bytes = adapter.generate(req)
    >>> open("out.png", "wb").write(png_bytes)

Detection order:
  1. GOOGLE_API_KEY       → provider="google" (default)
  2. OPENAI_API_KEY       → provider="openai"
  3. OPENROUTER_API_KEY   → provider="openrouter"
  4. (none)               → raises ImageNotConfiguredError
"""
from __future__ import annotations

import base64
import os
import sys
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

try:
    import httpx
except ImportError:
    httpx = None
    import urllib.request, urllib.error
    class _UrllibClient:
        """Minimal httpx-compatible wrapper using urllib, used when httpx missing."""
        def __init__(self, timeout=60):
            self.timeout = timeout
        def post(self, url, headers=None, json=None):
            req = urllib.request.Request(url, headers=headers or {}, method='POST')
            data = json and json.__class__.__module__ == 'builtins' and json or json
            import json as _json
            raw = _json.dumps(data).encode() if data else None
            if raw: req.add_header('Content-Type','application/json')
            try:
                resp = urllib.request.urlopen(req, data=raw, timeout=self.timeout)
                return _UrlResp(resp.status, resp.read(), dict(resp.headers))
            except urllib.error.HTTPError as e:
                return _UrlResp(e.code, e.read(), dict(e.headers or {}))
        def get(self, url, timeout=60):
            try:
                resp = urllib.request.urlopen(url, timeout=timeout)
                return _UrlResp(resp.status, resp.read(), dict(resp.headers))
            except urllib.error.HTTPError as e:
                return _UrlResp(e.code, e.read(), dict(e.headers or {}))
        def __enter__(self): return self
        def __exit__(self, *a): return False
    class _UrlResp:
        def __init__(self, status_code, content, headers):
            self.status_code = status_code
            self._content = content
            self.headers = headers
        def json(self): import json; return json.loads(self._content)
        def raise_for_status(self):
            if self.status_code >= 400:
                raise RuntimeError(f"HTTP {self.status_code}: {self._content!r}")
        @property
        def content(self): return self._content
    if httpx is None:
        httpx = _UrllibClient


class ImageNotConfiguredError(RuntimeError):
    """Raised when no image-generation API key is configured."""


class Provider(str, Enum):
    openai = "openai"
    google = "google"
    openrouter = "openrouter"


@dataclass
class ImageRequest:
    prompt: str
    aspect_ratio: str = "1:1"          # "1:1", "16:9", "9:16", "4:3", "3:4", "21:9"
    quality: str = "high"             # "low" / "medium" / "high" / "auto"
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


# ===================== Provider detection =====================

def detect_provider() -> Provider:
    """Pick the first provider that has a key configured.

    Override with TSC_IMAGE_PROVIDER env var:
        TSC_IMAGE_PROVIDER=openai|google|openrouter
    """
    forced = os.getenv("TSC_IMAGE_PROVIDER", "").lower().strip()
    if forced in {"openai", "google", "openrouter"}:
        return Provider(forced)
    if os.getenv("GOOGLE_API_KEY"):
        return Provider.google
    if os.getenv("OPENAI_API_KEY"):
        return Provider.openai
    if os.getenv("OPENROUTER_API_KEY"):
        return Provider.openrouter
    raise ImageNotConfiguredError(
        "No image-generation key found. Set one of:\n"
        "  GOOGLE_API_KEY (Gemini/Imagen)\n"
        "  OPENAI_API_KEY (GPT Image 2/DALL-E 3)\n"
        "  OPENROUTER_API_KEY (100+ models)\n"
        "Or override via TSC_IMAGE_PROVIDER env."
    )


# ===================== Endpoint configs =====================

GOOGLE_MODELS = {
    # default model aliases → real model ids
    "auto":                "gemini-3-pro-image-preview",
    "nano-banana":         "gemini-3-pro-image-preview",  # internal codename
    "gemini-3-pro":        "gemini-3-pro-image-preview",
    "gemini-3-flash":      "gemini-3.1-flash-image-preview",
    "imagen-4":            "imagen-4.0-generate-001",
}

OPENAI_MODELS = {
    "auto":     "gpt-image-2",
    "gpt-img-2":  "gpt-image-2",
    "gpt-image-2": "gpt-image-2",
    "dall-e-3":   "dall-e-3",
}

OPENROUTER_MODELS = {
    "auto":        "google/gemini-3-pro-image-preview",
    "nano-banana": "google/gemini-3-pro-image-preview",
    "gemini-3-pro":"google/gemini-3-pro-image-preview",
    "gemini-3-flash": "google/gemini-3.1-flash-image-preview",
    "gpt-image-2": "openai/gpt-image-2",
    "flux-2-max":    "black-forest-labs/flux-2-max",
    "imagen-4":      "google/imagen-4.0-generate-001",
}


def resolve_model(provider: Provider, requested: Optional[str]) -> str:
    table = {"openai": OPENAI_MODELS, "google": GOOGLE_MODELS, "openrouter": OPENROUTER_MODELS}
    key = requested or "auto"
    return table[provider].get(key, requested)  # fallback: pass through user-supplied


# ===================== Async API calls =====================

def _google_generate(req: ImageRequest, model: str, api_key: str) -> ImageResult:
    """Call Gemini 3 Pro Image / Imagen 4 via Google AI Studio."""
    is_imagen = model.startswith("imagen-")

    if is_imagen:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:predict"
        aspect_map = {"1:1": "1:1", "16:9": "16:9", "9:16": "9:16", "4:3": "4:3", "3:4": "3:4"}
        payload = {
            "instances": [{"prompt": req.prompt}],
            "parameters": {
                "sampleCount": req.n,
                "aspectRatio": aspect_map.get(req.aspect_ratio, "1:1"),
                "personGeneration": "dont_allow",
            },
        }
        cost = 0.04 * req.n
    else:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
        payload = {
            "contents": [{"parts": [{"text": req.prompt}]}],
            "generationConfig": {"responseModalities": ["TEXT", "IMAGE"]},
        }
        cost = 0.04 * req.n  # rough estimate for image output tokens

    with httpx(timeout=180) as cli:
        r = cli.post(url,
                     headers={"x-goog-api-key": api_key, "Content-Type": "application/json"},
                     json=payload)
    r.raise_for_status()
    data = r.json()

    # Imagen: b64 in predictions[0].bytesBase64Encoded
    if is_imagen:
        png = base64.b64decode(data["predictions"][0]["bytesBase64Encoded"])
    else:
        # Gemini 3 Pro Image: b64 in candidates[0].content.parts[].inlineData.data
        parts = data["candidates"][0]["content"]["parts"]
        png = None
        for p in parts:
            if "inlineData" in p:
                png = base64.b64decode(p["inlineData"]["data"])
                break
        if png is None:
            raise RuntimeError(f"Google response missing image: {data}")

    return ImageResult(png_bytes=png, provider=Provider.google, model=model,
                       used_aspect_ratio=req.aspect_ratio,
                       used_quality=req.quality, cost_estimate_usd=cost)


def _openai_generate(req: ImageRequest, model: str, api_key: str) -> ImageResult:
    """Call OpenAI GPT Image 2 / DALL-E 3."""
    url = "https://api.openai.com/v1/images/generations"
    size_map = {
        "1:1":  "1024x1024",
        "16:9": "1536x1024",
        "9:16": "1024x1536",
        "4:3":  "1536x1024",
        "3:4":  "1024x1536",
        "21:9": "1792x768",
    }
    payload = {
        "model": model,
        "prompt": req.prompt,
        "size": size_map.get(req.aspect_ratio, "1024x1024"),
        "quality": req.quality,
        "n": req.n,
    }
    if req.model == "dall-e-3":
        # dall-e-3 only supports n=1
        payload["n"] = 1

    with httpx.Client(timeout=180) as cli:
        r = cli.post(url,
                     headers={"Authorization": f"Bearer {api_key}"},
                     json=payload)
    r.raise_for_status()
    items = r.json()["data"]

    # OpenAI returns URL or b64_json depending on model/option
    png = None
    first = items[0]
    if "b64_json" in first:
        png = base64.b64decode(first["b64_json"])
    elif "url" in first:
        png = httpx.get(first["url"], timeout=60).content
    else:
        raise RuntimeError(f"OpenAI response missing image data: {first}")

    cost = (0.08 if model != "dall-e-3" or req.quality == "hd" else 0.04) * req.n
    return ImageResult(png_bytes=png, provider=Provider.openai, model=model,
                       used_aspect_ratio=req.aspect_ratio,
                       used_quality=req.quality, cost_estimate_usd=cost)


def _openrouter_generate(req: ImageRequest, model: str, api_key: str) -> ImageResult:
    """Call OpenRouter (OpenAI-compatible). Supports 100+ models."""
    url = "https://openrouter.ai/api/v1/images/generations"
    payload = {
        "model": model,
        "prompt": req.prompt,
        "size": "1024x1024",          # OpenRouter passthrough — model-dependent
        "n": req.n,
    }
    with httpx.Client(timeout=180) as cli:
        r = cli.post(url,
                     headers={"Authorization": f"Bearer {api_key}"},
                     json=payload)
    r.raise_for_status()
    data = r.json()

    # Handle both b64_json and url responses
    first = data["data"][0]
    if "b64_json" in first:
        png = base64.b64decode(first["b64_json"])
    elif "url" in first:
        png = httpx.get(first["url"], timeout=60).content
    else:
        raise RuntimeError(f"OpenRouter response missing image data: {first}")

    cost = 0.04 * req.n  # rough average across providers
    return ImageResult(png_bytes=png, provider=Provider.openrouter, model=model,
                       used_aspect_ratio=req.aspect_ratio,
                       used_quality=req.quality, cost_estimate_usd=cost)


# ===================== Main public API =====================

class ImageAdapter:
    """High-level adapter: hides provider detection + dispatch."""

    def __init__(self, provider: Optional[Provider] = None):
        self.provider = provider or detect_provider()
        self._keys = self._load_keys()

    def _load_keys(self) -> dict:
        keys = {}
        if os.getenv("GOOGLE_API_KEY"):
            keys[Provider.google] = os.environ["GOOGLE_API_KEY"]
        if os.getenv("OPENAI_API_KEY"):
            keys[Provider.openai] = os.environ["OPENAI_API_KEY"]
        if os.getenv("OPENROUTER_API_KEY"):
            keys[Provider.openrouter] = os.environ["OPENROUTER_API_KEY"]
        return keys

    def available_providers(self) -> list[Provider]:
        return list(self._keys.keys())

    def generate(self, req: ImageRequest) -> ImageResult:
        if self.provider not in self._keys:
            raise ImageNotConfiguredError(
                f"Provider {self.provider.value} has no key configured. "
                f"Available: {[p.value for p in self.available_providers()]}"
            )
        model = resolve_model(self.provider, req.model)
        api_key = self._keys[self.provider]

        if self.provider == Provider.google:
            return _google_generate(req, model, api_key)
        if self.provider == Provider.openai:
            return _openai_generate(req, model, api_key)
        if self.provider == Provider.openrouter:
            return _openrouter_generate(req, model, api_key)
        raise RuntimeError(f"Unsupported provider: {self.provider}")


# ===================== CLI for quick testing =====================

if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(description="Quickly generate 1 image to verify API keys work.")
    ap.add_argument("--prompt", default="A lone cyclist on a quiet road by Erhai Lake in Dali, Yunnan, at dawn, misty turquoise water, snow-capped mountains, cinematic photography, 8K.")
    ap.add_argument("--aspect-ratio", default="16:9")
    ap.add_argument("--provider", choices=["auto", "google", "openai", "openrouter"], default="auto")
    ap.add_argument("--out", default="/tmp/tsc_test.png")
    ap.add_argument("--model", default=None, help="Model alias (e.g. nano-banana, gpt-image-2, imagen-4)")
    args = ap.parse_args()

    if args.provider != "auto":
        adapter = ImageAdapter(provider=Provider(args.provider))
    else:
        adapter = ImageAdapter()

    req = ImageRequest(prompt=args.prompt,
                       aspect_ratio=args.aspect_ratio,
                       model=args.model)
    result = adapter.generate(req)
    open(args.out, "wb").write(result.png_bytes)
    print(f"✅ Saved {args.out} ({len(result.png_bytes):,} bytes)")
    print(f"   provider: {result.provider.value}")
    print(f"   model:    {result.model}")
    print(f"   cost:     ~${result.cost_estimate_usd:.3f}")
