import requests
import os
import json
from datetime import datetime
import time

EVO_API_KEY = os.getenv("EVO_API_KEY")
USDOT_NUMBER = os.getenv("USDOT_NUMBER")

print("🚛 Test mode ishga tushdi...")
print(f"USDOT: {USDOT_NUMBER}")
print(f"API Key uzunligi: {len(EVO_API_KEY) if EVO_API_KEY else 0}")

if __name__ == "__main__":
    url = f"https://read.evoeld.com/api/v2/units-by-usdot/{USDOT_NUMBER}"
    headers = {
        "x-api-key": EVO_API_KEY,
        "Content-Type": "application/json"
    }
    
    print(f"URL: {url}")
    
    try:
        r = requests.get(url, headers=headers, timeout=20)
        print(f"Status Code: {r.status_code}")
        print(f"Response: {r.text[:500]}...")   # birinchi 500 belgi
    except Exception as e:
        print("Xato:", e)
    
    time.sleep(30)