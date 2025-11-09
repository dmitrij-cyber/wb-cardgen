import os
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles
from pydantic_settings import BaseSettings

from .background_service import remove_bg_replicate
from .routes import upload, vision, nlp, card, validate

class Settings(BaseSettings):
    CORS_ORIGINS: str = "*"

settings = Settings()

app = FastAPI()

# CORS — важно для фронта
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.CORS_ORIGINS, "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Подключаем маршруты
app.include_router(upload.router)
app.include_router(vision.router)
app.include_router(nlp.router)
app.include_router(card.router)
app.include_router(validate.router)

REPLICATE_API_KEY = os.getenv("REPLICATE_API_KEY")

@app.post("/remove-bg")
async def remove_background(file: UploadFile = File(...)):
    if not REPLICATE_API_KEY:
        return {"error": "REPLICATE_API_KEY not set"}

    image_bytes = await file.read()

    result_bytes = remove_bg_replicate(image_bytes, REPLICATE_API_KEY)
    return Response(content=result_bytes, media_type="image/png")

# ✅ Важно: НЕ запускать uvicorn.run здесь!
