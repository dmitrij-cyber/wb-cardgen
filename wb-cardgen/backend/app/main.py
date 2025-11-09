from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles
from pydantic_settings import BaseSettings
from .routes import upload, vision, nlp, card, validate

class Settings(BaseSettings):
    CORS_ORIGINS: str = "http://localhost:3000"

settings = Settings()

app = FastAPI(title="WB Card Generator API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in settings.CORS_ORIGINS.split(",")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(upload.router, prefix="/media", tags=["media"])
app.include_router(vision.router, prefix="/vision", tags=["vision"])
app.include_router(nlp.router, prefix="/nlp", tags=["nlp"])
app.include_router(card.router, prefix="/card", tags=["card"])
app.include_router(validate.router, prefix="/validate", tags=["validate"])

# Static: serve generated files under /static
app.mount("/static", StaticFiles(directory="data"), name="static")

@app.get("/", tags=["meta"])
def root():
    return {"ok": True, "service": "wb-cardgen", "docs": "/docs"}
