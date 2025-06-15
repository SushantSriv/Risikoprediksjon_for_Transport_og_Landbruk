import requests
import pandas as pd
import os
from datetime import datetime, timedelta

CLIENT_ID = "a4bea9fb-7df2-4981-a69b-cc32124ae295"
CLIENT_SECRET = "b4d5c59a-8489-410e-a62f-59257d8f63a6"

elements = [
    "mean(air_temperature P1D)",
    "sum(precipitation_amount P1D)",
    "mean(wind_speed P1D)"
]
start_date = "1980-01-01"
end_date = "2024-05-31"

url = "https://frost.met.no/observations/v0.jsonld"

# Dynamisk path-oppsett
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
stations_path = os.path.join(project_root, "data", "processed", "all_frost_stations_with_kommune.csv")
output_path = os.path.join(project_root, "data", "processed", "historisk_vaer_alle_kommuner.csv")
os.makedirs(os.path.dirname(output_path), exist_ok=True)

# 📥 Les CSV og filtrer ut gyldige (ikke-null) rader
stations_df = pd.read_csv(stations_path)
stations_df = stations_df.dropna(subset=["kommune", "station_id"]).drop_duplicates(subset=["kommune"])

def fetch_period(station_id, start, end):
    params = {
        "sources": station_id,
        "elements": ",".join(elements),
        "referencetime": f"{start}/{end}"
    }
    r = requests.get(url, params=params, auth=(CLIENT_ID, CLIENT_SECRET))
    if r.status_code != 200:
        print(f"⚠️ {station_id} – feil {r.status_code}: {r.text}")
        return []
    return r.json().get("data", [])

def fetch_all_for_station(station_id):
    all_data = []
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    step = timedelta(days=365)

    while start < end:
        period_end = min(start + step, end)
        print(f"   ↪️  {start.date()} → {period_end.date()}")
        data = fetch_period(station_id, start.date(), period_end.date())
        all_data.extend(data)
        start = period_end + timedelta(days=1)

    rows = []
    for entry in all_data:
        base = {
            "time": entry["referenceTime"],
            "station": entry["sourceId"]
        }
        for obs in entry.get("observations", []):
            base[obs["elementId"]] = obs["value"]
        rows.append(base)

    return pd.DataFrame(rows)

# 🔁 Hent data for hver kommune
all_frames = []
for i, row in stations_df.iterrows():
    kommune = row["kommune"]
    station_id = row["station_id"]
    print(f"[{i+1}/{len(stations_df)}] Henter data for {kommune} ({station_id})")
    df = fetch_all_for_station(station_id)
    df["kommune"] = kommune
    all_frames.append(df)

# 📝 Lagre samlet CSV
df_all = pd.concat(all_frames, ignore_index=True)
df_all.to_csv(output_path, index=False)
print(f"\n✅ Lagret {len(df_all)} rader til: {output_path}")
