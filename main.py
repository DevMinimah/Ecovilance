import requests
import json

# ==========================================
# STEP 1: Fetch Environmental Data
# ==========================================
def fetch_air_quality_data(lat=6.5244, lon=3.3792):
    """Fetches real-time air quality data from Open-Meteo API."""
    url = f"https://air-quality-api.open-meteo.com/v1/air-quality?latitude={lat}&longitude={lon}&current=pm2_5,pm10,nitrogen_dioxide"
    response = requests.get(url, timeout=10)
    data = response.json()
    
    current = data['current']
    return {
        "timestamp": current['time'],
        "pm2_5": float(current['pm2_5']),
        "pm10": float(current['pm10']),
        "no2": float(current['nitrogen_dioxide'])
    }

if __name__ == "__main__":
    print("Testing API connection...")
    data = fetch_air_quality_data()
    print(json.dumps(data, indent=4))