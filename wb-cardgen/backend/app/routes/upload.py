import uuid, os
from fastapi import APIRouter, UploadFile, File, HTTPException
from PIL import Image
from typing import List

router = APIRouter()

ASSETS_DIR = "data/assets"

@router.post("/upload")
async def upload_files(files: List[UploadFile] = File(...)):
    saved = []
    for f in files:
        suffix = ".jpg"
        try:
            im = Image.open(f.file).convert("RGB")
        except Exception:
            raise HTTPException(400, detail=f"Не удалось прочитать файл: {f.filename}")
        file_id = str(uuid.uuid4()).replace("-", "")
        out_path = os.path.join(ASSETS_DIR, f"{file_id}{suffix}")
        im.save(out_path, "JPEG", quality=92, optimize=True)
        saved.append({
            "file_id": file_id,
            "url": f"/static/assets/{file_id}{suffix}",
            "width": im.width,
            "height": im.height,
            "format": "JPEG"
        })
    return {"items": saved}
