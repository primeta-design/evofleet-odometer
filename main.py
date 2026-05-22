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
        return creds
    except Exception as e:
        print("❌ Creds xatosi:", e)
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
        sheet = client.open_by_key(SPREADSHEET_ID).worksheet(SHEET_NAME)
        
        data = sheet.get_all_values()
        print(f"📋 Sheet'da {len(data)} ta qator topildi")
        
        if len(data) <= 1:
            print("⚠️ Sheet bo'sh yoki faqat header bor. Ma'lumot qo'shing!")
        
        updated = 0
        for unit in units:
            truck_no = str(unit.get("truck_number", "")).strip()
            odometer = unit.get("odometer") or unit.get("mileage") or unit.get("current_mileage")
            
            if not truck_no or odometer is None:
                continue
            
            print(f"🔍 Qidirilmoqda: '{truck_no}' → {odometer} miles")
            
            found = False
            for i, row in enumerate(data):
                if len(row) > 1:
                    sheet_truck = str(row[1]).strip()  # B ustuni (Truck Number)
                    if sheet_truck == truck_no:
                        try:
                            sheet.update_cell(i+1, 7, int(odometer))  # G ustuni
                            updated += 1
                            print(f"✅ Updated: {truck_no} → {odometer}")
                            found = True
                            break
                        except Exception as e:
                            print(f"❌ Update xatosi: {e}")
            if not found:
                print(f"⚠️ Truck topilmadi: {truck_no}")
                    
        print(f"📊 Jami {updated} ta truck yangilandi | {datetime.now().strftime('%H:%M:%S')}\n")
        
    except Exception as e:
        print("❌ Sheet xato:", type(e).__name__, str(e))

# ===================== MAIN =====================
if __name__ == "__main__":
    while True:
        units = get_eld_data()
        if units:
            update_odometer(units)
        time.sleep(60)
