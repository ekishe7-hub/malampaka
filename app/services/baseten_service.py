import requests
from app.config import settings

def analyze_risk_with_spark(image_b64: str, sam_data: dict):
    url = "https://model-xxxx.baseten.co/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {settings.BASETEN_KEY}",
        "Content-Type": "application/json"
    }
    prompt = f"Analyze spatial risk from segment data: {sam_data}. Provide risk_score (0-100) and 2 mitigation steps."
    payload = {
        "model": "meta-models/muse-spark-open-1026",
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_b64}"}}
                ]
            }
        ],
        "temperature": 0.2
    }
    try:
        res = requests.post(url, headers=headers, json=payload, timeout=15)
        return res.json()
    except Exception as e:
        return {
            "risk_score": 78,
            "level": "High Risk",
            "recommendations": ["Expand existing drainage culvert", "Establish green buffer zone"],
            "note": f"Fallback mode active: {str(e)}"
        }
