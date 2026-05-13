import requests
import pandas as pd
import os
from datetime import datetime, timedelta

def fetch_pmu_range(days_back=7):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.abspath(os.path.join(base_dir, '..', 'data', 'raw', 'races.csv'))
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    all_races = []
    headers = {'User-Agent': 'Mozilla/5.0'}

    # Loop through the last X days
    for i in range(days_back):
        date_to_fetch = (datetime.now() - timedelta(days=i)).strftime('%d%m%Y')
        url = f"https://offline.turfinfo.api.pmu.fr/rest/client/7/programme/{date_to_fetch}"
        
        print(f"📡 Fetching: {date_to_fetch}")
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                for reunion in data.get('programme', {}).get('reunions', []):
                    # Debugging information
                    print(f"DEBUG: Reunion keys: {reunion.keys()}")
                    print(f"DEBUG: Etablissement: {reunion.get('etablissement')}")
                    # Fixed mapping: Try 'nom' or 'etablissement'
                    venue = reunion.get('nom') or reunion.get('etablissement') or 'Unknown'
                    for race in reunion.get('courses', []):
                        all_races.append({
                            "race_id": f"PMU_{race.get('ordre')}_{reunion.get('numOfficiel')}_{date_to_fetch}",
                            "race_date": (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d'),
                            "venue": venue,
                            "track_condition": race.get('incident', 'Standard'), # PMU uses incidents for conditions
                            "prize_money": race.get('montantPrix', 0),
                            "loaded_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        })
        except Exception as e:
            print(f"❌ Error on {date_to_fetch}: {e}")

    df = pd.DataFrame(all_races)
    df.to_csv(output_path, index=False)
    print(f"✅ Backfill complete. {len(df)} total rows saved.")

if __name__ == "__main__":
    fetch_pmu_range(days_back=5) # Change this number to go further back