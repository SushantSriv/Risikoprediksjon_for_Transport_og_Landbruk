# 🌧️ Værbasert Risikoprediksjon for Transport og Landbruk
Et ende‑til‑ende‑system som kombinerer **34 år med historiske vær‑ og ulykkesdata** med **sanntids MET-vær** for å beregne trafikk‑ og driftsrisiko på kommunenivå i Norge.

Løsningen består av tre hoveddeler:
1. **Datainnsamling & forbehandling** – Python‑skript henter og prosesserer åpne data fra MET, Kartverket og Statens vegvesen.
2. **Maskinlæring** – tre risikomodeller (tidspunkt, temperatur, værforhold) + en 7‑dagers temperatur­modell.
3. **API & Frontend** – FastAPI som serverer prediksjoner, samt et React + Leaflet‑dashbord som viser risiko i sanntid.

> **Viktig 📦**  
> Tunge filer (f.eks. modell‑PKL, CSV‑eksporter, demo‑videoer) ligger **ikke** i Git‑repoet.  
> De hentes automatisk via skript når du kjører prosjektet første gang.

---
## 📁 Mappestruktur (kode som faktisk pushes)
```
vaerbasert-risikoprediksjon/
│
├── backend/                 # FastAPI‑tjeneste + nedlastingsskript
│   ├── main.py
│   ├── requirements.txt
│   └── get_assets.sh        # laster modeller & data ved behov
│
├── config/                  # .env‑eksempler, YAML/JSON-konfig
│
├── frontend_vite/           # React + Leaflet (Vite)
│   ├── src/
│   └── public/
│
├── scripts/                 # Datainnsamling & trening
│   ├── fetch_frost_weather_34yr.py
│   └── train_models.py
│
├── tests/                   # Pytest‑enhetstester
└── README.md
```

---
## 🔗 Datakilder (hentes ved kjøring)
| Kilde | Beskrivelse | Hentes av |
|-------|-------------|-----------|
| **FROST API (MET)** | Historiske temperatur‑, nedbør‑ og vinddata | `fetch_frost_weather_34yr.py` |
| **Kartverket / Geonorge** | Kommune‑ & fylkesgrenser (GeoJSON) | eget skript i `scripts/` |
| **Statens vegvesen – NVDB / TRINE** | Trafikkstasjoner & historiske ulykker | eget skript |

---
## 🤖 Maskinlærings­modeller
De ferdigtrente modellene lastes ned av `backend/get_assets.sh` (≈ 300 MB totalt) til en lokal `assets/`‑mappe.

| Fil (lokalt) | Formål | Algoritme | Output |
|--------------|--------|-----------|--------|
| `assets/modell_tidspunkt_pipeline.pkl` | Risiko – tidspunkt | RandomForest | lav / middels / høy |
| `assets/modell_temp_pipeline.pkl` | Risiko – temperatur | RandomForest | lav / middels / høy |
| `assets/modell_vaerforhold_pipeline.pkl` | Risiko – værtype | RandomForest | lav / middels / høy |
| `assets/random_forest_weather_model.pkl` | 7‑d temp | RandomForestRegressor | temp t+1 … t+7 |

---
## ⚙️ Komme i gang
```bash
# 1 Backend
cd backend
bash get_assets.sh                 # laster modeller & data (første gang)
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000   # http://localhost:8000/docs

# 2 Frontend
cd ../frontend_vite
npm install
npm run dev                                             # http://localhost:5173
```

`get_assets.sh` gjør bl.a.:
```bash
curl -L -o assets/models.zip "https://huggingface.co/ssriv/risikomodeller/resolve/main/models.zip"
unzip assets/models.zip -d assets && rm assets/models.zip
```
Du kan bytte til et annet lager (S3, Google Drive, etc.) ved å redigere URL‐en.

### Miljøvariabler
Legg `.env` i `backend/` med bl.a.
```
FROST_CLIENT_ID=…
FROST_CLIENT_SECRET=…
```

---
## 🎥 Demo‐video i README
1 Legg en **< 25 MB GIF** i `visualizations/` **eller** host MP4 eksternt (YouTube, Loom).  
Embed i Markdown:
```markdown
![Demo](visualizations/demo.gif)
```

---
## ☁️ Deploy (Railway)
```bash
railway login
railway init              # peker mot backend/
railway up                # Railway henter assets via get_assets.sh
```
Frontend bygges og deployes via Netlify/Vercel med `VITE_API_BASE` → Railway‑URL.

---
## 🛤 Videre arbeid
* Automatisk scheduler for å oppdatere modeller månedlig
* Prometheus‑metrics i FastAPI
* Docker‑Compose for backend + frontend

---
## 👤 Kontakt
**Sushant Srivastava**   |  sushant.nmbu@gmail.com  |  Norge

---
MIT License © 2025

