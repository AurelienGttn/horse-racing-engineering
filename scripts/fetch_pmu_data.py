import requests
import pandas as pd
import os
from datetime import datetime
from datetime import date
from dateutil.relativedelta import relativedelta

def fetch_today_pmu_races():
    # 1. Setup paths
    base_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.abspath(os.path.join(base_dir, '..', 'data', 'raw', 'races.csv'))
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # 2. Define API endpoint (Today's date)
    today_str = datetime.now().strftime('%d%m%Y')
    first_date = datetime.now() - relativedelta(days=1)  # Fetch yesterday's data to ensure it's available
    first_date_str = first_date.strftime('%d%m%Y')
    url = f"https://offline.turfinfo.api.pmu.fr/rest/client/7/programme/{first_date_str}"
    
    # 💡 ADD THESE HEADERS TO BYPASS 403
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'application/json',
        'Referer': 'https://www.pmu.fr/'
    }

    print(f"📡 Fetching data from PMU for {first_date_str}...")
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        race_list = []
        
        # 3. Parse the nested JSON
        # PMU structure: programme -> reunions -> courses
        for reunion in data.get('programme', {}).get('reunions', []):
            venue = reunion.get('etablissement', 'Unknown')
            for race in reunion.get('courses', []):
                race_list.append({
                    "race_id": f"PMU_{race.get('ordre')}_{reunion.get('numOfficiel')}_{first_date_str}",
                    "race_date": datetime.now().strftime('%Y-%m-%d'),
                    "venue": venue,
                    "track_condition": race.get('incident', 'Standard'), # PMU uses incidents for conditions
                    "prize_money": race.get('montantPrix', 0),
                    "loaded_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                })
        
        # 4. Save to CSV
        df = pd.DataFrame(race_list)
        if not df.empty:
            df.to_csv(output_path, index=False)
            print(f"✅ Successfully saved {len(df)} real races to {output_path}")
        else:
            print("⚠️ No races found in the API response.")

    except Exception as e:
        print(f"❌ Error fetching PMU data: {e}")

if __name__ == "__main__":
    fetch_today_pmu_races()