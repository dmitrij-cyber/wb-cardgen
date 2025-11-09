import uuid, os, io
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from PIL import Image, ImageFilter, ImageDraw
from ..services.background import remove_background_safe
from ..services.background_suggest import suggest_backgrounds, render_background

router = APIRouter()
DATA_DIR = "data"
ASSETS_DIR = os.path.join(DATA_DIR, "assets")
CUTOUTS_DIR = os.path.join(DATA_DIR, "cutouts")
COMPOSITES_DIR = os.path.join(DATA_DIR, "composites")

class RemoveBackgroundIn(BaseModel):
    file_id: str

@router.post("/remove_background")
def remove_background(body: RemoveBackgroundIn):
    src_path = os.path.join(ASSETS_DIR, f"{body.file_id}.jpg")
    if not os.path.exists(src_path):
        raise HTTPException(404, detail="file_id not found")
    cut_id, cut_url, w, h = remove_background_safe(src_path, CUTOUTS_DIR)
    return {"cutout_id": cut_id, "url": cut_url, "width": w, "height": h}

class SuggestBackgroundsIn(BaseModel):
    width: int = 1500
    height: int = 2000
    palette: list[str] | None = None

@router.post("/suggest_backgrounds")
def suggest_bg(body: SuggestBackgroundsIn):
    return {"items": suggest_backgrounds(width=body.width, height=body.height, palette=body.palette)}

class ComposeIn(BaseModel):
    cutout_id: str
    bg_id: str
    lighting_dir: float = 135.0  # degrees
    shadow_strength: float = 0.35
    shadow_blur: int = 45
    offset_x: int = 0
    offset_y: int = 0
    scale: float = 0.9

@router.post("/compose")
def compose(body: ComposeIn):
    cut_path = os.path.join(CUTOUTS_DIR, f"{body.cutout_id}.png")
    if not os.path.exists(cut_path):
        raise HTTPException(404, detail="cutout_id not found")

    # Render background image by id (or load cached)
    bg_path = render_background(body.bg_id)

    # Compose
    out_id = str(uuid.uuid4()).replace("-", "")
    out_path = os.path.join(COMPOSITES_DIR, f"{out_id}.png")

    bg = Image.open(bg_path).convert("RGBA")
    fg = Image.open(cut_path).convert("RGBA")

    # scale foreground
    W, H = bg.size
    target_w = int(W * body.scale)
    ratio = target_w / fg.width
    fg_resized = fg.resize((target_w, int(fg.height * ratio)), Image.LANCZOS)

    # create shadow under object (simple oval blur)
    shadow = Image.new("RGBA", bg.size, (0,0,0,0))
    draw = ImageDraw.Draw(shadow)
    bbox_w = int(fg_resized.width * 0.8)
    bbox_h = int(fg_resized.height * 0.12)
    cx, cy = W//2 + body.offset_x, int(H*0.75) + body.offset_y
    shadow_box = [cx - bbox_w//2, cy - bbox_h//2, cx + bbox_w//2, cy + bbox_h//2]
    draw.ellipse(shadow_box, fill=(0,0,0,int(255*body.shadow_strength)))
    shadow = shadow.filter(ImageFilter.GaussianBlur(radius=body.shadow_blur))

    composed = Image.alpha_composite(bg, shadow)

    # paste object
    top_left = (cx - fg_resized.width//2, cy - fg_resized.height)
    layer = Image.new("RGBA", composed.size, (0,0,0,0))
    layer.paste(fg_resized, top_left, mask=fg_resized.split()[-1])
    composed = Image.alpha_composite(composed, layer)

    composed.save(out_path, "PNG")
    return {"composite_id": out_id, "url": f"/static/composites/{out_id}.png", "width": W, "height": H}
