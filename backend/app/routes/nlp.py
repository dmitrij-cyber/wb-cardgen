from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Optional
from ..services.classifier import classify
from ..services.textgen import generate_benefits

router = APIRouter()

class ClassifyIn(BaseModel):
    title: Optional[str] = None

@router.post("/classify_category")
def classify_category(body: ClassifyIn):
    cat, conf, top3 = classify(body.title or "")
    return {"category_id": cat, "confidence": conf, "top3": top3}

class GenBenefitsIn(BaseModel):
    category_id: str
    tone: str = "concise"
    max_items: int = 5

@router.post("/generate_benefits")
def gen_benefits(body: GenBenefitsIn):
    items = generate_benefits(body.category_id, tone=body.tone, max_items=body.max_items)
    return {"items": items}
