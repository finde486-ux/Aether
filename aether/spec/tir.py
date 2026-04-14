import psutil

class ResourceGuard:
    def get_system_tension(self):
        # Tension-Based IR: Monitors RAM and scales model resources
        ram = psutil.virtual_memory().percent
        return {"ram_percent": ram, "critical": ram > 90}
