"""
SlideGuroo Backend - AI-Powered Learning Assistant
Main FastAPI application
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv
import logging

from routers import slides, topics, chat, diagrams, auth
from database import engine, Base

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan events for startup and shutdown"""
    # Startup: Create database tables
    logger.info("Creating database tables...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Database tables created successfully")

    yield

    # Shutdown: Close database connections
    logger.info("Closing database connections...")
    await engine.dispose()


# Create FastAPI app
app = FastAPI(
    title="SlideGuroo API",
    description="AI-Powered Student Learning Assistant with Authentication",
    version="2.0.0",
    lifespan=lifespan
)

# Configure CORS
cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://localhost:5173").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create upload directory if it doesn't exist
upload_dir = os.getenv("UPLOAD_DIR", "./uploads")
os.makedirs(upload_dir, exist_ok=True)

# Mount static files for uploads
if os.path.exists(upload_dir):
    app.mount("/uploads", StaticFiles(directory=upload_dir), name="uploads")

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(slides.router, prefix="/api/slides", tags=["Slides"])
app.include_router(topics.router, prefix="/api/topics", tags=["Topics"])
app.include_router(chat.router, prefix="/api/chat", tags=["Chat"])
app.include_router(diagrams.router, prefix="/api/diagrams", tags=["Diagrams"])

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to SlideGuroo API",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "SlideGuroo API"
    }

if __name__ == "__main__":
    import uvicorn
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))

    logger.info(f"Starting SlideGuroo API on {host}:{port}")
    uvicorn.run("main:app", host=host, port=port, reload=True)
