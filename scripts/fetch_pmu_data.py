import requests
import pandas as pd
import os
from datetime import datetime, timedelta

def fetch_all_pmu_fields(days_back=10):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.abspath(os.path.join(base_dir, '..', 'data', 'raw', 'races.csv'))
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    all_races = []
    headers = {'User-Agent': 'Mozilla/5.0'}

    for i in range(days_back):
        date_obj = datetime.now() - timedelta(days=i)
        date_str = date_obj.strftime('%d%m%Y')
        url = f"https://offline.turfinfo.api.pmu.fr/rest/client/7/programme/{date_str}"
        
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                for reunion in data.get('programme', {}).get('reunions', []):
                    # --- Nested Dictionary Extraction ---
                    hippo = reunion.get('hippodrome', {})
                    meteo = reunion.get('meteo', {})
                    pays = reunion.get('pays', {})
                    
                    # Reunion Level Metadata
                    venue = hippo.get('libelleLong') or hippo.get('libelleCourt') or 'Unknown'
                    weather = meteo.get('libelleMeteo') or 'Unknown'
                    country = pays.get('libelle') or 'Unknown'
                    num_reunion = reunion.get('numOfficiel')
                    nature = reunion.get('nature', 'Unknown')
                    
                    for race in reunion.get('courses', []):
                        # Course Level Metadata
                        all_races.append({
                            # IDs
                            "race_id": f"PMU_{date_str}_{num_reunion}_{race.get('ordre')}",
                            "race_date": date_obj.strftime('%Y-%m-%d'),
                            "num_reunion": num_reunion,
                            "race_number": race.get('ordre'),
                            
                            # Categorical Features
                            "venue": venue,
                            "country": country,
                            "weather": weather,
                            "reunion_nature": nature,
                            "discipline": race.get('discipline', 'Unknown'),
                            "specialty": race.get('specialite', 'Unknown'),
                            "condition_age": race.get('conditionAge', 'Unknown'),
                            "statut": race.get('statut', 'Unknown'),
                            
                            # Numerical Features
                            "prize_money": race.get('montantPrix', 0),
                            "runners_count": race.get('nombrePartants', 0),
                            "distance": race.get('distance', 0),
                            "distance_unit": race.get('distanceUnite', 'm'),
                            
                            # Flags
                            "is_quinte": 1 if race.get('cached') and 'QUINTE' in str(race).upper() else 0,

                            # Technical Metadata
                            "inserted_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        })
                print(f"✅ Ingested {date_str}")
        except Exception as e:
            print(f"❌ Error on {date_str}: {e}")

    df = pd.DataFrame(all_races)
    df.to_csv(output_path, index=False)
    print(f"🚀 Total Rows: {len(df)} | Columns: {len(df.columns)}")

if __name__ == "__main__":
    fetch_all_pmu_fields(10)