# 📁 Fil: data_preprocessing/generate_stations_json.py
import pandas as pd
import json
import os 
# Les inn CSV-filen med stasjonsdata
root_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
csv_path= os.path.join(root_dir, "data", "processed", "all_frost_stations_with_kommune.csv")
df = pd.read_csv(csv_path)

# Filtrer ut rader med gyldige latitude og longitude
df_filtered = df.dropna(subset=["latitude", "longitude", "station_id", "kommune"])

# Behold kun nødvendige kolonner og konverter til ønsket format
stations = df_filtered[["kommune", "station_id", "latitude", "longitude"]].to_dict(orient="records")

# Lagre som JSON
json_path = "stations.json"
with open(json_path, "w", encoding="utf-8") as f:
    json.dump(stations, f, ensure_ascii=False, indent=2)

print(f"✅ Lagret {len(stations)} stasjoner til: {json_path}")
