import requests
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import time
import os
import json

# ================== SOZLAMALAR ==================
EVO_API_KEY = os.getenv("EVO_API_KEY")
USDOT_NUMBER = os.getenv("USDOT_NUMBER")
PROVIDER_TOKEN = os.getenv("PROVIDER_TOKEN")

SPREADSHEET_ID = "1EszHInPi3_8hKIU32EpyxdIdfaKNa90ZZlMuf0xtiH8"
SHEET_NAME = "Dock 2 Dock"

print("🚛 EVO ELD Odometer Updater ishga tushdi...")

def get_google_creds():
    creds_json = os.getenv("GOOGLE_CREDENTIALS")
    if not creds_json:
        print("❌ GOOGLE_CREDENTIALS topilmadi!")
        return None
    try:
        creds_dict = json.loads(creds_json)
        SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
        creds = Credentials.from_service_account_info(creds_dict, scopes=SCOPES)
        print("✅ Service Account credentials yaratildi")
        return creds
    except Exception as e:
        print("❌ Creds yaratish xatosi:", e)
        return None

def get_eld_data():
    url = f"https://read.evoeld.com/api/v2/units-by-usdot/{USDOT_NUMBER}"
    headers = {
        "Content-Type": "application/json",
        "x-api-key": EVO_API_KEY,
        "provider-token": PROVIDER_TOKEN
    }
    try:
        r = requests.get(url, headers=headers, timeout=30)
        if r.status_code == 200:
            units = r.json().get("units", [])
            print(f"✅ {len(units)} ta truck ma'lumoti olindi")
            return units
        else:
            print(f"❌ API Error: {r.status_code}")
            return []
    except Exception as e:
        print("❌ Request xatosi:", e)
        return []

def update_odometer(units):
    creds = get_google_creds()
    if not creds:
        return
    
    try:
        client = gspread.authorize(creds)
        print("✅ gspread muvaffaqiyatli authorize qilindi")
        
        sheet = client.open_by_key(SPREADSHEET_ID).worksheet(SHEET_NAME)
        print(f"✅ Sheet ochildi: {SPREADSHEET_ID} | {SHEET_NAME}")
        
        data = sheet.get_all_values()
        print(f"📋 Sheet'da {len(data)} ta qator topildi")
        
        # ... (qolgan kod keyinroq qo'shiladi)
        
    except Exception as e:
        print("❌ Sheet xato turi:", type(e).__name__)
        print("❌ To'liq xato:", str(e))
        if hasattr(e, 'args'):
            print("❌ Xato argumentlari:", e.args)

# ===================== MAIN =====================
if __name__ == "__main__":
    while True:
        units = get_eld_data()
        if units:
            update_odometer(units)
        time.sleep(60)
