from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.core.config import settings
from backend.routers import story, job
from backend.db.database import create_tables

create_tables()

app = FastAPI(
    title="Choose Your Own Adventure Game API",
    description="api to generate cool stories using FREE Groq API",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS - allow all origins if ALLOWED_ORIGINS not configured
allowed_origins = settings.ALLOWED_ORIGINS if settings.ALLOWED_ORIGINS else ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(story.router, prefix=settings.API_PREFIX)
app.include_router(job.router, prefix=settings.API_PREFIX)


@app.get("/")
def root():
    return {
        "message": "Choose Your Own Adventure API",
        "status": "running",
        "using": "Groq (FREE)",
        "docs": "/docs"
    }


@app.get("/health")
def health():
    return {"status": "healthy", "api": "groq"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)