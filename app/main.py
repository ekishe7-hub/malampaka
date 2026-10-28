from fastapi import FastAPI
from pydantic import BaseModel
from app.services.sam_service import run_sam_segmentation
from app.services.baseten_service import analyze_risk_with_spark

app = FastAPI(title="EcoSpatial AI Pipeline", version="1.0.0")

class AnalysisRequest(BaseModel):
    image_url: str
    image_b64: str
    feature_prompt: str = "drainage channel"

@app.get("/")
def read_root():
    return {"status": "EcoSpatial AI Backend Active", "models": ["SAM 3.1", "Muse Spark Open", "Muse Wonder"]}

@app.post("/api/v1/analyze-spatial")
async def analyze_spatial_endpoint(request: AnalysisRequest):
    sam_result = run_sam_segmentation(request.image_url, request.feature_prompt)
    risk_analysis = analyze_risk_with_spark(request.image_b64, sam_result)
    return {
        "success": True,
        "segmentation": sam_result,
        "risk_assessment": risk_analysis
    }
