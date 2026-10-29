from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List, Optional
import os

from app.services.baseten_service import BasetenSpatialService

app = FastAPI(title="EcoSpatial AI", version="1.0.0")

class SpatialRequest(BaseModel):
    prompt: str
    coordinates: List[List[float]]

class RerouteRequest(BaseModel):
    origin: List[float]
    destination: List[float]
    flood_zone: Optional[List[List[float]]] = None

@app.get("/")
def root():
    return {
        "status": "EcoSpatial AI Backend Active",
        "models": ["SAM 3.1", "Muse Spark Open", "Muse Wonder"],
        "capabilities": ["Spatial Segmentation", "Flood Modeling", "Traffic Rerouting (Foleni)"]
    }

@app.post("/analyze-spatial")
def analyze_spatial(payload: SpatialRequest):
    try:
        return BasetenSpatialService.analyze_spatial_area(
            prompt=payload.prompt,
            coordinates=payload.coordinates
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/reroute-traffic")
def reroute_traffic(payload: RerouteRequest):
    try:
        return BasetenSpatialService.compute_traffic_reroute(
            origin=payload.origin,
            destination=payload.destination,
            flood_zone=payload.flood_zone
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if os.path.exists("app/static"):
    app.mount("/static", StaticFiles(directory="app/static"), name="static")
