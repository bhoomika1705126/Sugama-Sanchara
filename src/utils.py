import logging
from typing import List

# Configure isolated, production-grade logging format
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger("GridlockUtils")

def extract_temporal_slot(datetime_str: str) -> int:
    """
    Parses an ISO/ASTraM timestamp string and groups it into an operational shift block.
    Shifts: 0 (00:00-04:00), 1 (04:00-08:00), 2 (08:00-12:00), 
            3 (12:00-16:00), 4 (16:00-20:00), 5 (20:00-24:00)
    """
    try:
        # String slice split to maximize execution speed without parser overhead
        time_segment = str(datetime_str).split(" ")[1]
        hour_integer = int(time_segment.split(":")[0])
        return hour_integer // 4
    except (IndexError, ValueError) as err:
        logger.debug(f"Failed parsing raw time signature: '{datetime_str}'. Falling back to default block. Details: {err}")
        return 2

def get_adjacent_police_stations(station_name: str) -> List[str]:
    """
    Simulates a localized geospatial adjacency network mapping out detour grid vectors
    controlled by neighboring Bengaluru Traffic Police (BTP) stations.
    """
    adjacency_graph = {
        "Peenya": ["Sadashivanagar", "Wilson Garden"],
        "HSR Layout": ["Wilson Garden", "Jayanagara"],
        "Wilson Garden": ["HSR Layout", "Jayanagara", "Sadashivanagar"],
        "Sadashivanagar": ["Peenya", "Wilson Garden"],
        "Jayanagara": ["Wilson Garden", "HSR Layout"]
    }
    return adjacency_graph.get(station_name, ["Wilson Garden", "HSR Layout"])