import os, uuid
from PIL import Image, ImageDraw, ImageFont
from typing import List

DATA_DIR = "data"
COMPOSITES_DIR = os.path.join(DATA_DIR, "composites")
EXPORTS_DIR = os.path.join(DATA_DIR, "exports")
os.makedirs(EXPORTS_DIR, exist_ok=True)

PRESETS = {
    "WB_3x4": (1500, 2000),
}

# Try to use a sensible default font
def _load_font(size: int):
    try:
        return ImageFont.truetype("DejaVuSans.ttf", size)
    except Exception:
        return ImageFont.load_default()

def _wrap_text(draw, text, font, max_width):
    words = text.split()
    lines = []
    cur = ""
    for w in words:
        test = (cur + " " + w).strip()
        if draw.textlength(test, font=font) <= max_width:
            cur = test
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def _layout_variant(bg, composite, benefits, variant_idx: int):
    W, H = bg.size
    draw = ImageDraw.Draw(bg)
    title_font = _load_font(64)
    text_font = _load_font(36)

    # Title position varies by variant
    title = "Ключевые преимущества"
    if variant_idx == 0:
        tpos = (80, 80)
    elif variant_idx == 1:
        tpos = (80, H//2 + 40)
    else:
        tpos = (W//2 + 40, 80)

    draw.text(tpos, title, font=title_font, fill=(20,20,20,255))

    # Place composite (product) left/right depending on variant
    if variant_idx == 2:
        prod_pos = (80, 300)
    else:
        prod_pos = (W//2 + 40, 300)

    # Paste product
    layer = Image.new("RGBA", bg.size, (0,0,0,0))
    comp_resized = composite.resize((int(W*0.45), int(composite.height*0.45)), Image.LANCZOS)
    layer.paste(comp_resized, prod_pos, comp_resized.split()[-1])
    bg = Image.alpha_composite(bg, layer)
    draw = ImageDraw.Draw(bg)

    # Benefit bullets in a column
    x = 80 if variant_idx != 2 else W//2 + 40
    y = tpos[1] + 120
    max_width = int(W*0.4)
    for b in benefits[:5]:
        draw.rounded_rectangle([x-10, y-10, x+max_width+10, y+110], radius=12, fill=(255,255,255,220))
        draw.text((x, y), b["title"], font=text_font, fill=(20,20,20,255))
        lines = _wrap_text(draw, b["short_text"], font=text_font, max_width=max_width)
        yy = y + 44
        for ln in lines[:3]:
            draw.text((x, yy), ln, font=text_font, fill=(60,60,60,255))
            yy += 40
        y = yy + 30
    return bg

def generate_variants(composite_id: str, benefits: List[dict], brand: dict, count: int, preset: str):
    size = PRESETS.get(preset, (1500, 2000))
    comp_path = os.path.join(COMPOSITES_DIR, f"{composite_id}.png")
    if not os.path.exists(comp_path):
        raise FileNotFoundError("composite not found")
    product = Image.open(comp_path).convert("RGBA")

    results = []
    for i in range(max(1, min(6, count))):
        canvas = Image.new("RGBA", size, (245, 247, 250, 255))
        variant = _layout_variant(canvas, product, benefits, i)
        vid = str(uuid.uuid4()).replace("-", "")
        out_path = os.path.join(EXPORTS_DIR, f"{vid}.png")
        variant.save(out_path, "PNG")
        results.append({"variant_id": vid, "url": f"/static/exports/{vid}.png", "width": size[0], "height": size[1]})
    return results
