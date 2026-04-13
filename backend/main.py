"""
PropAI Backend - Main FastAPI Application
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import os

from models.database import init_db, SessionLocal
from api.routes import router as api_router

# Initialize database on startup
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup event
    print("🚀 Starting PropAI Backend...")
    try:
        init_db()
        print("✅ Database initialized")
    except Exception as e:
        print(f"⚠️ Database init warning: {e}")
    yield
    # Shutdown event
    print("🛑 Shutting down PropAI Backend...")


# Create FastAPI app
app = FastAPI(
    title="PropAI Backend",
    description="AI-Powered Real Estate Intelligence Platform for India",
    version="0.1.0",
    lifespan=lifespan,
)

# CORS middleware
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL, "http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api_router, prefix="/api", tags=["api"])


@app.get("/", tags=["root"])
async def root():
    """Root endpoint"""
    return {
        "message": "PropAI Backend - AI Real Estate Intelligence",
        "status": "ok",
        "docs": "/docs",
    }


@app.get("/health", tags=["health"])
async def health():
    """Health check endpoint"""
    return {"status": "healthy", "service": "propai-api"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host=os.getenv("API_HOST", "0.0.0.0"),
        port=int(os.getenv("API_PORT", 8000)),
        reload=os.getenv("ENVIRONMENT") == "development",
    )
