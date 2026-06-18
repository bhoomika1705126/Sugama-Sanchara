import asyncio
from src.orchestrator import GridlockOrchestrator

async def test_advanced_system():
    engine = GridlockOrchestrator()
    
    station = "Majestic"
    time = "18:45"
    chaos_triggers = {
        "is_raining": True, 
        "active_waterlogging": True, 
        "vip_movement": False
    }
    
    print("=== ASYNC ARCHITECTURE INTEGRATION TEST ===")
    state = await engine.process_incident_pipeline(station, time, env_factors=chaos_triggers)
    
    print("\n=== NETWORK RIPPLE ENGINE PROPAGATION ===")
    for sector, pressure in state['network_ripple_impact'].items():
        print(f" -> Corridor Sector [{sector}]: Calculated Rippled Pressure -> {pressure}x")
        
    print("\n⚡ GENERATIVE TACTICAL DISPATCH BRIEFING:")
    print(state['tactical_briefing'])
    print("====================================================")

if __name__ == "__main__":
    asyncio.run(test_advanced_system())