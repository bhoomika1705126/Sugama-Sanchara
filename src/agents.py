import os
import json
import pickle
import logging
from typing import Dict, Any, List
from src.utils import extract_temporal_slot, get_adjacent_police_stations

logger = logging.getLogger("BTPMultiAgentSystem")

class BTPDataOraclePipeline:
    def __init__(self, model_path: str, config_path: str):
        self.model_path = model_path
        self.config_path = config_path
        self.intelligence_matrix: Dict[str, Any] = {}
        self.asset_configuration: Dict[str, Any] = {}
        
        self._synchronize_system_dependencies()

    def _synchronize_system_dependencies(self) -> None:
        """Loads static parameters and serialized matrices cleanly into memory."""
        try:
            if os.path.exists(self.model_path):
                with open(self.model_path, "rb") as model_handler:
                    self.intelligence_matrix = pickle.load(model_handler)
                logger.info("Successfully loaded pre-compiled lookup intelligence matrix into memory.")
            else:
                logger.warning(f"Target model file missing at {self.model_path}. Activating default safe mode.")

            if os.path.exists(self.config_path):
                with open(self.config_path, "r") as config_handler:
                    self.asset_configuration = json.load(config_handler)
                logger.info("Successfully synchronized local BTP asset configuration boundaries.")
            else:
                raise FileNotFoundError(f"Critical configuration assets map missing at: {self.config_path}")
        except Exception as error:
            logger.critical(f"Fatal initialization error in Multi-Agent Core Engine: {error}")
            raise error

    def intelligence_agent_node(self, police_station: str, timestamp_str: str) -> Dict[str, Any]:
        """
        Agent Node 1: Quantifies spatiotemporal incident congestion anomaly factors
        without relying on external web layers or third-party dependencies.
        """
        binned_slot = extract_temporal_slot(timestamp_str)
        
        station_profile = self.intelligence_matrix.get(police_station, {})
        metrics_payload = station_profile.get(binned_slot, {"historical_baseline_volume": 5, "anomaly_multiplier": 1.0})
        
        anomaly_intensity = metrics_payload["anomaly_multiplier"]
        logger.info(f"[Intel Node] Resolved sector tracking for {police_station} at shift {binned_slot}. Anomaly: {anomaly_intensity}x")
        
        return {
            "target_location": police_station,
            "anomaly_intensity": float(anomaly_intensity)
        }

    def strategy_agent_node(self, police_station: str, anomaly_intensity: float) -> Dict[str, Any]:
        """
        Agent Node 2: Evaluates adjacent sectors and filters out over-saturated grids 
        to return compliant, un-blocked diversion routes.
        """
        raw_detour_options = get_adjacent_police_stations(police_station)
        validated_bypass_corridors: List[str] = []
        
        for neighbor_grid in raw_detour_options:
            neighbor_profile = self.intelligence_matrix.get(neighbor_grid, {})
            # Look up shift 2 (mid-day proxy) to evaluate base grid pressure conditions
            neighbor_pressure = neighbor_profile.get(2, {}).get("anomaly_multiplier", 1.0)
            
            # Defensive validation: Only reroute through adjacent zones with stable traffic conditions
            if neighbor_pressure < 1.75:
                validated_bypass_corridors.append(neighbor_grid)
                
        if not validated_bypass_corridors:
            # Safe defensive fallback logic to prevent execution graph failure
            validated_bypass_corridors = [raw_detour_options[0]] if raw_detour_options else ["Wilson Garden"]

        logger.info(f"[Strategy Node] Formulated alternative routing paths bypassing {police_station}: {validated_bypass_corridors}")
        return {
            "origin_location": police_station,
            "recommended_diversion_corridors": validated_bypass_corridors
        }

    def logistics_agent_node(self, police_station: str, anomaly_intensity: float) -> Dict[str, Any]:
        """
        Agent Node 3: Validates local station inventory and scales asset distribution requirements
        under strict mathematical capacity limits.
        """
        global_constraints = self.asset_configuration.get("global_limits", {})
        regional_pools = self.asset_configuration.get("regional_inventory", {})
        
        station_inventory = regional_pools.get(police_station, regional_pools.get("default"))
        
        # Scale hardware deployments dynamically based on target structural anomaly weights
        target_personnel = min(int(2 * anomaly_intensity), global_constraints.get("max_personnel_per_incident", 8))
        target_barricades = min(int(4 * anomaly_intensity), global_constraints.get("max_barricades_per_incident", 15))
        
        # Hard Physical Constraint Validation Engine
        if target_personnel > station_inventory["personnel"]:
            target_personnel = station_inventory["personnel"]
            logger.warning(f"[Logistics Node] Personnel cap reached for regional asset station: {police_station}")
            
        if target_barricades > station_inventory["barricades"]:
            target_barricades = station_inventory["barricades"]
            
        logger.info(f"[Logistics Node] Dispatched physical infrastructure assets. Officers: {target_personnel}, Barricades: {target_barricades}")
        return {
            "allocated_personnel": int(target_personnel),
            "allocated_barricades": int(target_barricades)
        }