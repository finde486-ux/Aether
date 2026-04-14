from typing import Dict, Any, List

class SigmaMonitor:
    @staticmethod
    async def check_drift(intent: str, proposal: Dict[str, Any], iteration: int) -> Dict[str, Any]:
        """Flags 'Internal Logic Drift' if iterations spike without success."""
        print(f"--- SIGMA: Monitoring Logic Drift (Iteration {iteration}) ---")

        drift_detected = iteration > 3

        return {
            "status": "STABLE" if not drift_detected else "DRIFT_DETECTED",
            "logic_drift": "NONE" if not drift_detected else "ITERATION_SPIKE",
            "trigger_pivot": drift_detected,
            "metrics": {
                "iteration_depth": iteration,
                "alignment_score": 0.9 if not drift_detected else 0.4
            }
        }
