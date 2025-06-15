import requests
import json
import os

class UnsafeForecast:
    def __init__(self, lat, lon, alt, user_agent):
        self.lat = lat
        self.lon = lon
        self.alt = alt
        self.url = (
            f"https://api.met.no/weatherapi/locationforecast/2.0/compact"
            f"?lat={self.lat}&lon={self.lon}&altitude={self.alt}"
        )
        self.headers = {"User-Agent": user_agent}
        self.data = None

    def update(self):
        response = requests.get(self.url, headers=self.headers, verify=False)
        if response.status_code == 200:
            self.data = response.json()
        else:
            raise Exception(f"Feil {response.status_code}: {response.text}")

def fetch_met_data(city_name, lat, lon, alt):
    forecast = UnsafeForecast(lat, lon, alt, "weather_risk_prediction/1.0 sushant.nmbu@gmail.com")
    forecast.update()

    root_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    output_path = os.path.join(root_dir, "data", "raw", "met", f"{city_name.lower()}_forecast.json")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "w") as f:
        json.dump(forecast.data, f, indent=2)

if __name__ == "__main__":
    # Hent for flere steder:
    locations = {
    "Oslo": (59.91, 10.75, 23),
    "Bergen": (60.39, 5.32, 12),
    "Trondheim": (63.43, 10.39, 30),
    "Tromsø": (69.65, 18.96, 15),
    "Stavanger": (58.97, 5.73, 14),
    "Kristiansand": (58.15, 8.00, 15),
    "Ålesund": (62.47, 6.15, 5),
    "Bodø": (67.28, 14.41, 13),
    "Alta": (69.97, 23.27, 60),
    "Hamar": (60.79, 11.07, 127),
    "Gjøvik": (60.80, 10.69, 130),
    "Lillehammer": (61.11, 10.46, 180),
    "Drammen": (59.74, 10.21, 5),
    "Fredrikstad": (59.21, 10.95, 6)
}


    for city, (lat, lon, alt) in locations.items():
        print(f"Henter data for {city}...")
        fetch_met_data(city, lat, lon, alt)
        print(f"{city} fullført ✅")
