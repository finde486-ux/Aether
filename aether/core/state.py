from typing import Annotated, TypedDict, List, Dict, Any, Optional

def merge_reports(left: List[Dict[str, Any]], right: List[Dict[str, Any]]):
    return left + right

class AetherState(TypedDict):
    intent: str
    temporal_context: Annotated[List[Dict[str, Any]], merge_reports]
    adversarial_report: Annotated[List[Dict[str, Any]], merge_reports]
    system_health: Dict[str, Any]
    next_commands: List[str]
    last_execution_output: Optional[str]
    shadow_mode: bool
    iteration_count: int
    strategy_pivot: bool
    repair_proposals: List[Dict[str, Any]]
