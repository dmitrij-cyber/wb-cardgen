import os, json, uuid
from PIL import Image, ImageDraw

DATA_DIR = "data"
BG_DIR = os.path.join(DATA_DIR, "backgrounds")
os.makedirs(BG_DIR, exist_ok=True)

# Predefined styles (can be extended/admin-managed later)
STYLES = [
    {"kind": "solid", "name": "Clean White", "color": (250,250,250)},
    {"kind": "solid", "name": "Soft Gray", "color": (238,240,242)},
    {"kind": "gradient", "name": "Lilac Mist", "from": (240,235,255), "to": (255,255,255)},
    {"kind": "gradient", "name": "Warm Sand", "from": (255,246,234), "to": (255,255,255)},
    {"kind": "gradient", "name": "Mint Breeze", "from": (230,255,245), "to": (255,255,255)},
]

def suggest_backgrounds(width=1500, height=2000, palette=None):
    items = []
    for i, s in enumerate(STYLES):
        bg_id = f"bg_{s['kind']}_{i}_{width}x{height}"
        items.append({
            "bg_id": bg_id,
            "name": s["name"],
            "preview_url": f"/static/backgrounds/{bg_id}.png",
            "kind": s["kind"]
        })
        # Pre-render on demand
        render_background(bg_id, width, height)
    return items

def render_background(bg_id: str, width=None, height=None):
    # bg_id encoded as bg_kind_index_WxH
    parts = bg_id.split("_")
    kind = parts[1]
    idx = int(parts[2])
    size_part = parts[3]
    W, H = map(int, size_part.split("x"))
    path = os.path.join(BG_DIR, f"{bg_id}.png")
    if os.path.exists(path):
        return path
    style = STYLES[idx]
    im = Image.new("RGBA", (W, H), (255,255,255,255))
    if kind == "solid":
        c = style["color"]
        im = Image.new("RGBA", (W, H), (c[0], c[1], c[2], 255))
    else:
        # vertical gradient
        top = style["from"]
        bottom = style["to"]
        for y in range(H):
            t = y / max(1, H-1)
            r = int(top[0]*(1-t) + bottom[0]*t)
            g = int(top[1]*(1-t) + bottom[1]*t)
            b = int(top[2]*(1-t) + bottom[2]*t)
            for x in range(W):
                im.putpixel((x,y), (r,g,b,255))
    im.save(path, "PNG")
    return path
