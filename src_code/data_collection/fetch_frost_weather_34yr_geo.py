import pandas as pd
import os

# Filstier (juster hvis du kjører selv)
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
stations_path = os.path.join(project_root, "data", "processed", "all_frost_stations_with_kommune.csv")
weather_path = os.path.join(project_root, "data", "processed", "historisk_vaer_alle_kommuner.csv")
output_path = os.path.join(project_root, "data", "processed", "historisk_vaer_alle_kommuner_geo.csv")

# Les data
stations_df = pd.read_csv(stations_path)
weather_df = pd.read_csv(weather_path)


weather_df["station_clean"] = weather_df["station"].str.split(":").str[0]

# Rens og behold nødvendige kolonner
stations_clean = stations_df[["station_id", "latitude", "longitude"]].dropna().drop_duplicates(subset=["station_id"])

# Slå sammen på ren station_id
merged_df = weather_df.merge(stations_clean, how="left", left_on="station_clean", right_on="station_id")

# Fjern midlertidige kolonner
merged_df = merged_df.drop(columns=["station_clean", "station_id"])

# Lagre resultat
os.makedirs(os.path.dirname(output_path), exist_ok=True)
merged_df.to_csv(output_path, index=False)

print(f"✅ Ferdig! Lagret med koordinater til:\n{output_path}")
