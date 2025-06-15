
# 🌦️ Værbasert Risikoprediksjon

Et ende‑til‑ende‑prosjekt som kombinerer historiske ulykkesdata og sanntidsvær fra MET Norway for å forutsi trafikkulykker på kommunenivå i Norge.  
Prosjektet består av tre hoveddeler:

1. **Datainnsamling & forbehandling** – Python‑skript som henter og prosesserer 34 år med vær‑ og ulykkesdata.
2. **Maskinlæring** – Tre modeller (tidspunkt, temperatur, værforhold) trent på de prosesserte datasettene.
3. **API & Frontend** – FastAPI‑server som kombinerer modellene og et React‑dashbord som visualiserer risikoen i sanntid.

📦 Modellene er også publisert på Hugging Face:  
👉 https://huggingface.co/sushant

---

## 📁 Prosjektstruktur

```
Værbasert RisikoPrediksjon
├── backend/
│   ├── main.py
│   ├── requirements.txt
│   ├── modell_temp_pipeline.pkl
│   ├── modell_tid_pipeline.pkl
│   ├── modell_vaer_pipeline.pkl
│   ├── random_forest_weather_model.pkl
│   ├── label_encoder.pkl
│   └── fetch_frost_weather_34yr.py
├── frontend_vite/
│   ├── index.html
│   ├── vite.config.js
│   └── src/components/MapView.jsx
│   └── public/data/stations.json
└── README.md
```
## 📂 Mappestruktur

```
Værbasert Risikoprediksjon/
├── data/
│   └── processed/
│       ├── all_frost_stations_with_kommune.csv   # stasjon-/kommune-mapping
│       └── historisk_vaer_alle_kommuner.csv      # 34 års historikk
│
├── models/
│   ├── modell_tidspunkt_pipeline.pkl             # risiko: tidspunkt-kategori
│   ├── modell_temp_pipeline.pkl                  # risiko: temperatur-kategori
│   ├── modell_vaerforhold_pipeline.pkl           # risiko: værtype
│   ├── random_forest_weather_model.pkl           # 7-dagers temperaturmodell
│   └── label_encoder.pkl                         # encoder for kommunenavn
│
├── src/
│   ├── data_processing/
│   │   └── fetch_frost_weather_34yr.py           # henter historikk fra Frost
│   └── main.py                                   # FastAPI-server
│
├── notebooks/                                    # utforskning / prototyping
│   └── temperaturmodell_trening.ipynb
└── README.md
---

## 📦 Modell-lagring og bruk

Modellene lastes automatisk fra Hugging Face ved hjelp av `huggingface_hub`. Eksempel fra `main.py`:

```python
from huggingface_hub import hf_hub_download
import joblib

modell_path = hf_hub_download("sushant/rf-weather-no", "random_forest_weather_model.pkl")
modell_7dager = joblib.load(modell_path)
```

Andre modeller hentes på samme måte.

---

## 📦 Komplett kode og modeller

- 🔗 Kode og data (7-Zip):  
  https://drive.google.com/drive/folders/1q0W5uYjPStoXrE6fEnBSwFMg9p0FwbzB?usp=sharing *(be om tilgang)*

- 🤖 Modellene er publisert på Hugging Face:
    | Modell | Repo-ID |
    |--------|---------|
    | 7-dagers temperatur | `sushant/rf-weather-no` |
    | Risiko – Tidspunkt | `sushant/risiko-tid` |
    | Risiko – Temperatur | `sushant/risiko-temp` |
    | Risiko – Værtype | `sushant/risiko-vaer` |
    | LabelEncoder | `sushant/risiko-encoder` |

---

## 🧠 Mer om prosjektet

Prosjektet benytter åpne datakilder som:

- **MET Norway (Frost & Locationforecast)**
- **Statens Vegvesen (NVDB API)** – for ulykkes- og trafikkdata
- **Kartverket (GeoJSON kommunegrenser)**

Formålet er å skape et prediktivt verktøy som både kan brukes til historisk analyse og i sanntid for trafikkplanlegging, beredskap og agronomi.

---

