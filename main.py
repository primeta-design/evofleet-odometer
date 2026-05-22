import requests
import os
import json
from datetime import datetime
import time

EVO_API_KEY = os.getenv("EVO_API_KEY")
USDOT_NUMBER = os.getenv("USDOT_NUMBER")
PROVIDER_TOKEN = os.getenv("PROVIDER_TOKEN")

print("🚛 Test mode ishga tushdi...")
print(f"USDOT: {USDOT_NUMBER}")
print(f"API Key uzunligi: {len(EVO_API_KEY) if EVO_API_KEY else 0}")
print(f"Provider Token uzunligi: {len(PROVIDER_TOKEN) if PROVIDER_TOKEN else 0}")

if __name__ == "__main__":
    url = f"https://read.evoeld.com/api/v2/units-by-usdot/{USDOT_NUMBER}"
    
    headers = {
        "Content-Type": "application/json"
    }
    
    # 1-usul: x-api-key
    if EVO_API_KEY:
        headers["x-api-key"] = EVO_API_KEY
    
    # 2-usul: Provider Token (Bearer)
    if PROVIDER_TOKEN:
        headers["Authorization"] = f"Bearer {PROVIDER_TOKEN}"
        print("✅ Bearer token qo'shildi")
    
    print(f"URL: {url}")
    print(f"Headers: {list(headers.keys())}")
    
    try:
        r = requests.get(url, headers=headers, timeout=30)
        print(f"Status Code: {r.status_code}")
        print(f"Response: {r.text[:1000]}...")
    except Exception as e:
        print("Xato:", str(e))
    
    time.sleep(30)
