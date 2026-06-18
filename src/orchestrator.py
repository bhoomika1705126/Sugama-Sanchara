import os
import asyncio
import logging
from src.agents import BTPDataOraclePipeline

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("GridlockOrchestrator")

class GridlockOrchestrator:
    def __init__(self):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        model_path = os.path.join(base_dir, "models", "demand_model.pkl")
        config_path = os.path.join(base_dir, "config", "btp_assets.json")
        
        self.pipeline = BTPDataOraclePipeline(model_path=model_path, config_path=config_path)
        self.state_cache = {}

    async def process_incident_pipeline(self, police_station: str, timestamp_str: str, env_factors: dict = None) -> dict:
        """Runs the entire multi-agent cycle asynchronously with ripple modeling and text synthesis."""
        if env_factors is None:
            env_factors = {"is_raining": False, "active_waterlogging": False, "vip_movement": False}

        # Initialize isolated token state for concurrency safety
        token = f"{police_station}_{timestamp_str}"
        self.state_cache[token] = {
            "target_location": police_station,
            "timestamp": timestamp_str,
            "base_anomaly_intensity": 1.0,
            "compounded_chaos_intensity": 1.0,
            "recommended_diversion_corridors": [],
            "network_ripple_impact": {},
            "allocated_personnel": 0,
            "allocated_barricades": 0,
            "logistics_directives": [],
            "tactical_briefing": "",
            "execution_status": "PROCESSING"
        }

        try:
            # Node 1: Intelligence Processing (Simulating minor async I/O gap)
            await asyncio.sleep(0.01)
            intel_output = self.pipeline.intelligence_agent_node(police_station, timestamp_str)
            base_intensity = intel_output.get("anomaly_intensity", 1.0)
            self.state_cache[token]["base_anomaly_intensity"] = base_intensity
            
            # Apply Chaos Factors
            chaos_multiplier = 1.0
            if env_factors.get("is_raining"): chaos_multiplier += 0.3
            if env_factors.get("active_waterlogging"): chaos_multiplier += 0.4
            if env_factors.get("vip_movement"): chaos_multiplier += 0.6
            
            compounded_intensity = round(base_intensity * chaos_multiplier, 2)
            self.state_cache[token]["compounded_chaos_intensity"] = compounded_intensity

            # Node 2: Strategy Processing with Network Ripple Modeling
            strategy_output = self.pipeline.strategy_agent_node(police_station, compounded_intensity)
            raw_diversions = strategy_output.get("recommended_diversion_corridors", [])
            
            # Execute Ripple Propagation Calculation
            validated_diversions = []
            ripple_map = {}
            for neighbor in raw_diversions:
                neighbor_profile = self.pipeline.intelligence_matrix.get(neighbor, {})
                base_neighbor_pressure = neighbor_profile.get(2, {}).get("anomaly_multiplier", 1.0)
                
                # Apply cascading spillover weight from primary incident
                rippled_pressure = round(base_neighbor_pressure + (compounded_intensity - 1.0) * 0.3, 2)
                ripple_map[neighbor] = rippled_pressure
                
                if rippled_pressure < 2.0:
                    validated_diversions.append(neighbor)
                    
            if not validated_diversions:
                validated_diversions = [raw_diversions[0]] if raw_diversions else ["Wilson Garden"]

            self.state_cache[token]["recommended_diversion_corridors"] = validated_diversions
            self.state_cache[token]["network_ripple_impact"] = ripple_map

            # Node 3: Logistics Processing
            logistics_output = self.pipeline.logistics_agent_node(police_station, compounded_intensity)
            self.state_cache[token]["allocated_personnel"] = logistics_output.get("allocated_personnel", 0)
            self.state_cache[token]["allocated_barricades"] = logistics_output.get("allocated_barricades", 0)
            
            # Cross-Station Resource Borrowing Loop
            await self._execute_logistics_healing(token, police_station, compounded_intensity, validated_diversions)
            
            # Synthesis Node: Generate Human Readable Tactical Text
            self.state_cache[token]["tactical_briefing"] = self._generate_tactical_briefing(self.state_cache[token])
            self.state_cache[token]["execution_status"] = "SUCCESS"
            
        except Exception as error:
            self.state_cache[token]["execution_status"] = "FAILED"
            logger.error(f"Async engine boundary failure: {str(error)}")
            
        return self.state_cache[token]

    async def _execute_logistics_healing(self, token: str, station: str, intensity: float, neighbors: list):
        """Autonomously reallocates hardware pools from neighbor grids during sharp deficits."""
        ideal_personnel = min(int(2 * intensity), 8)
        ideal_barricades = min(int(4 * intensity), 15)
        
        deficit_personnel = ideal_personnel - self.state_cache[token]["allocated_personnel"]
        deficit_barricades = ideal_barricades - self.state_cache[token]["allocated_barricades"]
        
        if deficit_personnel <= 0 and deficit_barricades <= 0:
            self.state_cache[token]["logistics_directives"].append(f"Local deployment at {station} fulfills safety quotas.")
            return

        regional_inventory = self.pipeline.asset_configuration.get("regional_inventory", {})
        
        for helper in neighbors:
            if helper not in regional_inventory:
                continue
            helper_stock = regional_inventory[helper]
            
            if deficit_personnel > 0 and helper_stock["personnel"] > 3:
                shared_officers = min(deficit_personnel, helper_stock["personnel"] - 3)
                if shared_officers > 0:
                    self.state_cache[token]["allocated_personnel"] += shared_officers
                    deficit_personnel -= shared_officers
                    self.state_cache[token]["logistics_directives"].append(f"Reallocate {shared_officers} officers from {helper} to {station}.")
                    
            if deficit_barricades > 0 and helper_stock["barricades"] > 5:
                shared_barricades = min(deficit_barricades, helper_stock["barricades"] - 5)
                if shared_barricades > 0:
                    self.state_cache[token]["allocated_barricades"] += shared_barricades
                    deficit_barricades -= shared_barricades
                    self.state_cache[token]["logistics_directives"].append(f"Deploy {shared_barricades} physical barriers from {helper} reserves to {station} corridors.")
                    
            if deficit_personnel <= 0 and deficit_barricades <= 0:
                break

    def _generate_tactical_briefing(self, data: dict) -> str:
        """Synthesizes systemic metrics into structured command text for operators."""
        station = data["target_location"]
        intensity = data["compounded_chaos_intensity"]
        diversions = ", ".join(data["recommended_diversion_corridors"])
        
        severity = "MINOR" if intensity < 1.3 else "MODERATE" if intensity < 1.7 else "CRITICAL"
        
        brief = f"STATUS REPORT [{severity}]: {station} sector is experiencing a {intensity}x traffic anomaly profile. "
        brief += f"Initiating structured perimeter adjustments. Traffic flow is actively being diverted along the following verified bypass pathways: [{diversions}]. "
        brief += f"Operational metrics confirm a total deployment of {data['allocated_personnel']} officers along with {data['allocated_barricades']} structural field barricades. "
        
        if len(data["logistics_directives"]) > 1 or "Reallocate" in "".join(data["logistics_directives"]):
            brief += "NOTICE: Inter-station emergency asset borrowing protocols have been activated to address capacity limits."
        else:
            brief += "Resource levels within the primary grid boundary remain sufficient."
            
        return brief