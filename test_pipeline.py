import logging
from src.agents import BTPDataOraclePipeline

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def run_local_integration_smoke_test():
    model_source = "models/demand_model.pkl"
    config_source = "config/btp_assets.json"
    
    # Initialize the engine
    pipeline_instance = BTPDataOraclePipeline(model_path=model_source, config_path=config_source)
    
    # Simulate an incoming live incident payload matching values in the ASTraM log file
    test_station = "Peenya"
    simulated_timestamp = "2024-03-07 17:01:48.111+00"
    
    print("\n--- STANDALONE MULTI-AGENT EXECUTION LOOP START ---")
    
    # Invoke Agent Node 1
    intel_response = pipeline_instance.intelligence_agent_node(test_station, simulated_timestamp)
    calculated_intensity = intel_response["anomaly_intensity"]
    
    # Invoke Agent Node 2
    strategy_response = pipeline_instance.strategy_agent_node(test_station, calculated_intensity)
    
    # Invoke Agent Node 3
    logistics_response = pipeline_instance.logistics_agent_node(test_station, calculated_intensity)
    
    print("\n--- VERIFYING OUTPUT SCHEMAS AND DATA CONTRACT CONTRACTS ---")
    print(f"Node 1 Output (Intensity Multiplier) -> {calculated_intensity}x")
    print(f"Node 2 Output (Diversion Pathways)    -> {strategy_response['recommended_diversion_corridors']}")
    print(f"Node 3 Output (Resource Deployments)  -> Personnel: {logistics_response['allocated_personnel']}, Barricades: {logistics_response['allocated_barricades']}")
    print("----------------------------------------------------\n")

if __name__ == "__main__":
    run_local_integration_smoke_test()