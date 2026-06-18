# Sugama Sanchara - AI Traffic Command Center Frontend

## Overview

This is the **production-grade Streamlit frontend** for the Sugama Sanchara multi-agent AI traffic management system. The dashboard is designed to impress judges and stakeholders by presenting a professional, government-grade command center interface.

## 🎯 Key Features

### 1. **Command Center Interface**
- Professional header with system status indicators
- Real-time system health monitoring (3 AI agents ready, Flipkart connected)
- Clean, organized layout with intuitive navigation

### 2. **Event Input Panel**
- Dropdown selection for police stations (Peenya, HSR Layout, Wilson Garden, etc.)
- Time picker for event scheduling
- Environmental chaos factors:
  - ☔ Is Raining (adds 0.3x multiplier)
  - 💧 Active Waterlogging (adds 0.4x multiplier)
  - 🚨 VIP Movement (adds 0.6x multiplier)

### 3. **AI Agent Execution Visualizer**
- Animated pipeline showing 3-agent orchestration:
  - 🧠 **Intelligence Agent** - Analyzes historical patterns
  - 🗺️ **Strategy Agent** - Plans diversion routes
  - 🚓 **Logistics Agent** - Allocates resources
- Real-time progress indicators

### 4. **Key Performance Indicators (KPI Dashboard)**
- **Traffic Severity**: Shows multiplier and severity level (LOW/MEDIUM/HIGH/CRITICAL)
- **Base Anomaly**: Historical baseline intensity
- **Officers Required**: Resource allocation (0-8 max)
- **Barricades Needed**: Physical barriers (0-15 max)

### 5. **Congestion Risk Gauge**
- Interactive gauge chart showing risk percentage
- Color-coded risk levels
- SLA breach probability for Flipkart

### 6. **Interactive Bengaluru Map**
- **Event Location Marker**: Red pin showing incident zone
- **Congestion Impact Radius**: 2km blast zone visualization
- **Diversion Routes**: Green lines showing recommended bypass corridors
- **Adjacent Station Markers**: Green pins for diversion points
- **Network Ripple Effects**: Pressure indicators on neighboring stations

### 7. **Tactical Briefing Section**
- Human-readable operational directive
- Numbered deployment instructions
- Clear communication for traffic police

### 8. **Multi-Tab Analysis View**

#### Tab 1: Operations Summary
- Detailed incident metrics in table format
- Diversion corridor analysis
- Resource allocation summary

#### Tab 2: Flipkart Integration ⭐
- Live API integration with Flipkart logistics
- Real-time delivery impact assessment
- Fleet operational actions (PROCEED / DIVERGENT ROUTING / CRITICAL REROUTE)
- JSON response display for judges

#### Tab 3: Network Analysis
- Ripple propagation analysis
- Adjacent station pressure visualization
- Bar chart of network cascade effects

### 9. **Executive Summary Card**
- Quick reference for key recommendations
- Traffic severity at a glance
- Confirmation of Flipkart route updates

## 📋 Installation & Setup

### Prerequisites
- Python 3.8+
- Backend API running (see backend repository)
- Internet connection for maps

### 1. Clone Repository
```bash
git clone <repo-url>
cd frontend-sugama
```

### 2. Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Backend URL
The frontend defaults to `http://localhost:8000`. You can change this:

**Option A: Environment Variable**
```bash
# Windows
set API_URL=http://your-api-url:8000

# macOS/Linux
export API_URL=http://your-api-url:8000
```

**Option B: In-App Configuration**
- Use the "API Configuration" panel on the right side of the input section
- Enter custom backend URL

### 5. Run the Dashboard
```bash
streamlit run app.py
```

The application will open at `http://localhost:8501`

## 🔗 API Integration

### Connected Endpoints

#### 1. Health Check
```
GET /
```
Verifies backend is online

