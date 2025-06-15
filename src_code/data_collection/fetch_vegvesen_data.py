import requests
import os
import json

def fetch_nvdb_trafikkstasjoner():
    # ObjektTypeID for trafikkstasjon er 638
    url = "https://nvdbapiles-v3.atlas.vegvesen.no/vegobjekter/638"
    headers = {
        "Accept": "application/json"
    }

    response = requests.get(url, headers=headers, verify=False)  # SSL-verifisering er slått av

    if response.status_code == 200:
        # Definer lagringssti
        root_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        output_path = os.path.join(root_dir, "data", "raw", "vegvesen", "trafikkstasjoner.json")
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        # Lagre JSON-data
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(response.json(), f, indent=2)
        print(f"✅ Lagret trafikkstasjoner til: {output_path}")
    else:
        print(f"❌ Feil: {response.status_code} - {response.text}")

if __name__ == "__main__":
    fetch_nvdb_trafikkstasjoner()
