import requests
import base64
from fastapi import HTTPException

def remove_bg_replicate(image_bytes: bytes, replicate_api_key: str) -> bytes:
    url = "https://api.replicate.com/v1/models/armanrod/anybg-removal/versions/a47af983e8f699d76b99ecdc02a5f5a1b0fb98196be947d048fae26c1c45bd85"

    headers = {
        "Authorization": f"Bearer {replicate_api_key}",
        "Content-Type": "application/json"
    }

    data = {
        "input": {
            "image": f"data:image/png;base64,{base64.b64encode(image_bytes).decode()}"
        }
    }

    response = requests.post(url, json=data, headers=headers)

    if response.status_code != 200:
        raise HTTPException(status_code=500, detail=f"Replicate API error: {response.text}")

    output = response.json().get("output")

    if not output:
        raise HTTPException(status_code=500, detail="No output from background removal API")

    # Возвращаем URL готового изображения
    result_url = output
    img_data = requests.get(result_url).content

    return img_data
