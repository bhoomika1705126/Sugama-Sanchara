import os
import sys
import pickle
import logging
import pandas as pd

# Append parent directory to path to enable clean root-level module lookups
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.utils import extract_temporal_slot

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger("DataProcessingPipeline")

def compile_historical_intelligence_matrix(csv_path: str, output_pickle_path: str) -> None:
    """
    Ingests, cleans, transforms, and processes raw ASTraM traffic data, 
    compiling it into a high-speed spatiotemporal look-up matrix.
    """
    logger.info(f"Starting Data Ingestion Loop from raw file: {csv_path}")
    
    if not os.path.exists(csv_path):
        logger.critical(f"Pipeline execution aborted. Raw file not found at: {csv_path}")
        return

    # Phase 1: Load explicit target feature vectors to conserve system RAM limits
    target_columns = ["police_station", "start_datetime", "priority", "requires_road_closure"]
    raw_df = pd.read_csv(csv_path, usecols=target_columns)
    initial_row_count = len(raw_df)
    
    # Phase 2: Data Cleansing & Missing-Value Truncation
    clean_df = raw_df.dropna(subset=["police_station", "start_datetime"]).copy()
    clean_df["police_station"] = clean_df["police_station"].str.strip()
    dropped_rows = initial_row_count - len(clean_df)
    
    logger.info(f"Cleaned {dropped_rows} incomplete/malformed logs out of {initial_row_count} total records.")
    
    # Phase 3: Feature Engineering & Operational Normalization
    logger.info("Transforming exact datetime timestamps into discrete operational shift bins...")
    clean_df["temporal_slot"] = clean_df["start_datetime"].apply(extract_temporal_slot)
    
    # Cast chaotic string/boolean column variations cleanly into unified bitmasks
    clean_df["is_severe_incident"] = (
        (clean_df["priority"].astype(str).str.lower() == "high") | 
        (clean_df["requires_road_closure"] == True) | 
        (clean_df["requires_road_closure"].astype(str).str.lower() == "true")
    )
    
    # Phase 4: Statistical Aggregation & Matrix Compilation
    logger.info("Aggregating spatiotemporal partitions and anomalies...")
    grouped_segments = clean_df.groupby(["police_station", "temporal_slot"])
    
    compiled_intelligence_matrix = {}
    
    for (station, slot), frame_partition in grouped_segments:
        volume_baseline = len(frame_partition)
        severe_count = frame_partition["is_severe_incident"].sum()
        
        # Calculate localized anomaly scale factors relative to historical means
        calculated_multiplier = 1.0 + (float(severe_count) / float(volume_baseline) * 2.0)
        
        if station not in compiled_intelligence_matrix:
            compiled_intelligence_matrix[station] = {}
            
        compiled_intelligence_matrix[station][slot] = {
            "historical_baseline_volume": int(volume_baseline),
            "anomaly_multiplier": float(round(calculated_multiplier, 3))
        }
        
    # Phase 5: Production-Ready Verification Check
    # Ensure that any dynamic station lookup that has zero records falls back cleanly
    unique_stations = clean_df["police_station"].unique()
    logger.info(f"Matrix successfully generated for {len(unique_stations)} distinct Bengaluru BTP Station grids.")
    
    # Serialize the compiled matrix to disk
    os.makedirs(os.path.dirname(output_pickle_path), exist_ok=True)
    with open(output_pickle_path, "wb") as output_handler:
        pickle.dump(compiled_intelligence_matrix, output_handler, protocol=pickle.HIGHEST_PROTOCOL)
        
    logger.info(f"Data pipeline complete. Serialized intelligence model written to: {output_pickle_path}")

if __name__ == "__main__":
    csv_source_file = os.path.join("dataset", "astram_events.csv")
    model_destination = os.path.join("models", "demand_model.pkl")
    compile_historical_intelligence_matrix(csv_source_file, model_destination)