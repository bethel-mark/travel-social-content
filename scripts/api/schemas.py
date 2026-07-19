"""Pydantic request/response models for the generation API."""
from __future__ import annotations

from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class Platform(str, Enum):
    xiaohongshu = "xiaohongshu"
    instagram = "instagram"
    wechat_moments = "wechat_moments"
    weibo = "weibo"
    douyin = "douyin"
    all_platforms = "all"


class Style(str, Enum):
    series_checkin = "系列打卡型"
    emotion_resonance = "情绪共鸣型"
    contrast_hook = "反差吸引型"
    numeric_playbook = "数字攻略型"
    immersive_script = "沉浸脚本型"


class GenerateRequest(BaseModel):
    destination: str = Field(..., min_length=1, max_length=80, description="目的地景点或城市名")
    platform: Platform = Platform.xiaohongshu
    style: Style = Style.contrast_hook
    secondary_styles: Optional[list[Style]] = Field(default=None, description="可选：额外的文案风格，最多 2 个")
    num_image_prompts: int = Field(default=3, ge=1, le=9, description="AI 生图 Prompt 数量，1-9")
    include_search: bool = Field(default=True, description="是否检索，True 会调用 search-destination.sh")
    language: str = Field(default="zh", pattern=r"^(zh|en|both)$")


class GenerateResponse(BaseModel):
    status: str  # 'ok' | 'needs_llm' | 'error'
    destination: str
    platform: Platform
    style: Style
    markdown: Optional[str] = None
    prompt_to_llm: Optional[str] = None
    raw_search: Optional[str] = None
    skill_version: str = "1.0.0"
    warnings: list[str] = Field(default_factory=list)
    references_used: list[str] = Field(default_factory=list)


class HealthResponse(BaseModel):
    status: str
    version: str
    llm_configured: bool
    search_available: bool
