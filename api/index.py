# api/index.py - Vercel Serverless Function Entry Point
# This file adapts your FastAPI app to work with Vercel's serverless functions

from fastapi import FastAPI
from mangum import Mangum

# Import your main FastAPI app
# Adjust the import based on your project structure
try:
    from main import app  # If main.py is in root
except ImportError:
    try:
        from ..main import app  # If main.py is elsewhere
    except ImportError:
        # If you need to create the app here
        app = FastAPI()
        
        @app.get("/")
        def read_root():
            return {"message": "StoryForge API"}
        
        @app.get("/health")
        def health_check():
            return {"status": "healthy"}

# Add CORS middleware
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://*.vercel.app",  # Allow all Vercel preview deployments
        "https://your-custom-domain.com"  # Add your custom domain
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Wrap FastAPI app with Mangum for AWS Lambda/Vercel compatibility
handler = Mangum(app)