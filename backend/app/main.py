import os
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles  # ✅ добавлено
from pydantic_settings import BaseSettings

from app.background_service import remove_bg_replicate
from app.routes import upload, vision, nlp, card, validate


class Settings(BaseSettings):
    CORS_ORIGINS: str = "*"


settings = Settings()

app = FastAPI()

# ✅ CORS — разрешаем фронту общаться с API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # позже можно заменить на ["https://wb-cardgen.vercel.app"]
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Статика — важно! путь к экспортам
app.mount("/static", StaticFiles(directory="data/static"), name="static")

# ✅ Роуты
app.include_router(upload.router, prefix="/upload")
app.include_router(vision.router, prefix="/vision")
app.include_router(nlp.router, prefix="/nlp")
app.include_router(card.router, prefix="/card")
app.include_router(validate.router, prefix="/validate")

REPLICATE_API_KEY = os.getenv("REPLICATE_API_KEY")


@app.post("/remove-bg")
async def remove_background(file: UploadFile = File(...)):
    if not REPLICATE_API_KEY:
        return {"error": "REPLICATE_API_KEY not set"}

    image_bytes = await file.read()
    result_bytes = remove_bg_replicate(image_bytes, REPLICATE_API_KEY)
    return Response(content=result_bytes, media_type="image/png")
