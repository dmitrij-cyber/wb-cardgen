import os
from fastapi import APIRouter
from pydantic import BaseModel
from PIL import Image

router = APIRouter()

PRESETS = {
    "WB_Main": (1600, 1600),
    "WB_3x4": (1500, 2000),
}

class ValidateIn(BaseModel):
    path: str  # /static/exports/xxx.png
    preset: str = "WB_3x4"

@router.post("/validate")  # или "/" если используешь prefix="/validate"
def validate_card(body: ValidateIn):
    if not body.path.startswith("/static/"):
        return {"ok": False, "errors": ["path must start with /static/"]}

    local = "data" + body.path[7:]
    if not os.path.exists(local):
        return {"ok": False, "errors": ["file not found"]}

    w, h = PRESETS.get(body.preset, (1500, 2000))
    im = Image.open(local)

    errors = []
    if im.size != (w, h):
        errors.append(f"size must be {w}x{h}, got {im.width}x{im.height}")

    return {"ok": len(errors)==0, "errors": errors, "warnings": []}