#### 2. Trigger Incident Analysis ⭐ PRIMARY
```
POST /api/v1/operations/trigger
```
**Request:**
```json
{
  "police_station": "Majestic",
  "timestamp_str": "2024-01-15 18:45",
  "environmental_factors": {
    "is_raining": true,
    "active_waterlogging": true,
    "vip_movement": false
  }
}
```

**Response:**
```json
{
  "status": "SUCCESS",
  "payload": {
    "target_location": "Majestic",
    "timestamp": "2024-01-15 18:45",
    "base_anomaly_intensity": 2.3,
    "compounded_chaos_intensity": 3.8,
    "recommended_diversion_corridors": ["Wilson Garden", "HSR Layout"],
    "network_ripple_impact": {
      "Wilson Garden": 1.75,
      "HSR Layout": 1.65
    },
    "allocated_personnel": 8,
    "allocated_barricades": 15,
    "logistics_directives": [...],
    "tactical_briefing": "...",
    "execution_status": "SUCCESS"
  }
}
```

#### 3. Flipkart Logistics Update
```
GET /api/v1/flipkart/logistics-update
```

**Response (Active Incident):**
```json
{
  "monitored_hub_sector": "Majestic",
  "compounded_congestion_index": 3.8,
  "recommended_bypass_corridors": ["Wilson Garden", "HSR Layout"],
  "fleet_operational_action": "CRITICAL_REROUTE_MANDATORY",
  "sla_breach_probability_pct": "98.5%",
  "projected_freight_delay_mins": 48,
  "supply_chain_cost_impact": "CRITICAL_SURGE",
  "telemetry_timestamp": "2024-01-15 18:45"
}
```

## 🏗️ File Structure

```
frontend-sugama/
├── app.py                    # Main Streamlit application
├── requirements.txt          # Python dependencies
├── README.md                 # This file
└── .env (optional)           # Environment variables
```

## 🎨 Design Features for Judge Impression

### Visual Hierarchy
1. **Header** - Immediately shows this is an official command center
2. **KPI Cards** - 4 key metrics at a glance
3. **Risk Gauge** - Professional risk visualization
4. **Interactive Map** - Tangible proof of spatial analysis
5. **Tabs** - Organized information without clutter

