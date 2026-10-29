from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.api.endpoints import router as api_router
import os

app = FastAPI(
    title="EcoSpatial AI API",
    description="Spatial Analysis and AI Segmentation API for Meta Hackathon",
    version="1.0.0"
)

app.include_router(api_router, prefix="/api/v1")

# Mount static frontend files
frontend_path = os.path.join(os.path.dirname(__file__), "..", "frontend")
if os.path.exists(frontend_path):
    app.mount("/static", StaticFiles(directory=frontend_path), name="static")

    @app.get("/")
    async def serve_frontend():
        return FileResponse(os.path.join(frontend_path, "index.html"))
