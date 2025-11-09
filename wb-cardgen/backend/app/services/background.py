import os, uuid
from PIL import Image
from rembg import remove

def remove_background_safe(src_path: str, out_dir: str):
    os.makedirs(out_dir, exist_ok=True)
    out_id = str(uuid.uuid4()).replace("-", "")
    out_path = os.path.join(out_dir, f"{out_id}.png")
    try:
        src = Image.open(src_path).convert("RGBA")
        result = remove(src)  # returns RGBA PIL.Image
        result.save(out_path, "PNG")
    except Exception:
        # Fallback: just copy RGB as RGBA (no real background removal)
        src = Image.open(src_path).convert("RGBA")
        src.save(out_path, "PNG")
    return out_id, f"/static/cutouts/{out_id}.png", src.width, src.height
