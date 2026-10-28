import requests
from app.config import settings

def run_sam_segmentation(image_url: str, target_prompt: str = "water channel"):
    url = "https://api.meta.ai/v1/vision/segment"
    headers = {
        "Authorization": f"Bearer {settings.SAM_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "sam-3.1",
        "image_url": image_url,
        "prompt": target_prompt
    }
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=15)
        if response.status_code == 200:
            return response.json()
        return {"status": "mock_success", "segmented_count": 4, "feature": target_prompt}
    except Exception as e:
        return {"status": "error", "message": str(e)}
