"""
Test script for body analysis endpoint
"""
import base64
import requests
import json

# Read test image
image_path = r"c:\Users\jayde\Documents\Ayurveda\WhatsApp Image 2026-04-27 at 13.15.57.jpeg"

with open(image_path, 'rb') as f:
    image_data = base64.b64encode(f.read()).decode('utf-8')

# Prepare request
url = "http://127.0.0.1:5000/analyze-face-body-fusion"
payload = {
    "image": f"data:image/jpeg;base64,{image_data}",
    "face_scores": {
        "vata": 35.0,
        "pitta": 40.0,
        "kapha": 25.0
    }
}

print("Sending request to body analysis endpoint...")
print(f"Image size: {len(image_data)} bytes")

try:
    response = requests.post(url, json=payload, timeout=30)
    print(f"\nStatus Code: {response.status_code}")
    print(f"\nResponse:")
    print(json.dumps(response.json(), indent=2))
except Exception as e:
    print(f"Error: {e}")
