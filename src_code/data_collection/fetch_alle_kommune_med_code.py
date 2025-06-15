import requests
import pandas as pd

CLIENT_ID = "a4bea9fb-7df2-4981-a69b-cc32124ae295"
CLIENT_SECRET = "b4d5c59a-8489-410e-a62f-59257d8f63a6"

stations_url = "https://frost.met.no/sources/v0.jsonld"
params = {
    "types": "SensorSystem",
    "fields": "id,name,geometry,validFrom,validTo,municipality",
    "geometry": "POLYGON((4 58, 31 58, 31 72, 4 72, 4 58))",  # Omtrentlig boks rundt Norge
    "country": "NO"
}

response = requests.get(stations_url, params=params, auth=(CLIENT_ID, CLIENT_SECRET))

if response.status_code == 200:
    data = response.json().get("data", [])
    records = []
    for s in data:
        records.append({
            "station_id": s.get("id"),
            "station_name": s.get("name"),
            "kommune": s.get("municipality"),
            "latitude": s.get("geometry", {}).get("coordinates", [None, None])[1],
            "longitude": s.get("geometry", {}).get("coordinates", [None, None])[0],
        })
    df = pd.DataFrame(records)
    df = df.dropna(subset=["kommune"])
    df.to_csv("all_frost_stations_with_kommune.csv", index=False)
    print("✅ Lagret til all_frost_stations_with_kommune.csv")
else:
    print(f"❌ Feil: {response.status_code} - {response.text}")
