"""FastAPI server exposing the SKILL.md workflow as REST endpoints."""
from __future__ import annotations

import os
import sys
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

# Allow running with `python scripts/api/server.py`
sys.path.insert(0, str(Path(__file__).resolve().parent))

from generator import assemble_full_prompt_only  # noqa: E402
from llm_adapter import detect_llm, generate  # noqa: E402
from image_adapter import (  # noqa: E402
    ImageAdapter, ImageRequest, ImageNotConfiguredError,
    Provider as ImageProvider,
)

from schemas import (  # noqa: E402
    GenerateRequest,
    GenerateResponse,
    HealthResponse,
)


app = FastAPI(
    title="travel-social-content API",
    description="Expose the SKILL.md workflow as an HTTP API. "
                "Generate complete travel social-media content plans "
                "for any Chinese/foreign destination.",
    version="1.0.0",
)


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    cfg = detect_llm()
    search_ok = (Path(__file__).resolve().parents[2] / "scripts" / "search-destination.sh").exists()
    return HealthResponse(
        status="ok",
        version="1.0.0",
        llm_configured=cfg.provider != "none",
        search_available=search_ok,
    )


@app.post("/api/v1/generate", response_model=GenerateResponse)
def generate_content(req: GenerateRequest) -> GenerateResponse:
    cfg = detect_llm()
    secondary = [s.value if hasattr(s, "value") else str(s) for s in (req.secondary_styles or [])]

    built = assemble_full_prompt_only(
        destination=req.destination,
        platform=req.platform.value if hasattr(req.platform, "value") else str(req.platform),
        style=req.style.value if hasattr(req.style, "value") else str(req.style),
        secondary_styles=secondary,
        num_image_prompts=req.num_image_prompts,
        language=req.language,
        include_search=req.include_search,
    )

    if cfg.provider == "none":
        return GenerateResponse(
            status="needs_llm",
            destination=req.destination,
            platform=req.platform,
            style=req.style,
            markdown=None,
            prompt_to_llm=built["prompt"],
            raw_search=built["raw_search"],
            warnings=[
                "No LLM API key configured. Set ANTHROPIC_API_KEY / OPENAI_API_KEY "
                "/ DEEPSEEK_API_KEY environment variable to enable automatic generation.",
                "Otherwise copy `prompt_to_llm` into any AI assistant that supports "
                "the same prompt format.",
            ],
            references_used=[
                "SKILL.md",
                "references/output-template.md",
                "references/destinations.md",
            ],
        )

    try:
        markdown = generate(built["prompt"], cfg, max_tokens=6000)
    except Exception as exc:  # noqa: BLE001
        return JSONResponse(
            status_code=502,
            content={
                "status": "error",
                "destination": req.destination,
                "error": f"{type(exc).__name__}: {exc}",
                "prompt_to_llm": built["prompt"],
            },
        )

    return GenerateResponse(
        status="ok",
        destination=req.destination,
        platform=req.platform,
        style=req.style,
        markdown=markdown,
        prompt_to_llm=None,
        raw_search=built["raw_search"],
        skill_version="1.0.0",
        warnings=[],
        references_used=["SKILL.md", "references/output-template.md", "LLM: " + cfg.provider + "/" + cfg.model],
    )


@app.get("/api/v1/destinations")
def list_destinations() -> dict:
    """Return a list of destinations covered by the cached cheat-sheet."""
    cheat = Path(__file__).resolve().parents[2] / "references" / "destinations.md"
    if not cheat.exists():
        return {"destinations": []}
    text = cheat.read_text(encoding="utf-8")
    names = []
    for line in text.splitlines():
        if line.startswith("### "):
            names.append(line[4:].strip())
    return {"destinations": names[:60]}


class ImageGenerateRequest(BaseModel):
    prompt: str = Field(..., min_length=1, max_length=4000)
    aspect_ratio: str = Field(default="1:1")
    quality: str = Field(default="high")
    n: int = Field(default=1, ge=1, le=4)
    model: Optional[str] = None
    provider: Optional[str] = None


class ImageGenerateResponse(BaseModel):
    status: str
    provider: Optional[str] = None
    model: Optional[str] = None
    png_base64: Optional[str] = None
    size_bytes: int = 0
    cost_estimate_usd: float = 0.0
    error: Optional[str] = None


@app.post("/api/v1/generate-image", response_model=ImageGenerateResponse)
def generate_image(req: ImageGenerateRequest):
    """Generate image. Auto-detects provider from env: GOOGLE / OPENAI / OPENROUTER."""
    forced = req.provider
    try:
        if forced and forced != "auto":
            adapter = ImageAdapter(provider=ImageProvider(forced))
        else:
            adapter = ImageAdapter()
    except (ValueError, ImageNotConfiguredError) as exc:
        return ImageGenerateResponse(status="not_configured", error=str(exc))
    try:
        result = adapter.generate(ImageRequest(
            prompt=req.prompt, aspect_ratio=req.aspect_ratio,
            quality=req.quality, n=req.n, model=req.model,
        ))
    except Exception as exc:
        return ImageGenerateResponse(status="error", error=f"{type(exc).__name__}: {exc}")
    import base64
    return ImageGenerateResponse(
        status="ok", provider=result.provider.value, model=result.model,
        png_base64=base64.b64encode(result.png_bytes).decode("ascii"),
        size_bytes=len(result.png_bytes),
        cost_estimate_usd=result.cost_estimate_usd,
    )


if __name__ == "__main__":
    import uvicorn
    host = os.getenv("API_HOST", "0.0.0.0")
    port = int(os.getenv("API_PORT", "8000"))
    uvicorn.run(app, host=host, port=port)
