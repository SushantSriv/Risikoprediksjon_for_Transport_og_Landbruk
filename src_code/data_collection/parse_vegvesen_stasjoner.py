import requests
import json
import pandas as pd
from tqdm import tqdm
import os

# -- Paths --
root_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
input_path = os.path.join(root_dir, "data", "raw", "vegvesen", "trafikkstasjoner.json")
output_path = os.path.join(root_dir, "data", "processed", "trafikkstasjoner_parset.csv")

def extract_station_data(json_obj):
    station_id = json_obj.get("id")
    navn = ""
    wkt = ""
    kommune = ""
    fylke = ""

    # Egenskaper: navn og punkt
    for e in json_obj.get("egenskaper", []):
        if isinstance(e, dict):
            if e.get("navn") == "Navn":
                navn = e.get("verdi", "")
            elif e.get("navn") == "Geometri, punkt":
                wkt = e.get("verdi", "")

    # Kommune
    kommuner = json_obj.get("lokasjon", {}).get("kommuner", [])
    if isinstance(kommuner, list) and len(kommuner) > 0 and isinstance(kommuner[0], dict):
        kommune = kommuner[0].get("kommune", "")
    elif isinstance(kommuner, int):  # fallback
        kommune = str(kommuner)

    # Fylke
    fylker = json_obj.get("lokasjon", {}).get("fylker", [])
    if isinstance(fylker, list) and len(fylker) > 0 and isinstance(fylker[0], dict):
        fylke = fylker[0].get("fylke", "")
    elif isinstance(fylker, int):
        fylke = str(fylker)

    return {
        "id": station_id,
        "navn": navn,
        "kommune": kommune,
        "fylke": fylke,
        "wkt": wkt
    }

def parse_all():
    with open(input_path, encoding="utf-8") as f:
        json_data = json.load(f)

    rows = []
    for obj in tqdm(json_data["objekter"], desc="🔄 Henter og parser trafikkstasjoner"):
        href = obj["href"]
        try:
            r = requests.get(href, headers={"Accept": "application/json"}, verify=False)
            r.raise_for_status()
            parsed = extract_station_data(r.json())
            parsed["href"] = href
            rows.append(parsed)
        except Exception as e:
            print(f"⚠️ Feil ved {href}: {e}")

    df = pd.DataFrame(rows)
    df.to_csv(output_path, index=False, encoding="utf-8")
    print(f"✅ Lagret {len(df)} stasjoner til: {output_path}")

if __name__ == "__main__":
    parse_all()
