from datetime import datetime, timezone
import uuid

class GraphitiMemory:
    def __init__(self): self.nodes = []
    async def record_event(self, event_type, data, status="SUCCESS"):
        node = {"id": str(uuid.uuid4()), "timestamp": datetime.now(timezone.utc).isoformat(), "event_type": event_type, "data": data, "status": status}
        self.nodes.append(node)
        return node
