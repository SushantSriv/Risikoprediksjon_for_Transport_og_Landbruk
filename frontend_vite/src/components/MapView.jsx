import { MapContainer, TileLayer, Marker, Popup, useMapEvents } from 'react-leaflet';
import { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

// Standard og valgt markør
const blueIcon = new L.Icon({
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41]
});

const redIcon = new L.Icon({
  iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-red.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41]
});



function MapView() {
  const [stations, setStations] = useState([]);
  const [visibleStations, setVisibleStations] = useState([]);
  const [mapZoom, setMapZoom] = useState(5);
  const [mapBounds, setMapBounds] = useState(null);
  const [selectedStation, setSelectedStation] = useState(null);
  const [searchTerm, setSearchTerm] = useState("");

  const mapRef = useRef(null);

  useEffect(() => {
    axios.get('/data/stations.json').then(res => setStations(res.data));
  }, []);

  const MapWatcher = () => {
    useMapEvents({
      moveend: (e) => {
        const map = e.target;
        setMapZoom(map.getZoom());
        setMapBounds(map.getBounds());
      }
    });
    return null;
  };

  useEffect(() => {
    if (!mapBounds || stations.length === 0) return;
    let filtered = [];

    if (mapZoom < 7) {
      filtered = stations.slice(0, 10);
    } else if (mapZoom < 10) {
      filtered = Object.values(stations.reduce((acc, curr) => {
        if (!acc[curr.kommune]) acc[curr.kommune] = curr;
        return acc;
      }, {}));
    } else {
      filtered = stations.filter(st => {
        const latlng = L.latLng(st.latitude, st.longitude);
        return mapBounds.contains(latlng);
      });
    }

    setVisibleStations(filtered);
  }, [mapBounds, mapZoom, stations]);

  const fetchWeather = (station) => {
    const now = new Date();
    const kommune = station.kommune;
    const måned = now.toLocaleString('no-NO', { month: 'long' }).toLowerCase();
    const år = now.getFullYear();
    const tid = now.toTimeString().slice(0, 5);

    axios.get('/api/weather', {
      params: { lat: station.latitude, lon: station.longitude, kommune, måned, år, tid }
    }).then(res => {
      const updatedStation = { ...station, weather: res.data };
      setStations(prev =>
        prev.map(s => s.station_id === station.station_id ? updatedStation : s)
      );
      setSelectedStation(updatedStation);
    }).catch(err => {
      console.error("Feil under henting:", err);
    });
  };

  const handleSearch = () => {
    const term = searchTerm.trim().toLowerCase();
    if (!term || stations.length === 0) {
      alert("Skriv inn kommunenavn og vent til data er lastet.");
      return;
    }

    const match = stations.find(s =>
      s.kommune && s.kommune.toLowerCase().includes(term)
    );

    if (match && mapRef.current) {
      mapRef.current.flyTo([match.latitude, match.longitude], 11, {
        duration: 1.5
      });
      fetchWeather(match);
    } else {
      alert("Ingen treff på kommunenavn.");
    }
  };

  const risikoFarge = (nivå) => {
    if (!nivå) return "#333";
    if (nivå === "høy") return "red";
    if (nivå === "middels") return "orange";
    return "green";
  };
  
  const antallKommuner = new Set(stations.map(s => s.kommune.toLowerCase())).size;
  const matchingKommuner = stations.filter(s =>
    s.kommune?.toLowerCase().includes(searchTerm.trim().toLowerCase())
  );
  const unikeTreff = new Set(matchingKommuner.map(s => s.kommune?.toLowerCase())).size;
  return (
    <>
      {/* 🔍 Søkeboks */}
	<div
	  onKeyDown={(e) => e.key === "Enter" && handleSearch()}
	  style={{
		position: "absolute",
		top: 20,
		left: "50%",
		transform: "translateX(-50%)",
		zIndex: 1000,
		background: "white",
		padding: "12px 18px",
		borderRadius: "8px",
		boxShadow: "0 4px 10px rgba(0, 0, 0, 0.15)",
		display: "flex",
		flexDirection: "column", // viktig for stacking!
		alignItems: "center",
		gap: "8px"
	  }}
	>
	  <div style={{ display: "flex", gap: "10px" }}>
		<input
		  type="text"
		  placeholder={`Søk kommune (${antallKommuner} tilgjengelig)`}
		  value={searchTerm}
		  onChange={(e) => setSearchTerm(e.target.value)}
		  style={{
			padding: "8px 12px",
			fontSize: "14px",
			border: "1px solid #ccc",
			borderRadius: "4px",
			minWidth: "200px"
		  }}
		/>
		<button
		  onClick={handleSearch}
		  style={{
			padding: "8px 16px",
			background: "#2e6edb",
			color: "white",
			border: "none",
			borderRadius: "4px",
			fontWeight: "bold",
			cursor: "pointer"
		  }}
		>
		  Søk
		</button>
	  </div>

	  {searchTerm && (
		<div style={{ fontSize: "13px", color: "#555" }}>
		  Treff: {unikeTreff} kommune{unikeTreff === 1 ? "" : "r"}
		</div>
	  )}
	</div>
			
      

      {/* 🗺️ Kart */}
      <div style={{ height: "100vh", width: "100%" }}>
        <MapContainer
          ref={mapRef}
          center={[65.0, 15.0]}
          zoom={5}
          minZoom={4}
          maxZoom={13}
          style={{ height: "100vh", width: "100%" }}
        >
          <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
          <MapWatcher />
          {visibleStations.map((station) => (
            <Marker
              key={station.station_id}
              position={[station.latitude, station.longitude]}
              icon={
                selectedStation?.station_id === station.station_id ? redIcon : blueIcon
              }
              eventHandlers={{ click: () => fetchWeather(station) }}
            >
              <Popup>
                <div>
                  <strong>{station.kommune}</strong><br />
                  {station.weather ? (
                    <>
                      🌡 Nå: {station.weather.temperature ?? "ukjent"}°C<br />
                      💨 Vind: {station.weather.wind ?? "ukjent"} m/s<br />
                      🌧 Nedbør: {station.weather.precipitation ?? "ukjent"} mm<br />
                      ⚠️ Risiko: {station.weather.total_risiko ?? "?"}<br />
                      {station.weather.symbol && (
                        <img
                          src={`https://api.met.no/images/weathericons/svg/${station.weather.symbol}.svg`}
                          alt={station.weather.symbol}
                          width="40"
                        />
                      )}
                      <br />
                    </>
                  ) : (
                    "Klikk for vær og risiko"
                  )}
                </div>
              </Popup>
            </Marker>
          ))}
        </MapContainer>

        {/* 📊 Infopanel */}
        <div
          style={{
            position: "absolute",
            top: 90,
            right: 20,
            zIndex: 1000,
            width: "300px",
            maxHeight: "75vh",
            background: "#fff",
            padding: "16px",
            borderRadius: "8px",
            boxShadow: "0 4px 16px rgba(0, 0, 0, 0.15)",
            overflowY: "auto",
            fontFamily: "Arial, sans-serif"
          }}
        >
          {selectedStation && selectedStation.weather ? (
            <>
              <h2 style={{ marginBottom: "0.5rem" }}>{selectedStation.kommune}</h2>
              <p><strong>🌡 Temperatur nå:</strong> {selectedStation.weather.temperature}°C</p>
              <p><strong>💨 Vind:</strong> {selectedStation.weather.wind} m/s</p>
              <p><strong>🌧 Nedbør:</strong> {selectedStation.weather.precipitation} mm</p>

              <h3 style={{ marginTop: "1rem" }}>🔍 Risikoanalyse</h3>
              <p><strong>🕒 Tidspunkt:</strong> <span style={{ color: risikoFarge(selectedStation.weather.risiko_tid) }}>{selectedStation.weather.risiko_tid}</span></p>
              <p><strong>🌡 Temperatur:</strong> <span style={{ color: risikoFarge(selectedStation.weather.risiko_temp) }}>{selectedStation.weather.risiko_temp}</span></p>
              <p><strong>🌫 Værforhold:</strong> <span style={{ color: risikoFarge(selectedStation.weather.risiko_vaer) }}>{selectedStation.weather.risiko_vaer}</span></p>
              <p><strong>⚠️ Samlet:</strong> <span style={{ color: risikoFarge(selectedStation.weather.total_risiko), fontWeight: "bold" }}>{selectedStation.weather.total_risiko}</span></p>

              <h4 style={{ marginTop: "1rem" }}>🗓 Forventet temperatur:</h4>
              <ul style={{ paddingLeft: "1.2rem" }}>
                {selectedStation.weather.forecast_7_days?.map((d, i) => (
                  <li key={i}>{d.date}: {d.temp} °C</li>
                ))}
              </ul>
            </>
          ) : (
            <p>📍 Klikk på et punkt i kartet for detaljer</p>
          )}
        </div>
      </div>
    </>
  );
}

export default MapView;
