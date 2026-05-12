import requests
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import time
import os

# ================== SOZLAMALAR ==================
EVO_API_KEY = os.getenv("EVO_API_KEY")
USDOT_NUMBER = os.getenv("USDOT_NUMBER")

SPREADSHEET_NAME = "COMPANIES OIL CHANGE"   # Google Sheet nomi
SHEET_NAME = "B1-TRACKING"                  # Varaq nomi

print("🚛 EVO ELD Odometer Updater ishga tushdi...")

def get_eld_data():
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
    try:
        creds = Credentials.from_service_account_file("service_account.json")
        client = gspread.authorize(creds)
        sheet = client.open(SPREADSHEET_NAME).worksheet(SHEET_NAME)
        
        data = sheet.get_all_values()
        updated = 0
        
        for unit in units:
            truck_no = str(unit.get("truck_number", "")).strip()
            odometer = unit.get("odometer") or unit.get("mileage") or unit.get("current_mileage")
            
            if not truck_no or not odometer:
                continue
                
            # B ustunda (Unit raqami) qidirish
            for i, row in enumerate(data):
                if len(row) > 1 and str(row[1]).strip() == truck_no:
                    try:
                        sheet.update_cell(i+1, 7, int(odometer))  # G ustun = Current Mileage
                        updated += 1
                        print(f"✅ Updated: {truck_no} → {odometer}")
                    except:
                        pass
                    break
                    
        print(f"📊 Jami {updated} ta truck yangilandi | {datetime.now().strftime('%H:%M:%S')}")
        
    except Exception as e:
        print("❌ Sheet yangilashda xato:", e)

# ===================== MAIN LOOP =====================
if __name__ == "__main__":
    while True:
        units = get_eld_data()
        if units:
            update_odometer(units)
        time.sleep(60)   # Har 1 daqiqada
