import os
from background_service import remove_bg_replicate
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import Response
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles
from pydantic_settings import BaseSettings
from .routes import upload, vision, nlp, card, validate

class Settings(BaseSettings):
    CORS_ORIGINS: str = "http://localhost:3000"

settings = Settings()

app = FastAPI()

REPLICATE_API_KEY = os.getenv("REPLICATE_API_KEY")

@app.post("/remove-bg")
async def remove_background(file: UploadFile = File(...)):
    if not REPLICATE_API_KEY:
        return {"error": "REPLICATE_API_KEY not set"}

    image_bytes = await file.read()

    result_bytes = remove_bg_replicate(image_bytes, REPLICATE_API_KEY)
    return Response(content=result_bytes, media_type="image/png")
