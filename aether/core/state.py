from typing import Annotated, TypedDict, List, Dict, Any, Optional
import operator

def merge_list(left: List[Any], right: List[Any]) -> List[Any]:
    return left + right

class AetherState(TypedDict):
    # Core Intent
    intent: str

    # Temporal Context (Graphiti Nodes/Events)
    temporal_context: Annotated[List[Dict[str, Any]], merge_list]

    # The Adversarial Triad Reports
    alpha_proposal: Dict[str, Any]
    omega_report: Annotated[List[Dict[str, Any]], merge_list]
    sigma_trace: Annotated[List[Dict[str, Any]], merge_list]

    # System & Execution
    system_health: Dict[str, Any]
    last_output: Optional[str]

    # Logic Control
    iteration_count: int
    strategy_pivot: bool
    convergence_score: float
    shadow_mode: bool
    terminated: bool
