import pandas as pd
import geopandas as gpd
from shapely.wkt import loads as wkt_loads
import os

def convert_csv_to_geodata():
    root_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    input_csv = os.path.join(root_dir, "data", "processed", "trafikkstasjoner_parset.csv")
    output_geojson = os.path.join(root_dir, "data", "processed", "trafikkstasjoner_matched.geojson")

    # Last inn CSV
    df = pd.read_csv(input_csv)

    # Konverter wkt -> Point (hopp over rader med tom geometri)
    df = df[df["wkt"].notnull()]
    df["geometry"] = df["wkt"].apply(wkt_loads)

    # Lag GeoDataFrame
    gdf = gpd.GeoDataFrame(df, geometry="geometry", crs="EPSG:5973")  # SRID fra XML: 5973 = ETRS89 UTM sone 33

    # Valgfritt: transformer til WGS84 (lat/lon) for visning eller kart
    gdf = gdf.to_crs("EPSG:4326")

    # Lagre til GeoJSON
    gdf.to_file(output_geojson, driver="GeoJSON")
    print(f"✅ Lagret {len(gdf)} trafikkstasjoner til: {output_geojson}")

if __name__ == "__main__":
    convert_csv_to_geodata()
