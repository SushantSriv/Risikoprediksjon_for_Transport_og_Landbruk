import geopandas as gpd
import os

def validate_kartverket_geojson():
    root_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    geojson_path = os.path.join(root_dir, "data", "raw", "kartverket", "kommuner.geojson")

    if not os.path.exists(geojson_path):
        print(f"❌ Fil ikke funnet: {geojson_path}")
        return

    # Les kommune-laget eksplisitt
    gdf = gpd.read_file(geojson_path, layer="Kommune")
    print(f"✅ Antall kommuner (polygoner): {len(gdf)}")
    print(gdf[["kommunenavn", "kommunenummer", "geometry"]].head())

if __name__ == "__main__":
    validate_kartverket_geojson()
