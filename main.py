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
SPREADSHEET_NAME = os.getenv("SPREADSHEET_NAME", "COMPANIES OIL CHANGE")
SHEET_NAME = "B1-TRACKING"

print("🚛 EVO ELD Odometer Updater ishga tushdi...")

# Google Credentials ni Environment dan olish
def get_google_creds():
    creds_json = os.getenv("GOOGLE_CREDENTIALS")
    if not creds_json:
        print("❌ GOOGLE_CREDENTIALS topilmadi!")
        return None
    try:
        creds_dict = json.loads(creds_json)
        return Credentials.from_service_account_info(creds_dict)
    except Exception as e:
        print("❌ JSON parse xatosi:", e)
        return None

def get_eld_data():
    if not EVO_API_KEY or not USDOT_NUMBER:
        print("❌ EVO_API_KEY yoki USDOT_NUMBER sozlanmagan!")
        return []
    
    url = f"https://read.evoeld.com/api/v2/units-by-usdot/{USDOT_NUMBER}"
    headers = {
        "x-api-key": EVO_API_KEY,
        "Content-Type": "application/json"
    }
    try:
        r = requests.get(url, headers=headers, timeout=20)
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
        sheet = client.open(SPREADSHEET_NAME).worksheet(SHEET_NAME)
        
        data = sheet.get_all_values()
        updated = 0
        
        for unit in units:
            truck_no = str(unit.get("truck_number", "")).strip()
            odometer = unit.get("odometer") or unit.get("mileage") or unit.get("current_mileage")
            
            if not truck_no or not odometer:
                continue
                
            for i, row in enumerate(data):
                if len(row) > 1 and str(row[1]).strip() == truck_no:
                    try:
                        sheet.update_cell(i+1, 7, int(odometer))  # G ustun
                        updated += 1
                        print(f"✅ Updated: {truck_no} → {odometer}")
                    except:
                        pass
                    break
                    
        print(f"📊 Jami {updated} ta truck yangilandi | {datetime.now().strftime('%H:%M:%S')}")
        
    except Exception as e:
        print("❌ Sheet yangilashda xato:", e)

# ===================== MAIN =====================
if __name__ == "__main__":
    while True:
        units = get_eld_data()
        if units:
            update_odometer(units)
        time.sleep(60)