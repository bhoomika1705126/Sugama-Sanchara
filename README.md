# Sugama-Sanchara: Spatiotemporal Multi-Agent Traffic Routing Matrix

An enterprise-grade, localized multi-agent orchestration architecture designed to optimize traffic gridlock anomalies across Bengaluru. Powered by real-world historical event streams from the **ASTraM (Advanced Traffic Management System)** dataset, the platform evaluates spatiotemporal congestion patterns and calculates defensive physical asset deployments and routing bypass matrices under strict resource boundary thresholds.

---

## 🏗️ Core System Architecture

The platform decouples dense analytical ingestion calculations from real-time operational routing pipelines. By structuring logic into a low-latency offline training phase and a deterministic multi-agent evaluation grid, the application maintains high performance under heavy system load.

`	ext
       [ Raw ASTraM Data Streams ]  ---> ( Drops Malformed Rows / Truncates Strings )
                  |
                  v
       [ Ingestion Processing Engine ]  ---> ( Resolves Varied Flags into Unified Bitmasks )
                  |
                  v
       [ Serialized Data Matrix ]   ---> ( Cached Locally into models/demand_model.pkl )
                  |
  +---------------v-------------------------------------------------------------------+
  | Real-Time Orchestration Grid (src/agents.py)                                      |
  |                                                                                   |
  |  [ Intelligence Node ]  ---> Extracts 4-hour temporal shifts & calculates         |
  |                              historical localized anomaly multipliers.            |
  |           |                                                                       |
  |           v                                                                       |
  |  [ Strategy Node ]      ---> Evaluates adjacent network graphs and filters out    |
  |                              over-saturated boundary pathways.                    |
  |           |                                                                       |
  |           v                                                                       |
  |  [ Logistics Node ]     ---> Maps infrastructure distribution (Officers/Barricades)  |
  |                              constrained by local station inventory ceilings.      |
  +-----------------------------------------------------------------------------------+
`

## 📌 Frontend Overview

This repository contains the Streamlit frontend for the Sugama Sanchara traffic orchestration platform. It is designed to present a professional operational command center with live backend health, incident inputs, AI agent orchestration, and route diversion visualization for Bengaluru.

## 🎯 Frontend Features

- Real-time system health badges for backend and Flipkart connectivity
- Incident input panel with station selection, time, and environmental chaos factors
- AI orchestration visualizer showing Intelligence, Strategy, and Logistics agents
- KPI dashboard with traffic severity, resource allocation, and breach risk indicators
- Interactive Bengaluru map with incident marker, diversion routes, and adjacent station impact
- Flipkart logistics integration tab with delivery-impact telemetry and route recommendations
- Tactical briefing and executive summary for rapid operational decisions

## 📋 Installation & Setup

### Prerequisites
- Python 3.8+
- Backend API running
- Internet connection for maps (Folium tile loading)

### 1. Clone the repository
`ash
git clone https://github.com/bhoomika1705126/Sugama-Sanchara.git
cd frontend/sugama/frontend/sugama
`

### 2. Create a virtual environment
`ash
python -m venv venv
venv/Scripts/activate
`

### 3. Install dependencies
`ash
pip install -r requirements.txt
`

### 4. Configure backend URL
The frontend defaults to http://localhost:8000. To change it:

`powershell
set API_URL=http://your-backend-url:8000
`

For Streamlit Cloud, set the `API_URL` environment variable in your app settings or secrets panel to the public backend URL.

### 5. Run the dashboard
`ash
streamlit run app.py
`

Open the app at http://localhost:8501.

## 🔌 API Integration

### Health check
- GET /

### Incident trigger
- POST /api/v1/operations/trigger

### Flipkart logistics update
- GET /api/v1/flipkart/logistics-update

## 🗂️ File Structure

`
frontend-sugama/
├── app.py                    # Main Streamlit application
├── app_old.py                # Legacy frontend variant
├── requirements.txt          # Python dependencies
├── README.md                 # This file
├── .github/                  # CI workflow files
├── scripts/                  # Helper scripts and syntax checks
└── .env.example              # Optional environment config template
`

## 🚀 Push to GitHub & Backend Integration

Use the helper scripts to push the frontend and keep the remote in sync.

Windows:
`powershell
.\push_to_github.bat
`

macOS/Linux:
`ash
chmod +x push_to_github.sh
./push_to_github.sh
`

To point the app at a deployed backend, set:
`powershell
set API_URL=https://your-backend-host:8000
`

## 📌 Notes

- Prefer a secure routing provider for production instead of the OSRM demo server.
- Do not store production API keys in source control.
- API_URL controls the runtime backend endpoint.

---

Made with 💜 for the Sugama Sanchara initiative.
