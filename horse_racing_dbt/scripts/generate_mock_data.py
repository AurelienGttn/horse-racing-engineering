import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

def generate_horse_racing_data(days_back=10):
    # Ensure the raw data directory exists
    # Get the directory where the script is located
    base_dir = os.path.dirname(os.path.abspath(__file__))
    # Move up one level to the repo root, then into data/raw
    raw_data_path = os.path.join(base_dir, '..', 'data', 'raw')

    os.makedirs(raw_data_path, exist_ok=True)
    
    data = []
    # Generate data starting from 10 days ago up to today
    start_date = datetime.now() - timedelta(days=days_back)
    
    venues = ["Longchamp", "Chantilly", "Auteuil", "Vincennes", "Deauville"]
    conditions = ["Good", "Soft", "Heavy", "Dry"]
    
    for day in range(days_back + 1):
        current_date = start_date + timedelta(days=day)
        # Generate 5 races per day
        for race_num in range(1, 6):
            race_id = f"RACE_{current_date.strftime('%Y%m%d')}_{race_num}"
            data.append({
                "race_id": race_id,
                "race_date": current_date.strftime('%Y-%m-%d'),
                "venue": np.random.choice(venues),
                "track_condition": np.random.choice(conditions),
                "prize_money": np.random.randint(5000, 100000),
                "loaded_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })
    
    df = pd.DataFrame(data)
    output_file = os.path.join(raw_data_path, 'races.csv')
    df.to_csv(output_file, index=False)
    print(f"✅ Success! Created {len(df)} rows in {output_file}")

if __name__ == "__main__":
    generate_horse_racing_data()