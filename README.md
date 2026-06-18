# Sugama-Sanchara: Spatiotemporal Multi-Agent Traffic Routing Matrix

An enterprise-grade, localized multi-agent orchestration architecture designed to optimize traffic gridlock anomalies across Bengaluru. Powered by real-world historical event streams from the **ASTraM (Advanced Traffic Management System)** dataset, the platform evaluates spatiotemporal congestion patterns and calculates defensive physical asset deployments and routing bypass matrices under strict resource boundary thresholds.

---

## 🏗️ Core System Architecture

The platform decouples dense analytical ingestion calculations from real-time operational routing pipelines. By structuring logic into a low-latency offline training phase and a deterministic multi-agent evaluation grid, the application maintains high performance under heavy system load.

```text
       [ Raw ASTraM Data Streams ]  ---> ( Drops Malformed Rows / Truncates Strings )
                  |
                  v
       [ Ingestion Processing Engine ] ---> ( Resolves Varied Flags into Unified Bitmasks )
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
