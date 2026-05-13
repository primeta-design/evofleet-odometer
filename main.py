import requests
import os
import time

EVO_API_KEY = os.getenv("EVO_API_KEY")
PROVIDER_TOKEN = os.getenv("PROVIDER_TOKEN")
USDOT_NUMBER = os.getenv("USDOT_NUMBER")

print("🚛 Test boshlandi...")
print(f"USDOT: {USDOT_NUMBER}")
print(f"API Key uzunligi: {len(EVO_API_KEY) if EVO_API_KEY else 0}")
print(f"Provider Token uzunligi: {len(PROVIDER_TOKEN) if PROVIDER_TOKEN else 0}")

url = f"https://read.evoeld.com/api/v2/units-by-usdot/{USDOT_NUMBER}"

headers = {
    "x-api-key": EVO_API_KEY,
    "provider-token": PROVIDER_TOKEN,
    "Content-Type": "application/json"
}

try:
    r = requests.get(url, headers=headers, timeout=30)
    print(f"Status Code: {r.status_code}")
    print(f"Response: {r.text[:800]}...")
    
    if r.status_code == 200:
        data = r.json()
        print(f"✅ Muvaffaqiyatli! {len(data.get('units', []))} ta unit topildi.")
except Exception as e:
    print("Xato:", e)

time.sleep(30)