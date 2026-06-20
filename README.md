# 🚦 Sugama Sanchara

### Autonomous AI Traffic Command Center for Smart Urban Mobility

![Python](https://img.shields.io/badge/Python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green)
![Streamlit](https://img.shields.io/badge/Streamlit-Frontend-red)
![AI](https://img.shields.io/badge/AI-Multi--Agent-orange)
![Deployment](https://img.shields.io/badge/Deployment-Render%20%7C%20Streamlit-success)

---

## 🌟 Overview

**Sugama Sanchara** is an AI-powered traffic command center designed to help city authorities proactively manage traffic incidents, congestion, and mobility disruptions.

The platform combines:

* 🧠 Multi-Agent AI Coordination
* 📊 Predictive Traffic Intelligence
* 🗺️ Dynamic Diversion Planning
* 🚓 Resource Allocation Optimization
* 📦 Logistics Impact Assessment
* 🚦 Smart Decision Support Dashboard

Instead of reacting to congestion after it occurs, Sugama Sanchara predicts disruptions and recommends the most effective response strategy.

---

## 🚨 Problem Statement

Modern cities face increasing traffic challenges due to:

* Vehicle breakdowns
* Road accidents
* VIP movements
* Public events and gatherings
* Construction activities
* Weather-related disruptions

Current traffic management systems are often reactive and fragmented.

Authorities lack:

* Real-time impact estimation
* Predictive decision support
* Automated diversion planning
* Resource optimization
* Logistics impact visibility

---

## 💡 Solution

Sugama Sanchara acts as an intelligent command center that analyzes incidents and coordinates multiple AI agents to generate an optimized response plan.

The system can:

✅ Predict congestion impact

✅ Generate diversion strategies

✅ Recommend police deployment

✅ Estimate network-wide disruption

✅ Assess logistics and delivery impact

✅ Provide operational briefings in real time

---

## 🏗️ System Architecture

```text
User Dashboard (Streamlit)
            │
            ▼
      FastAPI Backend
            │
            ▼
   Multi-Agent Orchestrator
            │
 ┌──────────┼──────────┐
 │          │          │
 ▼          ▼          ▼
Intelligence Strategy Logistics
 Agent        Agent      Agent
 │             │          │
 └───────► Demand Model ◄─┘
            │
            ▼
     Unified Response Plan
            │
            ▼
      Interactive Dashboard
```

---

## 🤖 AI Agents

### 🧠 Intelligence Agent

Responsibilities:

* Historical incident analysis
* Congestion pattern detection
* Traffic impact estimation
* Risk assessment

Outputs:

* Congestion severity
* Predicted demand surge
* Impact score

---

### 🗺️ Strategy Agent

Responsibilities:

* Diversion route planning
* Network optimization
* Bottleneck identification

Outputs:

* Recommended routes
* Congestion mitigation plans

---

### 🚓 Logistics Agent

Responsibilities:

* Police resource allocation
* Traffic personnel deployment
* Incident response coordination

Outputs:

* Deployment recommendations
* Operational response plans

---

## 📊 Key Features

### 🚦 Incident Simulation

Simulate:

* Vehicle breakdowns
* Road accidents
* Public gatherings
* VIP movements
* Weather disruptions

---

### 🗺️ Interactive Traffic Map

Visualize:

* Incident locations
* Diversion routes
* Risk zones
* Operational hotspots

---

### 📈 Predictive Analytics

Provides:

* Traffic demand forecasting
* Congestion prediction
* Impact scoring

---

### 📦 Logistics Impact Monitoring

Estimates:

* Delivery delays
* Route disruptions
* Supply chain impact

---

### 📋 Operational Briefing Generator

Automatically generates:

* Situation summary
* Recommended actions
* Resource deployment plans

---

## 🛠️ Tech Stack

### Frontend

* Streamlit
* Plotly
* Folium
* Streamlit-Folium

### Backend

* FastAPI
* Uvicorn

### AI & Analytics

* Python
* Pandas
* NumPy
* Scikit-Learn

### Deployment

* Render (Backend)
* Streamlit Community Cloud (Frontend)

---

## 📂 Project Structure

```text
Sugama-Sanchara/
│
├── app.py
├── requirements.txt
├── render.yaml
│
├── src/
│   ├── api.py
│   ├── agents.py
│   ├── orchestrator.py
│   └── utils.py
│
├── dataset/
│   └── astram_events.csv
│
├── models/
│   └── demand_model.pkl
│
└── README.md
```

---

## 🚀 Installation

### Clone Repository

```bash
git clone https://github.com/bhoomika1705126/Sugama-Sanchara.git
cd Sugama-Sanchara
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Environment

Windows:

```bash
venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Run Backend

```bash
uvicorn src.api:app --reload --host 0.0.0.0 --port 8000
```

Backend:

```text
http://localhost:8000
```

Swagger Docs:

```text
http://localhost:8000/docs
```

---

## ▶️ Run Frontend

```bash
streamlit run app.py
```

Frontend:

```text
http://localhost:8501
```

---

## 🌐 Deployment

### Backend

Hosted on Render:

```text
https://sugama-backend.onrender.com
```

### Frontend

Hosted on Streamlit Community Cloud.
```text
https://sugama-sanchara-smmxktkdmqe9eujhzfnmtw.streamlit.app/
```
---

## 🎯 Future Enhancements

* Real-time traffic feeds
* Google Maps integration
* Emergency vehicle prioritization
* Crowd event forecasting
* Smart signal optimization
* IoT sensor integration
* Digital twin traffic simulation
* LLM-powered command center assistant

---

## 👩‍💻 Team TRIFUSION

**Bhoomika N\n**
**Gangaparameshwari D\n**
**B M Keerthana**


---

## 🏆 Vision

To build a proactive, AI-driven urban mobility ecosystem that helps cities reduce congestion, improve emergency response, and enable smarter transportation decisions.

**"Predict. Coordinate. Optimize. Move Smarter."**
