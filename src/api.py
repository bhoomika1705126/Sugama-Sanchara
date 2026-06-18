from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from src.orchestrator import GridlockOrchestrator

app = FastAPI(title="Sugama-Sanchara BTP Agent Ops Gateway", version="3.0.0")
orchestrator = GridlockOrchestrator()

class EnvironmentalFactors(BaseModel):
    is_raining: bool = False
    active_waterlogging: bool = False
    vip_movement: bool = False

class IncidentTrigger(BaseModel):
    police_station: str
    timestamp_str: str
    environmental_factors: EnvironmentalFactors

@app.get("/")
def read_root():
    return {"status": "ONLINE", "system": "Sugama-Sanchara Async Multi-Agent Core Engine Active"}

@app.post("/api/v1/operations/trigger")
async def trigger_incident_pipeline(payload: IncidentTrigger):
    env_dict = payload.environmental_factors.dict()
    updated_state = await orchestrator.process_incident_pipeline(
        police_station=payload.police_station, 
        timestamp_str=payload.timestamp_str,
        env_factors=env_dict
    )
    if updated_state["execution_status"] == "FAILED":
        raise HTTPException(status_code=500, detail="Internal agent orchestration pipeline failure.")
    return {"status": "SUCCESS", "payload": updated_state}

@app.post("/api/v1/operations/batch-trigger")
async def trigger_batch_incidents(payloads: List[IncidentTrigger]):
    """Elite Feature: Ingests multiple distinct city incidents and processes them concurrently."""
    tasks = [
        orchestrator.process_incident_pipeline(p.police_station, p.timestamp_str, p.environmental_factors.dict())
        for p in payloads
    ]
    results = await asyncio.gather(*tasks)
    return {"status": "BATCH_SUCCESS", "processed_incidents_count": len(results), "payloads": results}

@app.get("/api/v1/flipkart/logistics-update")
def get_flipkart_supply_chain_feed():
    # Grabs the latest token state from orchestrator memory cleanly
    if not orchestrator.state_cache:
        return {"status": "IDLE", "message": "No active incidents tracked in memory cache."}
        
    latest_token = list(orchestrator.state_cache.keys())[-1]
    current_memory = orchestrator.state_cache[latest_token]
    intensity = current_memory.get("compounded_chaos_intensity", 1.0)
    
    sla_breach_probability = min(98.5, round(max(0.0, (intensity - 1.0) * 35.0), 1))
    estimated_freight_delay = int((intensity - 1.0) * 22) if intensity > 1.0 else 0
    
    routing_action = "PROCEED_ON_SCHEDULE"
    cost_impact = "NEGLIGIBLE"
    if intensity >= 1.8:
        routing_action = "CRITICAL_REROUTE_MANDATORY"
        cost_impact = "CRITICAL_SURGE"
    elif intensity > 1.2:
        routing_action = "DIVERGENT_ROUTING_RECOMMENDED"
        cost_impact = "MODERATE_ELEVATION"
        
    return {
        "monitored_hub_sector": current_memory.get("target_location", "None"),
        "compounded_congestion_index": intensity,
        "recommended_bypass_corridors": current_memory.get("recommended_diversion_corridors", []),
        "fleet_operational_action": routing_action,
        "sla_breach_probability_pct": f"{sla_breach_probability}%",
        "projected_freight_delay_mins": estimated_freight_delay,
        "supply_chain_cost_impact": cost_impact,
        "telemetry_timestamp": current_memory.get("timestamp", "None")
    }