### Color Scheme
- **Primary**: Purple gradient (#667eea → #764ba2)
- **Success**: Green (#10b981)
- **Warning**: Amber (#f59e0b)
- **Critical**: Red (#ef4444)

### Professional Touches
- ✅ Animated agent execution pipeline
- ✅ Real-time Flipkart integration display
- ✅ Executive summary box
- ✅ Responsive layout for different screen sizes
- ✅ Consistent iconography (🚦 🧠 🗺️ 🚓)
- ✅ Clean typography and spacing

## 🚀 Usage Workflow

### For Judges
1. Open the dashboard
2. Select a police station (e.g., "Peenya")
3. Set an event time
4. Toggle environmental factors (rain, waterlogging, VIP movement)
5. Click "ANALYZE EVENT"
6. Watch the 3-agent pipeline execute in real-time
7. Review:
   - KPI metrics
   - Risk gauge
   - Interactive map with diversions
   - Flipkart logistics tab (shows commercial value)
   - Tactical briefing

### Expected Impression Points
- **Seconds 0-5**: Professional header + system status badges + clear input panel
- **Seconds 5-15**: Agent execution animation (shows multi-agent orchestration)
- **Seconds 15-30**: KPI cards + risk gauge (quantified impact)
- **Seconds 30-45**: Interactive map with visual markers (spatial intelligence)
- **Seconds 45-60**: Flipkart integration tab (commercial value + business impact)

## 🔧 Customization

### Change Backend URL
```python
# In the API Configuration panel or set environment variable
API_URL=http://your-backend-url:8000
```

### Modify Station Coordinates
Edit the `STATION_COORDINATES` dictionary in `app.py`:
```python
STATION_COORDINATES = {
    "YourStation": [latitude, longitude],
    ...
}
```

### Adjust Colors
Modify the CSS in the styling section at the top of `app.py`

### Add More Tabs
Add additional `st.tabs()` sections in the "Results Display" section

## 🐛 Troubleshooting

### Issue: "Could not connect to backend API"
- Ensure backend is running: `python -m uvicorn src.api:app --reload`
- Check backend URL in API Configuration panel
- Verify firewall isn't blocking port 8000

### Issue: Map not loading
- Check internet connection
- Ensure Folium library is installed: `pip install folium streamlit-folium`
- Clear browser cache

### Issue: Agent execution times out
- Backend may be processing slowly
- Check backend logs for errors
- Increase timeout in the API call function if needed

### Issue: Flipkart tab shows error
- Confirm `/api/v1/flipkart/logistics-update` endpoint exists in backend
- This endpoint should always return valid JSON (even if no active incidents)

## 📊 Performance Notes

- **Load Time**: ~2-3 seconds on first run (map tile loading)
- **API Response**: 1-3 seconds for agent orchestration
- **Visualization**: Real-time updates in <500ms

## 🎓 Hackathon Judge Tips

**What to Emphasize:**
1. **Multi-Agent Architecture** - Show how 3 agents collaborate
2. **Real Business Value** - Flipkart integration is the commercial win
3. **Spatial Intelligence** - Interactive map proves data-driven approach
4. **Resource Optimization** - KPI cards show efficient allocation
5. **Human-Readable Output** - Tactical briefing proves explainability

**Demo Sequence:**
1. Start with clear event selection
2. Trigger an incident with high chaos factors (rain + waterlogging + VIP)
3. Let judges watch the 3-agent animation
4. Show the resulting risk gauge (impressive visual)
5. Zoom into the Bengaluru map showing diversions
6. **Close the loop** by showing Flipkart tab with delivery impact
7. Reference executive summary showing quantified outcomes

## 📱 Responsive Design

The dashboard is optimized for:
- 📺 Large displays (1920x1080+)
- 💻 Standard monitors (1366x768)
- 📱 Tablets (landscape orientation)
- Mobile viewing supported but optimized for desktop judging

## 🔐 Security Notes

- No API keys stored in frontend
- Backend URL is configurable (no hardcoding)
- Environment variables for sensitive config
- Assumes HTTPS for production deployment

## 📝 License

Part of Sugama Sanchara - Flipkart Supply Chain Hackathon 2026

## 🤝 Support

For issues or questions:
1. Check backend logs
2. Verify API endpoints are responding
3. Review error messages in app info/warning boxes
4. Restart Streamlit: `streamlit run app.py --logger.level=debug`

---

**Made with 💜 for Flipkart Supply Chain Innovation Challenge**

## 📦 Push to GitHub & Integrate with Backend

If you'd like to push this frontend to your GitHub repository and wire it to the backend at https://github.com/bhoomika1705126/Sugama-Sanchara, follow the steps below.

1. Update remote (or use the helper script)

Windows (run in PowerShell):

```powershell
.\push_to_github.bat
```

macOS / Linux:

```bash
chmod +x push_to_github.sh
./push_to_github.sh
```

The scripts set the remote to `https://github.com/bhoomika1705126/Sugama-Sanchara.git`, initialize the git repository (if needed), commit and push the current tree to `main`.

2. Set the backend URL for runtime

By default the frontend will call `http://localhost:8000`. To point to a deployed backend, set the `API_URL` environment variable before starting Streamlit, for example:

```bash
export API_URL=https://your-backend-host:8000   # macOS / Linux
set API_URL=https://your-backend-host:8000      # Windows
```

3. CI (optional)

A minimal GitHub Actions workflow is included at `.github/workflows/ci.yml` which verifies Python syntax on push/PRs. Extend it to run tests or deploy the app.

4. Notes & permissions

- You must have push permissions to `https://github.com/bhoomika1705126/Sugama-Sanchara.git` or replace the URL with a repo you own/fork.
- For automation (CI/CD), prefer a self-hosted OSRM or a routing provider with an API key (do not embed keys in the repo).
- Backend integration is controlled at runtime by `API_URL` so no code changes are required to switch endpoints.
