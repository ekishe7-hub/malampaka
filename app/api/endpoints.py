from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from app.services.baseten_service import BasetenSpatialService

router = APIRouter()

class SpatialRequest(BaseModel):
    prompt: str
    coordinates: List[List[float]]

class RerouteRequest(BaseModel):
    origin: List[float]
    destination: List[float]
    flood_zone: Optional[List[List[float]]] = None

@router.get("/")
def root():
    return {
        "status": "EcoSpatial AI Backend Active",
        "models": ["SAM 3.1", "Muse Spark Open", "Muse Wonder"],
        "capabilities": ["Spatial Segmentation", "Flood Modeling", "Traffic Rerouting (Foleni)"]
    }

@router.post("/analyze-spatial")
def analyze_spatial(payload: SpatialRequest):
    try:
        result = BasetenSpatialService.analyze_spatial_area(
            prompt=payload.prompt,
            coordinates=payload.coordinates
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/reroute-traffic")
def reroute_traffic(payload: RerouteRequest):
    try:
        result = BasetenSpatialService.compute_traffic_reroute(
            origin=payload.origin,
            destination=payload.destination,
            flood_zone=payload.flood_zone
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
