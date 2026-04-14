import uuid
from datetime import datetime, timezone
from typing import Dict, Any, List

class TemporalMemory:
    def __init__(self):
        # In-memory mock for Graphiti Knowledge Graph
        self.nodes = []

    async def record_event(self, event_type: str, data: Dict[str, Any], status: str = "SUCCESS"):
        """Records a system event into the temporal graph."""
        timestamp = datetime.now(timezone.utc).isoformat()
        node_id = str(uuid.uuid4())

        node = {
            "id": node_id,
            "timestamp": timestamp,
            "event_type": event_type,
            "data": data,
            "status": status
        }

        print(f"--- GRAPHITI: Recording Node [{event_type}] @ {timestamp} ---")
        self.nodes.append(node)
        return node_id

    async def get_recent_history(self, limit: int = 5) -> List[Dict[str, Any]]:
        return self.nodes[-limit:]

    async def perform_delta_analysis(self, current_state: Dict[str, Any]) -> Dict[str, Any]:
        """Identifies what changed in the system since the last success."""
        if not self.nodes:
            return {"delta": "INITIAL_STATE"}

        last_success = next((n for n in reversed(self.nodes) if n["status"] == "SUCCESS"), None)
        if not last_success:
            return {"delta": "NO_PREVIOUS_SUCCESS"}

        return {
            "last_success_id": last_success["id"],
            "delta": f"Changes since {last_success['timestamp']}"
        }
