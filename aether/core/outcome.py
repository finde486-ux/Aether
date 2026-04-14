from typing import Dict, Any
from aether.core.state import AetherState

class OutcomeEngine:
    @staticmethod
    def evaluate_convergence(state: AetherState) -> float:
        """Evaluates how close the current state is to the user intent."""
        if not state.get("adversarial_report"):
            return 0.0

        last_audit = state["adversarial_report"][-1]

        # Simulation logic: cat usually isn't enough to "repair"
        cmd = state["alpha_proposal"].get("cmd", "")
        if "fixed" in cmd or "bak" in cmd or "purge" in cmd or "upgrade" in cmd or "kill" in cmd:
            return 1.0

        if last_audit.get("status") == "SAFE":
            return 0.5 # Partial convergence
        return 0.0

    @staticmethod
    def should_pivot(state: AetherState) -> bool:
        """Determines if a strategic shift is needed to avoid infinite loops."""
        return state["iteration_count"] >= 3 and state["convergence_score"] < 0.8

    @staticmethod
    def prune_state(state: AetherState) -> Dict[str, Any]:
        """TIR Sparse Activation: Prunes non-essential state nodes."""
        if len(state["temporal_context"]) > 10:
             return {"temporal_context": state["temporal_context"][-10:]}
        return {}
