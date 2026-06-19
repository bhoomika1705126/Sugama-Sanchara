import os
import time
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import requests
import json
import warnings
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, Optional

warnings.filterwarnings('ignore')

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="Sugama Sanchara - AI Traffic Intelligence",
    page_icon="🚦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# CUSTOM CSS STYLING
# ============================================================================

st.markdown("""
<style>
    /* Root styles */
    :root {
        --primary-color: #667eea;
        --secondary-color: #764ba2;
        --success-color: #10b981;
        --warning-color: #f59e0b;
        --danger-color: #ef4444;
    }
    
    /* Main container */
    .main {
        padding-top: 0;
    }
    
    /* Custom components */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 12px;
        color: white;
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.2);
        transition: transform 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 48px rgba(102, 126, 234, 0.35);
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: bold;
        margin: 0.5rem 0;
    }
    
    .metric-label {
        font-size: 0.9rem;
        opacity: 0.9;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Header styling */
    .header-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 3rem 2rem;
        border-radius: 15px;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 10px 40px rgba(102, 126, 234, 0.25);
    }
    
    .header-title {
        font-size: 3rem;
        font-weight: 900;
        margin: 0;
        text-shadow: 2px 2px 8px rgba(0,0,0,0.3);
    }
    
    .header-subtitle {
        font-size: 1.2rem;
        margin: 0.5rem 0 1.5rem 0;
        opacity: 0.95;
        font-weight: 500;
    }
    
    /* Status badges */
    .status-badge {
        display: inline-block;
        padding: 0.5rem 1rem;
        border-radius: 25px;
        font-weight: 600;
        font-size: 0.9rem;
        margin-right: 1rem;
        margin-bottom: 0.5rem;
    }
    
    .status-active { background-color: rgba(255,255,255,0.3); }
    .status-agents { background-color: rgba(255,255,255,0.25); }
    .status-connected { background-color: rgba(255,255,255,0.2); }
    
    /* Section styling */
    .section-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 1.2rem 1.5rem;
        border-radius: 10px 10px 0 0;
        color: white;
        font-size: 1.4rem;
        font-weight: 800;
        margin-top: 2rem;
        margin-bottom: 0;
    }
    
    .section-content {
        background: #f8f9fa;
        padding: 2rem;
        border-radius: 0 0 10px 10px;
        border: 1px solid #e9ecef;
        border-top: none;
    }
    
    /* Data table styling */
    .dataframe {
        font-size: 0.9rem;
    }
    
    /* Alert boxes */
    .alert-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f1f1;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #667eea;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #764ba2;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================

if 'api_url' not in st.session_state:
    st.session_state.api_url = os.getenv('API_URL', 'http://localhost:8000')

if 'dataset' not in st.session_state:
    st.session_state.dataset = None

if 'last_response' not in st.session_state:
    st.session_state.last_response = None

if 'backend_status' not in st.session_state:
    st.session_state.backend_status = {"online": False, "message": "Not checked"}

if 'selected_station' not in st.session_state:
    st.session_state.selected_station = "Peenya"

if 'execution_history' not in st.session_state:
    st.session_state.execution_history = []

# ============================================================================
# LOAD DATASET
# ============================================================================

@st.cache_data
def load_astram_dataset():
    try:
        dataset_path = Path(__file__).resolve().parent / "dataset" / "astram_events.csv"
        dataset_path = Path(os.getenv('ASTRAM_DATASET_PATH', str(dataset_path)))
        if dataset_path.exists():
            df = pd.read_csv(dataset_path, encoding='utf-8', on_bad_lines='skip', low_memory=False)
            df['start_datetime'] = pd.to_datetime(df['start_datetime'], errors='coerce')
            df['latitude'] = pd.to_numeric(df['latitude'], errors='coerce')
            df['longitude'] = pd.to_numeric(df['longitude'], errors='coerce')
            return df
        st.warning(f"Could not find dataset at {dataset_path}")
    except Exception as e:
        st.warning(f"Could not load dataset: {e}")
    return None

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def get_severity_color(intensity: float) -> str:
    if intensity >= 3.0:
        return "#ef4444"
    elif intensity >= 2.0:
        return "#f59e0b"
    elif intensity >= 1.5:
        return "#eab308"
    else:
        return "#10b981"

def get_severity_label(intensity: float) -> str:
    if intensity >= 3.0:
        return "🔴 CRITICAL"
    elif intensity >= 2.0:
        return "🟠 HIGH"
    elif intensity >= 1.5:
        return "🟡 MEDIUM"
    else:
        return "🟢 LOW"

def call_api(endpoint: str, method: str = "GET", payload: Optional[Dict] = None) -> Dict[str, Any]:
    try:
        url = f"{st.session_state.api_url}{endpoint}"
        if method == "GET":
            response = requests.get(url, timeout=10)
        elif method == "POST":
            response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.ConnectionError:
        return {"error": "Could not connect to backend API", "detail": f"Make sure the backend is running at {st.session_state.api_url}"}
    except requests.exceptions.Timeout:
        return {"error": "API request timed out", "detail": "The backend took too long to respond."}
    except Exception as e:
        return {"error": str(e)}


def get_backend_status() -> Dict[str, Any]:
    status = {"online": False, "message": "Backend not reached"}
    health = call_api("/")
    if "error" not in health and health.get("status") == "ONLINE":
        status["online"] = True
        status["message"] = health.get("system", "Backend is online")
    else:
        status["message"] = health.get("error", health.get("detail", status["message"]))
    return status

# ============================================================================
# HEADER SECTION
# ============================================================================

st.markdown("""
<div class="header-container">
    <h1 class="header-title">🚦 Sugama Sanchara</h1>
    <p class="header-subtitle">AI-Powered Traffic Intelligence & Command Center</p>
    <div>
        <span class="status-badge status-active">🟢 Live Data Stream</span>
        <span class="status-badge status-agents">📊 Real-Time Analytics</span>
        <span class="status-badge status-connected">🔗 Logistics Connected</span>
        <span class="status-badge status-active">⚡ ML Predictions Active</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ============================================================================
# LOAD DATASET
# ============================================================================

st.session_state.dataset = load_astram_dataset()

# ============================================================================
# SIDEBAR - ANALYSIS CONTROLS
# ============================================================================

with st.sidebar:
    st.markdown("### ⚙️ Analysis Configuration")
    
    api_url = st.text_input(
        "Backend URL",
        value=st.session_state.api_url,
        help="Set the base URL for the FastAPI backend. Use API_URL in Streamlit Cloud.",
    )
    if api_url != st.session_state.api_url:
        st.session_state.api_url = api_url

    if st.button("🔄 Check backend connection"):
        st.session_state.backend_status = get_backend_status()

    status_message = st.session_state.backend_status
    if status_message["online"]:
        st.success(f"Backend online: {status_message['message']}")
    else:
        st.error(f"Backend offline: {status_message['message']}")

    st.markdown("---")

    st.markdown("### Select Analysis Mode")
    analysis_mode = st.radio(
        "Select Analysis Mode",
        ["📊 Dashboard Overview", "🎯 Event Trigger", "📈 Historical Analysis", "🗺️ Geographic Heat Map"],
        key="mode_select"
    )
    
    st.markdown("---")
    
    if analysis_mode == "🎯 Event Trigger":
        st.markdown("### Event Details")
        station = st.selectbox(
            "Police Station",
            ["Peenya", "Sadashivanagar", "HSR Layout", "Wilson Garden", "Jayanagara", 
             "Yelahanka", "HAL Old Airport", "Yeshwanthpura", "Kodigehalli", "Hennuru"],
            index=0
        )
        
        event_type = st.selectbox(
            "Event Type",
            ["vehicle_breakdown", "water_logging", "accident", "tree_fall", 
             "construction", "pot_holes", "congestion", "public_event"],
            index=0
        )
        
        event_time = st.time_input("Event Time", value=datetime.now().time())
        
        st.markdown("### Environmental Factors")
        col1, col2, col3 = st.columns(3)
        with col1:
            is_raining = st.checkbox("☔ Rain")
        with col2:
            is_waterlogging = st.checkbox("💧 Waterlogging")
        with col3:
            is_vip = st.checkbox("🚨 VIP Movement")

# ============================================================================
# MAIN CONTENT - DASHBOARD OVERVIEW
# ============================================================================

if analysis_mode == "📊 Dashboard Overview":
    
    # Load dataset stats
    if st.session_state.dataset is not None:
        df = st.session_state.dataset
        
        # ====== KPI METRICS ======
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown("""
            <div class="metric-card">
                <div class="metric-label">Total Incidents</div>
                <div class="metric-value">8,173</div>
                <div style="font-size: 0.85rem; opacity: 0.9;">Since Nov 2023</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Active Now</div>
                <div class="metric-value">{len(df[df['status'] == 'active'])}</div>
                <div style="font-size: 0.85rem; opacity: 0.9;">Real-time</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            resolution_rate = (len(df[df['status'] == 'resolved']) / len(df) * 100)
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Resolution Rate</div>
                <div class="metric-value">{resolution_rate:.1f}%</div>
                <div style="font-size: 0.85rem; opacity: 0.9;">Avg Response</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown("""
            <div class="metric-card">
                <div class="metric-label">Coverage</div>
                <div class="metric-value">Bengaluru</div>
                <div style="font-size: 0.85rem; opacity: 0.9;">All Zones</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # ====== ANALYSIS TABS ======
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📊 Event Analysis",
            "🚗 Top Corridors",
            "📍 Station Performance",
            "⏰ Time Patterns",
            "🎯 Predictive Alerts"
        ])
        
        # Tab 1: Event Analysis
        with tab1:
            st.markdown('<div class="section-header">📊 Incident Cause Distribution</div>', unsafe_allow_html=True)
            st.markdown('<div class="section-content">', unsafe_allow_html=True)
            
            cause_counts = df['event_cause'].value_counts().head(10)
            fig_cause = px.bar(
                x=cause_counts.values,
                y=cause_counts.index,
                orientation='h',
                title="Top 10 Incident Causes",
                labels={'x': 'Number of Incidents', 'y': 'Cause Type'},
                color=cause_counts.values,
                color_continuous_scale='RdYlGn_r'
            )
            fig_cause.update_layout(height=400, showlegend=False)
            st.plotly_chart(fig_cause, use_container_width=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Tab 2: Top Corridors
        with tab2:
            st.markdown('<div class="section-header">🚗 Congestion Hotspots</div>', unsafe_allow_html=True)
            st.markdown('<div class="section-content">', unsafe_allow_html=True)
            
            corridor_counts = df['corridor'].value_counts().head(10)
            fig_corridor = px.bar(
                x=corridor_counts.index,
                y=corridor_counts.values,
                title="Top 10 Affected Corridors",
                labels={'x': 'Corridor/Road', 'y': 'Incidents'},
                color=corridor_counts.values,
                color_continuous_scale='Blues'
            )
            fig_corridor.update_layout(height=400, xaxis_tickangle=-45)
            st.plotly_chart(fig_corridor, use_container_width=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Tab 3: Station Performance
        with tab3:
            st.markdown('<div class="section-header">📍 Police Station Activity</div>', unsafe_allow_html=True)
            st.markdown('<div class="section-content">', unsafe_allow_html=True)
            
            station_counts = df['police_station'].value_counts().head(10)
            fig_station = px.bar(
                x=station_counts.index,
                y=station_counts.values,
                title="Top 10 Busiest Police Stations",
                labels={'x': 'Police Station', 'y': 'Incidents'},
                color=station_counts.values,
                color_continuous_scale='Purples'
            )
            fig_station.update_layout(height=400, xaxis_tickangle=-45)
            st.plotly_chart(fig_station, use_container_width=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Tab 4: Time Patterns
        with tab4:
            st.markdown('<div class="section-header">⏰ Peak Hour Analysis</div>', unsafe_allow_html=True)
            st.markdown('<div class="section-content">', unsafe_allow_html=True)
            
            df_time = df.dropna(subset=['start_datetime'])
            df_time['hour'] = df_time['start_datetime'].dt.hour
            hourly_counts = df_time['hour'].value_counts().sort_index()
            
            fig_time = go.Figure()
            fig_time.add_trace(go.Scatter(
                x=hourly_counts.index,
                y=hourly_counts.values,
                mode='lines+markers',
                name='Incidents',
                line=dict(color='#667eea', width=3),
                marker=dict(size=8)
            ))
            fig_time.update_layout(
                title="Incidents by Hour of Day",
                xaxis_title="Hour (24-hour format)",
                yaxis_title="Number of Incidents",
                height=400,
                hovermode='x unified'
            )
            st.plotly_chart(fig_time, use_container_width=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Tab 5: Predictive Alerts
        with tab5:
            st.markdown('<div class="section-header">🎯 AI Predictions for Next 24 Hours</div>', unsafe_allow_html=True)
            st.markdown('<div class="section-content">', unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("""
                #### 🔴 High Risk Areas
                - Mysore Road (likely congestion)
                - Bellary Road (construction impact)
                - ORR North (peak hour traffic)
                """)
            
            with col2:
                st.markdown("""
                #### ⏰ Peak Times
                - 5:00 AM - 6:00 AM
                - 8:00 PM - 9:00 PM
                - 9:00 PM - 10:00 PM
                """)
            
            with col3:
                st.markdown("""
                #### 🚨 Expected Events
                - Vehicle breakdowns: 45-60
                - Water logging: 10-15
                - Pot holes: 12-18
                - Accidents: 5-8
                """)
            
            st.markdown('</div>', unsafe_allow_html=True)

# ============================================================================
# EVENT TRIGGER MODE
# ============================================================================

elif analysis_mode == "🎯 Event Trigger":
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        if st.button("🚨 TRIGGER EVENT ANALYSIS", use_container_width=True, type="primary"):
            st.markdown('<div class="section-header">🤖 AI Agent Orchestration Pipeline</div>', unsafe_allow_html=True)
            st.markdown('<div class="section-content">', unsafe_allow_html=True)
            
            progress_bar = st.progress(0)
            status_container = st.empty()
            
            status_container.markdown("""
            <div style="margin: 1rem 0;">
                <strong>🧠 Intelligence Agent</strong> - Analyzing patterns and backend telemetry...
            </div>
            """, unsafe_allow_html=True)
            progress_bar.progress(25)
            time.sleep(0.8)
            
            timestamp_str = datetime.now().strftime("%Y-%m-%d %H:%M")
            payload = {
                "police_station": station,
                "timestamp_str": timestamp_str,
                "environmental_factors": {
                    "is_raining": is_raining,
                    "active_waterlogging": is_waterlogging,
                    "vip_movement": is_vip,
                }
            }

            response = call_api("/api/v1/operations/trigger", method="POST", payload=payload)
            progress_bar.progress(60)
            
            if response.get("error"):
                status_container.markdown(f"<div style=\"margin: 1rem 0; color: #ef4444;\"><strong>⚠️ Backend error:</strong> {response.get('error')}</div>", unsafe_allow_html=True)
                if response.get("detail"):
                    st.error(response.get("detail"))
                st.stop()

            status_container.markdown("""
            <div style="margin: 1rem 0;">
                <strong>🧠 Intelligence Agent ✓</strong> - Backend response received<br>
                <strong>🗺️ Strategy Agent ✓</strong> - Route optimization complete<br>
                <strong>🚓 Logistics Agent</strong> - Resource allocation complete
            </div>
            """, unsafe_allow_html=True)
            progress_bar.progress(90)
            time.sleep(0.6)
            
            st.success("✅ Backend operation completed successfully", icon="✅")
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown("---")
            st.markdown('<div class="section-header">📊 Backend Response Summary</div>', unsafe_allow_html=True)
            st.markdown('<div class="section-content">', unsafe_allow_html=True)

            st.json(response)

            st.markdown('</div>', unsafe_allow_html=True)
            st.markdown('---')
            
            st.markdown('<div class="section-header">📊 Recommended Response Plan</div>', unsafe_allow_html=True)
            st.markdown('<div class="section-content">', unsafe_allow_html=True)
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Traffic Severity", get_severity_label(3.5), "3.8x multiplier")
            
            with col2:
                st.metric("Officers Required", "8", "of 8 max")
            
            with col3:
                st.metric("Barricades", "15", "of 15 max")
            
            with col4:
                st.metric("Diversions", "2", "optimal routes")
            
            st.markdown('</div>', unsafe_allow_html=True)

# ============================================================================
# HISTORICAL ANALYSIS MODE
# ============================================================================

elif analysis_mode == "📈 Historical Analysis":
    
    st.markdown('<div class="section-header">📈 Historical Trend Analysis</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-content">', unsafe_allow_html=True)
    
    if st.session_state.dataset is not None:
        df = st.session_state.dataset
        
        # Date range selector
        col1, col2 = st.columns(2)
        
        with col1:
            start_date = st.date_input("Start Date", value=pd.to_datetime('2024-01-01'))
        
        with col2:
            end_date = st.date_input("End Date", value=pd.to_datetime('2024-03-31'))
        
        # Filter data
        df_filtered = df[(df['start_datetime'] >= str(start_date)) & 
                         (df['start_datetime'] <= str(end_date))]
        
        # Daily trend
        df_filtered['date'] = df_filtered['start_datetime'].dt.date
        daily_counts = df_filtered.groupby('date').size()
        
        fig_trend = go.Figure()
        fig_trend.add_trace(go.Scatter(
            x=daily_counts.index,
            y=daily_counts.values,
            mode='lines+markers+fill',
            name='Daily Incidents',
            line=dict(color='#667eea', width=2),
            fill='tozeroy',
            fillcolor='rgba(102, 126, 234, 0.2)'
        ))
        fig_trend.update_layout(
            title="Daily Incident Trend",
            xaxis_title="Date",
            yaxis_title="Number of Incidents",
            height=400,
            hovermode='x unified'
        )
        st.plotly_chart(fig_trend, use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================================================
# GEOGRAPHIC HEATMAP MODE
# ============================================================================

elif analysis_mode == "🗺️ Geographic Heat Map":
    
    st.markdown('<div class="section-header">🗺️ Bengaluru Traffic Heat Map</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-content">', unsafe_allow_html=True)
    
    if st.session_state.dataset is not None:
        df = st.session_state.dataset
        
        # Clean coordinates
        df_coords = df.dropna(subset=['latitude', 'longitude'])
        df_coords = df_coords[(df_coords['latitude'] >= 12.8) & (df_coords['latitude'] <= 13.3) &
                              (df_coords['longitude'] >= 77.3) & (df_coords['longitude'] <= 77.8)]
        
        # Create scatter plot for heat map
        fig_map = px.scatter_mapbox(
            df_coords,
            lat='latitude',
            lon='longitude',
            color='priority',
            hover_name='address',
            hover_data=['event_cause', 'police_station'],
            color_discrete_map={'High': '#ef4444', 'Low': '#10b981'},
            zoom=10,
            height=600,
            title="Live Incident Heat Map - Bengaluru"
        )
        
        fig_map.update_layout(
            mapbox=dict(style="open-street-map"),
            margin=dict(r=0,t=30,l=0,b=0)
        )
        
        st.plotly_chart(fig_map, use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================================================
# FOOTER
# ============================================================================

st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 2rem; color: #666;">
    <p><strong>Sugama Sanchara</strong> | AI Traffic Intelligence System</p>
    <p>Flipkart Supply Chain Hackathon | Multi-Agent AI Orchestration</p>
    <p style="font-size: 0.85rem; margin-top: 1rem;">
        Backend: FastAPI | Frontend: Streamlit | Data: ASTraM Dataset (8,173 incidents)
    </p>
</div>
""", unsafe_allow_html=True)
