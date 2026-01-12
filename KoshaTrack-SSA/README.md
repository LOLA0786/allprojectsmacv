# 🛰️ KoshaTrack - Sovereign Space Situational Awareness Platform

AI-Powered Orbit Intelligence for Peaceful Skies & Secure Borders

## 🚀 Features

- **Real-time satellite tracking** (30,000+ objects)
- **AI collision prediction** (7-30 day horizon)
- **Anomaly detection** for unreported maneuvers
- **Blockchain orbit ledger** for sovereignty
- **Multi-source data fusion** (TLE, optical, radar)
- **FastAPI + WebSocket** backend
- **Dual-use architecture** (civil + defense)

## 🏃 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run Quick Test
```bash
python quick_test.py
```

### 3. Fetch Live TLE Data
```bash
python src/utils/tle_fetcher.py
```

### 4. Start API Server
```bash
uvicorn src.api.app:app --reload
```

### 5. Access API
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## 📊 Tech Stack

- Python 3.9+
- FastAPI (REST + WebSocket)
- SGP4/Skyfield (orbit propagation)
- Scikit-learn (ML models)
- Web3.py (blockchain)

## 🎯 Roadmap

- [x] Core orbit propagator
- [x] TLE data fetcher
- [x] REST API
- [ ] WebSocket real-time updates
- [ ] ML anomaly detection
- [ ] Blockchain ledger
- [ ] WhatsApp/Telegram alerts
- [ ] 3D visualization
- [ ] iDEX/IN-SPACe grant applications

## 📝 License

MIT

## 🇮🇳 Made for India's Space Sovereignty

Built with ❤️ for Atmanirbhar Bharat
