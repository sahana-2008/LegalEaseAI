import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.routes import router


app = FastAPI(

    title="LegalEase API",

    version="1.0.0",

    description=(
        "AI-powered legal document generation API"
    )
)


app.add_middleware(

    CORSMiddleware,

    allow_origins=["*"],

    allow_credentials=False,

    allow_methods=["GET", "POST"],

    allow_headers=["*"]
)


app.include_router(router)


@app.get("/")
def root():

    return {

        "name": "LegalEase",

        "status": "running",

        "message": "LegalEase backend is running.",

        "docs": "/docs",

        "health": "/health"
    }


@app.get("/health")
def health():

    gemini_configured = bool(
        os.getenv(
            "GEMINI_API_KEY",
            ""
        ).strip()
    )

    return {

        "status": "ok",

        "gemini_configured":
            gemini_configured,

        "model":
            os.getenv(
                "GEMINI_MODEL",
                "gemini-3.8-flash"
            )
    }