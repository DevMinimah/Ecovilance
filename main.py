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
    return {"timestamp": current['time'], "pm2_5": float(current['pm2_5']), "pm10": float(current['pm10']), "no2": float(current['nitrogen_dioxide'])}

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
                writer.writerow([env_data['timestamp'], env_data['pm2_5'], env_data['pm10'], env_data['no2'], data_hash, previous_hash, chain_hash])
            print(f"[{i+1}/{num_entries}] Logged data | Chain Hash: {chain_hash[:16]}...")
            previous_hash = chain_hash
            if i < num_entries - 1: time.sleep(2) 
    print(f"\n✅ Success! Ledger saved to '{ledger_file}'")
    return ledger_file

def audit_ledger(ledger_file):
    print("\n--- 🕵️ INITIATING ECOVILANCE SECURITY AUDIT ---")
    previous_hash = "0" * 64
    with open(ledger_file, mode='r') as file:
        reader = csv.DictReader(file)
        for row_num, row in enumerate(reader, start=1):
            env_data = {"timestamp": row['Timestamp'], "pm2_5": float(row['PM2.5']), "pm10": float(row['PM10']), "no2": float(row['NO2'])}
            data_string = json.dumps(env_data, sort_keys=True)
            calculated_data_hash = hashlib.sha256(data_string.encode()).hexdigest()
            chain_input = calculated_data_hash + previous_hash
            calculated_chain_hash = hashlib.sha256(chain_input.encode()).hexdigest()
            if calculated_chain_hash != row['Chain Hash']:
                print(f"🚨 ALERT: TAMPER DETECTED AT ROW {row_num}! Environmental data has been maliciously modified.")
                return False
            previous_hash = row['Chain Hash']
    print("✅ AUDIT PASSED: All Ecovilance data integrity seals are intact.")
    return True

if __name__ == "__main__":
    ledger = create_hash_chain(num_entries=3)
    audit_ledger(ledger)
    
    # ==========================================
    # TEST TAMPER PROOF: Simulate a hack!
    # ==========================================
    print("\n--- ⚠️ SIMULATING A MALICIOUS ATTACK ---")
    with open(ledger, mode='r') as f:
        lines = f.readlines()
    
    parts = lines[1].split(',')
    parts[1] = "0.0" 
    lines[1] = ','.join(parts)
    
    with open(ledger, mode='w') as f:
        f.writelines(lines)
    print("Attacker changed PM2.5 reading to 0.0 to hide pollution.")
    
    audit_ledger(ledger)