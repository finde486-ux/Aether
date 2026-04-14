from typing import Dict, Any, Optional
from aether.memory.graphiti_v2 import TemporalMemory

class SelfHealingCLI:
    def __init__(self, memory: TemporalMemory):
        self.memory = memory

    async def diagnose_failure(self, failed_command: str, error_message: str) -> Dict[str, Any]:
        """Intercepts a failed manual command and suggests a fix from Graphiti."""
        print(f"--- AETHER SELF-HEAL: Intercepted failure -> {failed_command} ---")

        # 1. Search Knowledge Graph for similar failures
        history = await self.memory.get_recent_history(limit=50)

        # Heuristic search: Look for successful repairs involving similar commands
        suggested_fix = None
        for node in reversed(history):
            if node["event_type"] == "EXECUTION_COMPLETE" and node["status"] == "SUCCESS":
                # If we found a success in the same context (e.g., repairing a file)
                if "config" in failed_command and "config" in node["data"]["cmd"]:
                    suggested_fix = node["data"]["cmd"]
                    break

        if suggested_fix:
            return {
                "diagnosis": "Previously encountered and repaired similar failure.",
                "suggested_repair": suggested_fix,
                "confidence": 0.85
            }

        return {
            "diagnosis": "New failure pattern. Initiating Alpha/Omega diagnostic loop...",
            "suggested_repair": "aether diagnose",
            "confidence": 0.3
        }
