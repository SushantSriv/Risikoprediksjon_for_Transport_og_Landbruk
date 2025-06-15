import joblib
import pandas as pd
from datetime import datetime, timedelta

# Last modell, encoder og riktig feature-rekkefølge
model = joblib.load("random_forest_weather_model.pkl")
label_encoder = joblib.load("label_encoder.pkl")
feature_order = joblib.load("model_features_order.pkl")

kommune = "oslo"
kommune_encoded = label_encoder.transform([kommune])[0]

# Startverdier (f.eks. hentet fra observasjoner)
input_row = {
    "temp_lag_1": 12.3, "temp_lag_2": 13.0, "temp_lag_3": 12.8,
    "temp_lag_4": 11.7, "temp_lag_5": 13.4, "temp_lag_6": 12.9, "temp_lag_7": 13.1,
    "nedbor_lag_1": 1.0, "nedbor_lag_2": 2.2, "nedbor_lag_3": 0.8,
    "nedbor_lag_4": 3.0, "nedbor_lag_5": 0.0, "nedbor_lag_6": 4.1, "nedbor_lag_7": 2.3,
    "vind_lag_1": 3.2, "vind_lag_2": 3.5, "vind_lag_3": 3.3,
    "vind_lag_4": 3.0, "vind_lag_5": 2.9, "vind_lag_6": 3.7, "vind_lag_7": 3.4,
    "month": datetime.utcnow().month,
    "dayofyear": datetime.utcnow().timetuple().tm_yday,
    "latitude": 59.91,
    "longitude": 10.75,
    "kommune_encoded": kommune_encoded
}

input_df = pd.DataFrame([input_row])[feature_order]

predictions = []

for i in range(7):
    pred = model.predict(input_df)[0]
    predictions.append(pred)

    # Flytt lagene bakover
    for j in reversed(range(1, 7)):
        input_df.loc[0, f"temp_lag_{j+1}"] = input_df.loc[0, f"temp_lag_{j}"]
        input_df.loc[0, f"nedbor_lag_{j+1}"] = input_df.loc[0, f"nedbor_lag_{j}"]
        input_df.loc[0, f"vind_lag_{j+1}"] = input_df.loc[0, f"vind_lag_{j}"]

    # Sett dagens prediksjon som ny input for neste dag
    input_df.loc[0, "temp_lag_1"] = pred

# Skriv ut resultatene med datoer
today = datetime.utcnow().date()
print(f"📍 7-dagers temperaturprognose for {kommune.upper()}:")
for i, temp in enumerate(predictions):
    dato = today + timedelta(days=i + 1)
    print(f"  {dato.strftime('%A %d. %b')}: {round(temp, 2)} °C")
