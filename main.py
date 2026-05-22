import requests
import os
import time

EVO_API_KEY = os.getenv("EVO_API_KEY")
USDOT_NUMBER = os.getenv("USDOT_NUMBER")
PROVIDER_TOKEN = os.getenv("PROVIDER_TOKEN")

print("🚛 Test mode v2 ishga tushdi...")
print(f"USDOT: {USDOT_NUMBER}")
print(f"API Key uzunligi: {len(EVO_API_KEY) if EVO_API_KEY else 0}")
print(f"Provider Token uzunligi: {len(PROVIDER_TOKEN) if PROVIDER_TOKEN else 0}")

if __name__ == "__main__":
    url = f"https://read.evoeld.com/api/v2/units-by-usdot/{USDOT_NUMBER}"
    
    headers = {
        "Content-Type": "application/json",
        "x-api-key": EVO_API_KEY,
        "provider-token": PROVIDER_TOKEN
    }
    
    print(f"URL: {url}")
    print("Headers qo'shildi: x-api-key + provider-token")
    
    try:
        r = requests.get(url, headers=headers, timeout=30)
        print(f"Status Code: {r.status_code}")
        
        if r.status_code == 200:
            data = r.json()
            units = data.get("units", [])
            print(f"✅ Muvaffaqiyat! {len(units)} ta truck topildi")
            if units:
                print("Birinchi truck:", units[0])
        else:
            print(f"Response: {r.text}")
            print("\n💡 Maslahat: USDOT yoki tokenlarni qayta tekshiring")
    except Exception as e:
        print("Xato:", str(e))
    
    time.sleep(30)
