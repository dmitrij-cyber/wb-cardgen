import uuid, os
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from ..services.cardgen import generate_variants

router = APIRouter()
EXPORTS_DIR = "data/exports"

class CardGenerateIn(BaseModel):
    composite_id: str
    benefits: List[dict]  # {title, short_text}
    brand: dict | None = None  # palette, font, logo?
    count: int = 3
    size_preset: str = "WB_3x4"

@router.post("/generate")
def generate(body: CardGenerateIn):
    items = generate_variants(
        composite_id=body.composite_id,
        benefits=body.benefits,
        brand=body.brand or {},
        count=body.count,
        preset=body.size_preset
    )
    return {"variants": items}

class RenderIn(BaseModel):
    variant_ids: List[str]
    format: str = "png"  # png | jpg
    quality: int = 95

@router.post("/render")
def render(body: RenderIn):
    # Variанты уже рендерятся как PNG и лежат в exports
    results = []
    for vid in body.variant_ids:
        p = os.path.join(EXPORTS_DIR, f"{vid}.png")
        if not os.path.exists(p):
            raise HTTPException(404, detail=f"variant {vid} not found")
        url = f"/static/exports/{vid}.png"
        results.append({"variant_id": vid, "url": url})
    return {"items": results}
