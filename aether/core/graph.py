from langgraph.graph import StateGraph, END
from aether.core.state import AetherState
from aether.core.outcome import OutcomeEngine
from aether.agents.omega.evaluator import OmegaEvaluator
from aether.agents.sigma.monitor import SigmaMonitor
from aether.memory.graphiti_v2 import TemporalMemory
from aether.transport.mcp_bridge import MCPBridge
from aether.memory.synthesis import MemorySynthesizer

# Initialize shared resources
omega_eval = OmegaEvaluator()
temporal_mem = TemporalMemory()

class AetherBridge(MCPBridge):
    async def audit_command(self, command: str, context: dict) -> bool:
        report = await omega_eval.audit(command)
        return report["status"] == "SAFE"

mcp_bridge = AetherBridge(shadow_mode=True)

async def alpha_node(state: AetherState):
    print(f"--- ALPHA (Iteration {state['iteration_count']}) ---")
    cmd = "cat config_corrupted.conf" if not state.get("strategy_pivot") else "cp config_fixed.bak config_corrupted.conf"
    return {
        "alpha_proposal": {"cmd": cmd, "goal": "Repair config"},
        "iteration_count": state["iteration_count"] + 1
    }

async def omega_node(state: AetherState):
    proposal = state["alpha_proposal"]
    audit_result = await omega_eval.audit(proposal.get("cmd", ""))
    return {"adversarial_report": [audit_result]}

async def sigma_node(state: AetherState):
    drift_report = await SigmaMonitor.check_drift(state["intent"], state["alpha_proposal"], state["iteration_count"])
    return {"system_health": drift_report}

async def vision_node(state: AetherState):
    """I. Visual Diagnosis Node: Triggered on persistent failure."""
    if state["iteration_count"] > 2 and state["convergence_score"] < 0.6:
        monitor = SigmaMonitor()
        diagnosis = await monitor.vision_check(state["intent"])
        return {"temporal_context": [{"event_type": "VISION_DIAGNOSIS", "data": {"result": diagnosis}, "status": "SUCCESS"}]}
    return {}

async def condense_node(state: AetherState):
    """B. State Condenser Node."""
    if state["iteration_count"] % 5 == 0 and state["iteration_count"] > 0:
        return await MemorySynthesizer.condense(state)
    return {}

async def outcome_node(state: AetherState):
    score = OutcomeEngine.evaluate_convergence(state)
    await temporal_mem.record_event("ITERATION_RESULT", {"proposal": state["alpha_proposal"], "score": score}, "SUCCESS" if score >= 1.0 else "FAILURE")
    return {"convergence_score": score, "strategy_pivot": state["system_health"].get("trigger_pivot", False)}

async def execute_node(state: AetherState):
    print("--- EXECUTE: Invoking MCP Bridge ---")
    mcp_bridge.shadow_mode = state.get("shadow_mode", True)
    cmd = state["alpha_proposal"].get("cmd")
    result = await mcp_bridge.execute_command(cmd, {"state": "active"})
    await temporal_mem.record_event("EXECUTION_COMPLETE", {"cmd": cmd, "result": result}, "SUCCESS" if result["status"] == "success" else "FAILURE")
    return {"last_execution_output": result.get("output", result.get("message")), "terminated": True}

def should_continue(state: AetherState):
    if state.get("terminated"): return END
    if state["convergence_score"] >= 1.0: return "execute"
    if state["iteration_count"] > 10: return END # Increased for condenser test
    return "alpha"

workflow = StateGraph(AetherState)
workflow.add_node("alpha", alpha_node)
workflow.add_node("omega", omega_node)
workflow.add_node("sigma", sigma_node)
workflow.add_node("vision", vision_node)
workflow.add_node("condense", condense_node)
workflow.add_node("outcome", outcome_node)
workflow.add_node("execute", execute_node)

workflow.set_entry_point("alpha")
workflow.add_edge("alpha", "omega")
workflow.add_edge("omega", "sigma")
workflow.add_edge("sigma", "vision")
workflow.add_edge("vision", "condense")
workflow.add_edge("condense", "outcome")

workflow.add_conditional_edges("outcome", should_continue, {"alpha": "alpha", "execute": "execute", END: END})
workflow.add_edge("execute", END)
app = workflow.compile()
