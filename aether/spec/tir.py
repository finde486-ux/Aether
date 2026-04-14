import psutil
from typing import Dict, Any

class ResourceGuard:
    def __init__(self, ram_threshold_gb: float = 7.0):
        self.ram_threshold_bytes = ram_threshold_gb * (1024 ** 3)

    def get_system_tension(self) -> Dict[str, Any]:
        """Calculates current system tension based on resource usage."""
        mem = psutil.virtual_memory()

        # Tension is higher as RAM usage approaches the threshold
        tension_score = mem.used / self.ram_threshold_bytes
        is_critical = mem.used >= self.ram_threshold_bytes

        return {
            "ram_used_gb": round(mem.used / (1024 ** 3), 2),
            "ram_percent": mem.percent,
            "tension_score": round(tension_score, 2),
            "is_critical": is_critical,
            "action": "SCALE_DOWN" if is_critical else "OPTIMAL"
        }

    def get_suggested_context_window(self) -> int:
        """Suggests a context window size based on system tension (TIR logic)."""
        tension = self.get_system_tension()

        if tension["is_critical"]:
            return 2048  # Compressed window for 8GB RAM target
        elif tension["tension_score"] > 0.8:
            return 4096
        else:
            return 16384 # Default full context
