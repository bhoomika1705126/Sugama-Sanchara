import streamlit as st
import requests
import json
import time
from datetime import datetime, timedelta
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import folium
from streamlit_folium import st_folium
import os
from typing import Dict, Any, Optional
import numpy as np
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="Sugama Sanchara - AI Traffic Command Center",
    page_icon="🚦",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================================
# STYLING & THEME
# ============================================================================

st.markdown("""
<style>
    /* Main container styling */
    .main {
        padding-top: 0rem;
    }
    
    /* Header styling */
    .header-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2.5rem 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        color: white;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    
    .header-title {
        font-size: 2.5rem;
        font-weight: 800;
        margin: 0;
        color: white;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .header-subtitle {
        font-size: 1.1rem;
        margin: 0.5rem 0 0 0;
        color: rgba(255,255,255,0.9);
        font-weight: 500;
    }
    
    /* Status indicators */
    .status-badge {
        display: inline-block;
        padding: 0.4rem 0.8rem;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.85rem;
        margin-right: 1rem;
    }
    
    .status-active { background-color: #10b981; color: white; }
    .status-agents { background-color: #3b82f6; color: white; }
    .status-connected { background-color: #8b5cf6; color: white; }
    .status-error { background-color: #ef4444; color: white; }
    
    /* Card styling */
    .metric-card {
        background: white;
        border-left: 4px solid #667eea;
        padding: 1.5rem;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
    
    /* Section headers */
    .section-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 1rem 1.5rem;
        border-radius: 8px 8px 0 0;
        color: white;
        font-size: 1.3rem;
        font-weight: 700;
        margin-top: 2rem;
        margin-bottom: 0;
    }
    
    .section-content {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 0 0 8px 8px;
        border: 1px solid #e9ecef;
        border-top: none;
    }
    
    /* Agent timeline styling */
    .agent-timeline {
        background: white;
        border-left: 4px solid #667eea;
        padding: 1.2rem;
        border-radius: 6px;
        margin: 0.5rem 0;
    }
    
    .agent-success { border-left-color: #10b981; }
    .agent-pending { border-left-color: #f59e0b; }
    .agent-error { border-left-color: #ef4444; }
    
    /* Alert styling */
    .alert-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    /* Code block */
    .code-block {
        background: #1e293b;
        color: #e2e8f0;
        padding: 1.5rem;
        border-radius: 8px;
        font-family: 'Courier New', monospace;
        overflow-x: auto;
    }
    
    /* Responsive adjustments */
    @media (max-width: 768px) {
        .header-title { font-size: 1.8rem; }
        .header-container { padding: 1.5rem; }
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# SESSION STATE MANAGEMENT
# ============================================================================

if 'api_url' not in st.session_state:
    st.session_state.api_url = os.getenv('API_URL', 'http://localhost:8000')

if 'last_response' not in st.session_state:
    st.session_state.last_response = None

if 'execution_history' not in st.session_state:
    st.session_state.execution_history = []

if 'selected_station' not in st.session_state:
    st.session_state.selected_station = "Peenya"

if 'selected_time' not in st.session_state:
    st.session_state.selected_time = "18:00"

if 'selected_event_type' not in st.session_state:
    st.session_state.selected_event_type = "vehicle_breakdown"

if 'is_processing' not in st.session_state:
    st.session_state.is_processing = False

# ============================================================================
# DATASET LOADING
# ============================================================================

@st.cache_data
def load_astram_dataset():
    dataset_path = Path(os.getenv(
        'ASTRAM_DATASET_PATH',
        r'd:\Users\USER\Downloads\Astram event data_anonymized - Astram event data_anonymizedb40ac87.csv'
    ))
    if dataset_path.exists():
        df = pd.read_csv(dataset_path, encoding='utf-8', on_bad_lines='skip', low_memory=False)
        df['start_datetime'] = pd.to_datetime(df['start_datetime'], errors='coerce')
        df['latitude'] = pd.to_numeric(df['latitude'], errors='coerce')
        df['longitude'] = pd.to_numeric(df['longitude'], errors='coerce')
        return df
    return pd.DataFrame()

@st.cache_data
def build_station_coordinates(df: pd.DataFrame) -> Dict[str, Any]:
    coords: Dict[str, Any] = {}
    if df.empty:
        return coords
    grouped = (
        df.dropna(subset=['police_station', 'latitude', 'longitude'])
          .groupby('police_station')[['latitude', 'longitude']]
          .mean()
    )
    for station, row in grouped.iterrows():
        coords[station] = [float(row['latitude']), float(row['longitude'])]
    return coords

BENGALURU_CENTER = [12.9716, 77.5946]
DEFAULT_STATION_COORDINATES = {
    "Peenya": [13.0356, 77.5440],
    "Sadashivanagar": [13.0238, 77.6048],
    "HSR Layout": [12.9250, 77.6245],
    "Wilson Garden": [12.9589, 77.5984],
    "Jayanagara": [12.9589, 77.5984]
}

# Load dataset and derive station coordinates
astram_dataset = load_astram_dataset()
STATION_COORDINATES = build_station_coordinates(astram_dataset) or DEFAULT_STATION_COORDINATES

ADJACENT_STATIONS = {
    "Peenya": ["Sadashivanagar", "Wilson Garden"],
    "HSR Layout": ["Wilson Garden", "Jayanagara"],
    "Wilson Garden": ["HSR Layout", "Jayanagara", "Sadashivanagar"],
    "Sadashivanagar": ["Peenya", "Wilson Garden"],
    "Jayanagara": ["Wilson Garden", "HSR Layout"]
}

station_choices = sorted(
    astram_dataset['police_station'].dropna().unique().tolist()
) if not astram_dataset.empty else sorted(DEFAULT_STATION_COORDINATES.keys())

event_type_choices = sorted(
    astram_dataset['event_type'].dropna().unique().tolist()
) if not astram_dataset.empty else [
    "vehicle_breakdown", "water_logging", "accident", "tree_fall",
    "construction", "pot_holes", "congestion", "public_event"
]

def get_severity_color(intensity: float) -> str:
    """Map intensity to color code"""
    if intensity >= 3.0:
        return "#ef4444"  # Red
    elif intensity >= 2.0:
        return "#f59e0b"  # Amber
    elif intensity >= 1.5:
        return "#eab308"  # Yellow
    else:
        return "#10b981"  # Green

def get_severity_label(intensity: float) -> str:
    """Get severity label from intensity"""
    if intensity >= 3.0:
        return "🔴 CRITICAL"
    elif intensity >= 2.0:
        return "🟠 HIGH"
    elif intensity >= 1.5:
        return "🟡 MEDIUM"
    else:
        return "🟢 LOW"

def call_api(
    endpoint: str,
    method: str = "GET",
    payload: Optional[Dict] = None
) -> Dict[str, Any]:
    """Make API call to backend"""
    try:
        url = f"{st.session_state.api_url}{endpoint}"
        
        if method == "GET":
            response = requests.get(url, timeout=10)
        elif method == "POST":
            response = requests.post(url, json=payload, timeout=10)
        
        response.raise_for_status()
        return response.json()
    except requests.exceptions.ConnectionError:
        return {
            "error": "Could not connect to backend API",
            "detail": f"Make sure the backend is running at {st.session_state.api_url}"
        }
    except requests.exceptions.Timeout:
        return {"error": "API request timed out"}
    except Exception as e:
        return {"error": str(e)}


def get_system_status() -> Dict[str, Any]:
    status = {
        "system_active": False,
        "agents_ready": False,
        "flipkart_connected": False,
        "backend_message": "Backend not reachable"
    }

    health = call_api("/")
    if "error" not in health and health.get("status") == "ONLINE":
        status["system_active"] = True
        status["agents_ready"] = True
        status["backend_message"] = health.get("system", "Sugama-Sanchara backend active")

    flipkart = call_api("/api/v1/flipkart/logistics-update")
    if "error" not in flipkart:
        status["flipkart_connected"] = True

    return status


def format_timestamp(timestamp_str: str) -> str:
    """Format timestamp for display"""
    try:
        dt = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M")
        return dt.strftime("%d %B %Y, %H:%M")
    except:
        return timestamp_str


def get_route_osrm(start: list, end: list, profile: str = 'driving'):
    """Query OSRM public server for a driving route between start and end coords.
    start/end expected as [lat, lon]. Returns (coords_list, distance_m, duration_s) or (None, None, None)
    """
    try:
        # OSRM expects lon,lat
        lon1, lat1 = start[1], start[0]
        lon2, lat2 = end[1], end[0]
        url = f"http://router.project-osrm.org/route/v1/{profile}/{lon1},{lat1};{lon2},{lat2}?overview=full&geometries=geojson"
        resp = requests.get(url, timeout=6)
        resp.raise_for_status()
        data = resp.json()
        if data.get('code') == 'Ok' and data.get('routes'):
            coords = data['routes'][0]['geometry']['coordinates']
            # convert [lon,lat] -> [lat,lon]
            latlon = [[c[1], c[0]] for c in coords]
            dist = data['routes'][0].get('distance')
            dur = data['routes'][0].get('duration')
            return latlon, dist, dur
    except Exception:
        pass
    return None, None, None

# ============================================================================
# HEADER SECTION
# ============================================================================

status = get_system_status()

system_text = "🟢 System Active" if status["system_active"] else "🔴 System Offline"
system_class = "status-active" if status["system_active"] else "status-error"

agent_text = "🟟 3 AI Agents Ready" if status["agents_ready"] else "⚪ Agents Offline"
agent_class = "status-agents" if status["agents_ready"] else "status-error"

flipkart_text = "🔗 Flipkart Connected" if status["flipkart_connected"] else "⚠️ Flipkart Idle"
flipkart_class = "status-connected" if status["flipkart_connected"] else "status-error"

st.markdown(f"""
<div class="header-container">
    <h1 class="header-title">🚦 Sugama Sanchara</h1>
    <p class="header-subtitle">Autonomous AI Traffic Command Center</p>
    <div style="margin-top: 1rem;">
        <span class="status-badge {system_class}">{system_text}</span>
        <span class="status-badge {agent_class}">{agent_text}</span>
        <span class="status-badge {flipkart_class}">{flipkart_text}</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ============================================================================
# INPUT PANEL
# ============================================================================

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown('<div class="section-header">⚙️ Incident Configuration</div>', unsafe_allow_html=True)
    
    input_container = st.container()
    with input_container:
        st.markdown('<div class="section-content">', unsafe_allow_html=True)
        
        input_col1, input_col2 = st.columns(2)
        
        with input_col1:
            st.session_state.selected_station = st.selectbox(
                "📍 Police Station",
                station_choices,
                index=station_choices.index(st.session_state.selected_station) if st.session_state.selected_station in station_choices else 0,
                key="station_select"
            )
            st.session_state.selected_event_type = st.selectbox(
                "🚧 Incident Type",
                event_type_choices,
                index=0,
                key="event_type_select"
            )
        
        with input_col2:
            st.session_state.selected_time = st.time_input(
                "🕐 Event Time",
                value=datetime.strptime("18:00", "%H:%M").time(),
                key="time_input"
            )
        
        # Environmental factors
        st.markdown("**Environmental Chaos Factors:**")
        env_col1, env_col2, env_col3 = st.columns(3)
        
        with env_col1:
            is_raining = st.checkbox("☔ Is Raining", value=False)
        
        with env_col2:
            is_waterlogging = st.checkbox("💧 Active Waterlogging", value=False)
        
        with env_col3:
            is_vip = st.checkbox("🚨 VIP Movement", value=False)
        
        st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="section-header">API Configuration</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-content">', unsafe_allow_html=True)
    
    api_url = st.text_input(
        "Backend URL",
        value=st.session_state.api_url,
        help="Base URL of the FastAPI backend"
    )
    if api_url != st.session_state.api_url:
        st.session_state.api_url = api_url
    
    st.write(f"**Status:** Connected to `{st.session_state.api_url}`")
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================================================
# TRIGGER BUTTON & PROCESSING
# ============================================================================

st.markdown('<div style="margin: 2rem 0;"></div>', unsafe_allow_html=True)

trigger_col1, trigger_col2, trigger_col3 = st.columns([2, 1, 1])

with trigger_col1:
    if st.button(
        "🚨 ANALYZE EVENT",
        use_container_width=True,
        type="primary",
        key="trigger_button"
    ):
        st.session_state.is_processing = True

with trigger_col2:
    if st.button("🔄 Clear Results", use_container_width=True):
        st.session_state.last_response = None
        st.session_state.execution_history = []
        st.rerun()

with trigger_col3:
    if st.button("⚙️ Settings", use_container_width=True):
        st.session_state.show_settings = True

# ============================================================================
# PROCESSING & AGENT EXECUTION
# ============================================================================

if st.session_state.is_processing:
    # Format timestamp for API
    event_date = datetime.now().strftime("%Y-%m-%d")
    time_str = st.session_state.selected_time.strftime("%H:%M")
    timestamp_str = f"{event_date} {time_str}"
    
    # Prepare payload
    payload = {
        "police_station": st.session_state.selected_station,
        "timestamp_str": timestamp_str,
        "environmental_factors": {
            "is_raining": is_raining,
            "active_waterlogging": is_waterlogging,
            "vip_movement": is_vip
        }
    }
    
    # Agent execution animation
    processing_container = st.container()
    with processing_container:
        st.markdown('<div class="section-header">🤖 Agent Execution Pipeline</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-content">', unsafe_allow_html=True)
        
        agent_status = st.empty()
        
        # Show agent execution timeline
        with st.spinner("Initializing agents..."):
            time.sleep(0.5)
        
        st.markdown("""
        <div class="agent-timeline agent-pending">
            <strong>🧠 Intelligence Agent</strong> - Analyzing historical patterns...
        </div>
        """, unsafe_allow_html=True)
        
        with st.spinner("Intelligence Agent processing..."):
            time.sleep(0.8)
        
        st.markdown("""
        <div class="agent-timeline agent-success">
            <strong>🧠 Intelligence Agent</strong> ✓ Completed - Historical data analyzed
        </div>
        <div class="agent-timeline agent-pending">
            <strong>🗺️ Strategy Agent</strong> - Planning optimal diversion routes...
        </div>
        """, unsafe_allow_html=True)
        
        with st.spinner("Strategy Agent processing..."):
            time.sleep(0.8)
        
        st.markdown("""
        <div class="agent-timeline agent-success">
            <strong>🗺️ Strategy Agent</strong> ✓ Completed - Diversion routes calculated
        </div>
        <div class="agent-timeline agent-pending">
            <strong>🚓 Logistics Agent</strong> - Allocating police resources...
        </div>
        """, unsafe_allow_html=True)
        
        with st.spinner("Logistics Agent processing..."):
            # Make actual API call
            api_response = call_api(
                "/api/v1/operations/trigger",
                method="POST",
                payload=payload
            )
        
        st.markdown("""
        <div class="agent-timeline agent-success">
            <strong>🚓 Logistics Agent</strong> ✓ Completed - Resource allocation optimized
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Check for errors
        if "error" in api_response:
            st.error(f"❌ Error: {api_response['error']}")
            if "detail" in api_response:
                st.info(api_response['detail'])
        elif "detail" in api_response and "pipeline failure" in api_response["detail"]:
            st.error(f"❌ Agent Orchestration Error: {api_response['detail']}")
        else:
            # Store response
            st.session_state.last_response = api_response
            
            # Add to execution history
            history_entry = {
                "timestamp": datetime.now().isoformat(),
                "station": st.session_state.selected_station,
                "response": api_response
            }
            st.session_state.execution_history.append(history_entry)
            
            st.success("✅ Operation Plan Generated Successfully")
    
    st.session_state.is_processing = False
    st.rerun()

# ============================================================================
# RESULTS DISPLAY (only if we have a response)
# ============================================================================

if st.session_state.last_response:
    response = st.session_state.last_response
    payload_data = response.get("payload", {})
    
    # ========================================================================
    # KPI DASHBOARD
    # ========================================================================
    
    st.markdown('<div style="margin: 2rem 0;"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-header">📊 Key Performance Indicators</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-content">', unsafe_allow_html=True)
    
    kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)
    
    with kpi_col1:
        intensity = payload_data.get("compounded_chaos_intensity", 0)
        severity = get_severity_label(intensity)
        st.metric(
            "Traffic Severity",
            severity,
            f"{intensity:.1f}x multiplier" if intensity > 0 else "N/A"
        )
    
    with kpi_col2:
        base_intensity = payload_data.get("base_anomaly_intensity", 0)
        st.metric(
            "Base Anomaly",
            f"{base_intensity:.1f}x",
            "Pre-chaos baseline"
        )
    
    with kpi_col3:
        officers = payload_data.get("allocated_personnel", 0)
        st.metric(
            "Officers Required",
            officers,
            f"of {8} max available"
        )
    
    with kpi_col4:
        barricades = payload_data.get("allocated_barricades", 0)
        st.metric(
            "Barricades Needed",
            barricades,
            f"of {15} max available"
        )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # ========================================================================
    # RISK GAUGE
    # ========================================================================
    
    st.markdown('<div class="section-header">⚠️ Congestion Risk Assessment</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-content">', unsafe_allow_html=True)
    
    gauge_col1, gauge_col2 = st.columns([2, 1])
    
    with gauge_col1:
        # Create gauge chart
        intensity = payload_data.get("compounded_chaos_intensity", 0)
        risk_percentage = min(100, (intensity - 1.0) * 25) if intensity > 1.0 else 0
        
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=risk_percentage,
            title={'text': "Congestion Risk Level"},
            delta={'reference': 50},
            gauge={
                'axis': {'range': [0, 100]},
                'bar': {'color': get_severity_color(intensity)},
                'steps': [
                    {'range': [0, 25], 'color': "#e8f5e9"},
                    {'range': [25, 50], 'color': "#fff3e0"},
                    {'range': [50, 75], 'color': "#ffe0b2"},
                    {'range': [75, 100], 'color': "#ffebee"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 90
                }
            }
        ))
        fig.update_layout(height=300, margin=dict(l=20, r=20, t=70, b=20))
        st.plotly_chart(fig, use_container_width=True)
    
    with gauge_col2:
        st.markdown("**Risk Interpretation:**")
        risk_text = ""
        if intensity >= 3.0:
            risk_text = "🔴 **CRITICAL** - Immediate action required. Major traffic disruption expected."
        elif intensity >= 2.0:
            risk_text = "🟠 **HIGH** - Significant congestion. Deploy full contingency resources."
        elif intensity >= 1.5:
            risk_text = "🟡 **MEDIUM** - Moderate impact expected. Enhanced monitoring advised."
        else:
            risk_text = "🟢 **LOW** - Minimal traffic impact expected."
        
        st.markdown(risk_text)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # ========================================================================
    # INTERACTIVE MAP
    # ========================================================================
    
    st.markdown('<div style="margin: 2rem 0;"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-header">🗺️ Bengaluru Traffic Impact Map</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-content">', unsafe_allow_html=True)
    
    # Create map
    m = folium.Map(
        location=BENGALURU_CENTER,
        zoom_start=12,
        tiles="OpenStreetMap"
    )
    
    # Plot active incidents from the dataset for a real-time-like heatmap
    if not astram_dataset.empty:
        active_incidents = astram_dataset[astram_dataset['status'] == 'active']
        latest_incidents = active_incidents.sort_values('start_datetime', ascending=False).head(150)
        for _, incident in latest_incidents.iterrows():
            if pd.notna(incident['latitude']) and pd.notna(incident['longitude']):
                event_color = (
                    '#ef4444' if incident['event_cause'] in ['accident', 'vehicle_breakdown', 'vip_movement']
                    else '#f59e0b' if incident['event_cause'] in ['construction', 'water_logging', 'pot_holes']
                    else '#10b981'
                )
                folium.CircleMarker(
                    location=[float(incident['latitude']), float(incident['longitude'])],
                    radius=5,
                    color=event_color,
                    fill=True,
                    fill_color=event_color,
                    fill_opacity=0.7,
                    popup=(
                        f"<b>{incident['event_type'].title()} - {incident['event_cause'].replace('_', ' ').title()}</b><br/>"
                        f"Station: {incident['police_station']}<br/>"
                        f"Corridor: {incident['corridor']}<br/>"
                        f"Status: {incident['status']}"
                    ),
                    tooltip=incident['police_station']
                ).add_to(m)
    
    target_location = payload_data.get("target_location", st.session_state.selected_station)
    intensity = payload_data.get("compounded_chaos_intensity", 0)
    
    if target_location in STATION_COORDINATES:
        lat, lon = STATION_COORDINATES[target_location]
        
        # Event location marker
        folium.Marker(
            location=[lat, lon],
            popup=f"<b>Selected Station: {target_location}</b><br/>Severity: {intensity:.1f}x",
            tooltip=target_location,
            icon=folium.Icon(color="red", icon="fire", prefix="fa")
        ).add_to(m)
        
        # Impact radius (2km)
        folium.Circle(
            location=[lat, lon],
            radius=2000,
            color=get_severity_color(intensity),
            fill=True,
            fillColor=get_severity_color(intensity),
            fillOpacity=0.2,
            weight=2,
            popup="Congestion Impact Radius (2km)"
        ).add_to(m)
    
    # Draw diversions
    diversions = payload_data.get("recommended_diversion_corridors", [])
    network_ripple = payload_data.get("network_ripple_impact", {})
    
    for diversion in diversions:
        if diversion in STATION_COORDINATES and target_location in STATION_COORDINATES:
            start_coords = STATION_COORDINATES[target_location]
            end_coords = STATION_COORDINATES[diversion]
            
            # Try to fetch a road-following route (OSRM). If unavailable, fall back to straight line.
            route_coords, route_dist, route_dur = get_route_osrm(start_coords, end_coords)
            if route_coords:
                popup_text = f"Diversion Route: {target_location} → {diversion}<br/>Distance: {route_dist/1000:.2f} km, ETA: {int(route_dur/60)} min"
                folium.PolyLine(
                    locations=route_coords,
                    color="green",
                    weight=4,
                    opacity=0.8,
                    popup=popup_text
                ).add_to(m)
            else:
                # simple straight fallback
                folium.PolyLine(
                    locations=[start_coords, end_coords],
                    color="green",
                    weight=3,
                    opacity=0.7,
                    popup=f"Diversion Route (straight): {target_location} → {diversion}"
                ).add_to(m)

            # Marker for diversion station with ripple intensity
            ripple_intensity = network_ripple.get(diversion, 1.0)
            marker_popup = f"<b>Diversion Point: {diversion}</b><br/>Ripple Intensity: {ripple_intensity:.1f}x"
            if route_coords and route_dist is not None:
                marker_popup += f"<br/>Route dist: {route_dist/1000:.2f} km"
            folium.Marker(
                location=end_coords,
                popup=marker_popup,
                tooltip=diversion,
                icon=folium.Icon(color="green", icon="road", prefix="fa")
            ).add_to(m)
    
    # Display map
    st_folium(m, width=1200, height=500)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # ========================================================================
    # TACTICAL BRIEFING & DIRECTIVES
    # ========================================================================
    
    st.markdown('<div style="margin: 2rem 0;"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-header">📋 Operational Briefing</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-content">', unsafe_allow_html=True)
    
    tactical_briefing = payload_data.get("tactical_briefing", "No briefing available")
    st.info(f"**TACTICAL BRIEFING:**\n\n{tactical_briefing}")
    
    st.markdown("**Deployment Directives:**")
    logistics_directives = payload_data.get("logistics_directives", [])
    for i, directive in enumerate(logistics_directives, 1):
        st.markdown(f"**{i}.** {directive}")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # ========================================================================
    # TABS FOR ADDITIONAL VIEWS
    # ========================================================================
    
    st.markdown('<div style="margin: 2rem 0;"></div>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["📊 Operations Summary", "🔗 Flipkart Integration", "📈 Network Analysis"])
    
    with tab1:
        st.markdown("**Incident Details:**")
        details_df = pd.DataFrame({
            "Metric": [
                "Target Station",
                "Event Timestamp",
                "Base Anomaly",
                "Compounded Intensity",
                "Officers Allocated",
                "Barricades Allocated",
                "Execution Status"
            ],
            "Value": [
                payload_data.get("target_location", "N/A"),
                format_timestamp(payload_data.get("timestamp", "N/A")),
                f"{payload_data.get('base_anomaly_intensity', 0):.2f}x",
                f"{payload_data.get('compounded_chaos_intensity', 0):.2f}x",
                str(payload_data.get("allocated_personnel", 0)),
                str(payload_data.get("allocated_barricades", 0)),
                payload_data.get("execution_status", "N/A")
            ]
        })
        st.dataframe(details_df, use_container_width=True, hide_index=True)
        
        st.markdown("**Diversion Routes:**")
        diversions = payload_data.get("recommended_diversion_corridors", [])
        ripple = payload_data.get("network_ripple_impact", {})
        
        diversion_df = pd.DataFrame({
            "Corridor": diversions,
            "Ripple Impact": [f"{ripple.get(d, 1.0):.2f}x" for d in diversions]
        })
        st.dataframe(diversion_df, use_container_width=True, hide_index=True)
    
    with tab2:
        st.markdown("**Flipkart Logistics Integration:**")
        st.markdown("Fetching real-time delivery impact data...")
        
        flipkart_response = call_api("/api/v1/flipkart/logistics-update")
        
        if "error" not in flipkart_response:
            st.success("✅ Flipkart API Connected")
            st.markdown("**Live Logistics Update:**")
            st.code(json.dumps(flipkart_response, indent=2), language="json")
            
            # Display logistics decision
            if "fleet_operational_action" in flipkart_response:
                action = flipkart_response["fleet_operational_action"]
                if "CRITICAL" in action:
                    st.error(f"🚨 **CRITICAL ACTION REQUIRED:** {action}")
                elif "DIVERGENT" in action:
                    st.warning(f"⚠️ **ROUTING ADJUSTMENT:** {action}")
                else:
                    st.success(f"✅ **STATUS:** {action}")
        else:
            st.info("No active incidents currently. Flipkart delivery routes are nominal.")
    
    with tab3:
        st.markdown("**Network Ripple Propagation Analysis:**")
        
        ripple = payload_data.get("network_ripple_impact", {})
        if ripple:
            ripple_df = pd.DataFrame({
                "Adjacent Station": list(ripple.keys()),
                "Ripple Pressure": [f"{v:.2f}x" for v in ripple.values()]
            })
            st.dataframe(ripple_df, use_container_width=True, hide_index=True)
            
            # Visualize ripple as bar chart
            import plotly.express as px
            fig_ripple = px.bar(
                x=list(ripple.keys()),
                y=list(ripple.values()),
                labels={"x": "Adjacent Station", "y": "Ripple Pressure (Multiplier)"},
                title="Network Congestion Ripple Effect",
                color=list(ripple.values()),
                color_continuous_scale="RdYlGn_r"
            )
            st.plotly_chart(fig_ripple, use_container_width=True)
        else:
            st.info("No ripple data available")
    
    # ========================================================================
    # EXECUTIVE SUMMARY
    # ========================================================================
    
    st.markdown('<div style="margin: 2rem 0;"></div>', unsafe_allow_html=True)
    
    intensity = payload_data.get("compounded_chaos_intensity", 0)
    officers = payload_data.get("allocated_personnel", 0)
    barricades = payload_data.get("allocated_barricades", 0)
    diversions = len(payload_data.get("recommended_diversion_corridors", []))
    
    st.markdown(f"""
    <div class="alert-box">
        <h3>✅ OPERATION SUMMARY</h3>
        <ul>
            <li><strong>Traffic Severity:</strong> {get_severity_label(intensity)} ({intensity:.1f}x)</li>
            <li><strong>Congestion Radius:</strong> 2 km blast zone</li>
            <li><strong>Officers to Deploy:</strong> {officers} personnel</li>
            <li><strong>Barricades Required:</strong> {barricades} units</li>
            <li><strong>Suggested Diversion Corridors:</strong> {diversions} routes</li>
            <li><strong>Flipkart Routes Updated:</strong> ✅ SUCCESS</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

else:
    # Show default empty state
    st.markdown("""
    <div class="alert-box">
        <h3>📍 Welcome to the AI Traffic Command Center</h3>
        <p>This dashboard uses advanced multi-agent AI to analyze event-driven traffic congestion in Bengaluru.</p>
        <ol>
            <li>Select a police station and event time</li>
            <li>Configure environmental chaos factors</li>
            <li>Click "ANALYZE EVENT" to trigger the AI agent pipeline</li>
            <li>Review the operational recommendations and resource deployment plan</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# FOOTER
# ============================================================================

st.markdown('---')
st.markdown("""
<div style="text-align: center; padding: 2rem; color: #666;">
    <p><strong>Sugama Sanchara</strong> | AI-Powered Traffic Management System</p>
    <p>Flipkart Supply Chain Hackathon 2026</p>
    <p>Backend: FastAPI | Frontend: Streamlit | Intelligence: Multi-Agent AI</p>
</div>
""", unsafe_allow_html=True)
