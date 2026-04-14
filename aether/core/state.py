from typing import Annotated, TypedDict, List, Dict, Any, Optional
import operator

def merge_reports(left: List[Dict[str, Any]], right: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return left + right

class AetherState(TypedDict):
    # Core Intent & Goals
    intent: str

    # Temporal Context (Graphiti Nodes/Knowledge)
    temporal_context: Annotated[List[Dict[str, Any]], merge_reports]

    # Adversarial Triad Data
    alpha_proposal: Dict[str, Any]
    adversarial_report: Annotated[List[Dict[str, Any]], merge_reports]  # Agent OMEGA Output
    system_health: Dict[str, Any]                                     # Agent SIGMA Output

    # System Status & Output
    last_execution_output: Optional[str]
    shadow_mode: bool

    # Orchestration Control
    iteration_count: int
    strategy_pivot: bool
    convergence_score: float
    terminated: bool
    awaiting_user: bool
