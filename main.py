import requests
import json
import hashlib
import csv
import time

def fetch_air_quality_data(lat=6.5244, lon=3.3792):
    url = f"https://air-quality-api.open-meteo.com/v1/air-quality?latitude={lat}&longitude={lon}&current=pm2_5,pm10,nitrogen_dioxide"
    response = requests.get(url)
    data = response.json()
    current = data['current']
    return {
        "timestamp": current['time'],
        "pm2_5": float(current['pm2_5']),
        "pm10": float(current['pm10']),
        "no2": float(current['nitrogen_dioxide'])
    }

# ==========================================
# STEP 2 & 3: Cryptographic Seal & Mini-Ledger
# ==========================================
def create_hash_chain(num_entries=3):
    ledger_file = "ecovilance_ledger.csv"
    previous_hash = "0" * 64 
    
    with open(ledger_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Timestamp", "PM2.5", "PM10", "NO2", "Data Hash", "Previous Hash", "Chain Hash"])
        
        print(f"🛡️ Starting Ecovilance. Logging {num_entries} data points...\n")
        
        for i in range(num_entries):
            env_data = fetch_air_quality_data()
            data_string = json.dumps(env_data, sort_keys=True)
            data_hash = hashlib.sha256(data_string.encode()).hexdigest()
            
            chain_input = data_hash + previous_hash
            chain_hash = hashlib.sha256(chain_input.encode()).hexdigest()
            
            with open(ledger_file, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([
                    env_data['timestamp'], env_data['pm2_5'], env_data['pm10'], env_data['no2'],
                    data_hash, previous_hash, chain_hash
                ])
            
            print(f"[{i+1}/{num_entries}] Logged data | Chain Hash: {chain_hash[:16]}...")
            previous_hash = chain_hash
            
            if i < num_entries - 1:
                time.sleep(2) 
                
    print(f"\n✅ Success! Ledger saved to '{ledger_file}'")
    return ledger_file

if __name__ == "__main__":
    ledger = create_hash_chain(num_entries=3)
