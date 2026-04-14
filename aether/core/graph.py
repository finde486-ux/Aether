from langgraph.graph import StateGraph, END
from aether.core.state import AetherState
from aether.core.outcome import OutcomeEngine
from aether.agents.omega.evaluator import OmegaEvaluator
from aether.agents.sigma.monitor import SigmaMonitor
from aether.memory.graphiti_v2 import TemporalMemory
from aether.transport.mcp_bridge import MCPBridge

# Initialize concrete bridge for the graph
class AetherBridge(MCPBridge):
    async def audit_command(self, command: str, context: dict) -> bool:
        evaluator = OmegaEvaluator()
        report = await evaluator.audit(command)
        return report["status"] == "SAFE"

# Initialize shared resources
omega_eval = OmegaEvaluator()
temporal_mem = TemporalMemory()
mcp_bridge = AetherBridge(shadow_mode=True) # Default to Shadow for safety

async def alpha_node(state: AetherState):
    """Agent ALPHA: Proposes engineering/command changes."""
    print(f"--- ALPHA (Iteration {state['iteration_count']}) ---")

    if state.get("strategy_pivot"):
         # Use full path to avoid ambiguity during repair
         cmd = "cp config_fixed.bak config_corrupted.conf"
    else:
         cmd = "cat config_corrupted.conf"

    return {
        "alpha_proposal": {"cmd": cmd, "goal": "Repair corrupted config"},
        "iteration_count": state["iteration_count"] + 1
    }

async def omega_node(state: AetherState):
    """Agent OMEGA: Performs hacker-logic adversarial audit."""
    proposal = state["alpha_proposal"]
    audit_result = await omega_eval.audit(proposal.get("cmd", ""))
    return {"adversarial_report": [audit_result]}

async def sigma_node(state: AetherState):
    """Agent SIGMA: Observability and logic drift check."""
    drift_report = await SigmaMonitor.check_drift(
        state["intent"],
        state["alpha_proposal"],
        state["iteration_count"]
    )
    return {"system_health": drift_report}

async def outcome_node(state: AetherState):
    """Outcome-Check Node: Evaluates convergence and records events."""
    score = OutcomeEngine.evaluate_convergence(state)

    await temporal_mem.record_event(
        event_type="ITERATION_RESULT",
        data={
            "iteration": state["iteration_count"],
            "proposal": state["alpha_proposal"],
            "score": score
        },
        status="SUCCESS" if score >= 1.0 else "FAILURE"
    )

    pivot = state["system_health"].get("trigger_pivot", False)

    return {
        "convergence_score": score,
        "strategy_pivot": pivot
    }

async def execute_node(state: AetherState):
    """Final Execution Logic using the MCP Bridge."""
    print("--- EXECUTE: Invoking MCP Bridge ---")

    # Update bridge mode based on state
    mcp_bridge.shadow_mode = state.get("shadow_mode", True)

    cmd = state["alpha_proposal"].get("cmd")
    result = await mcp_bridge.execute_command(cmd, {"state": "active"})

    output = result.get("output", result.get("message", "Unknown execution error"))

    await temporal_mem.record_event(
        "EXECUTION_COMPLETE",
        {"cmd": cmd, "result": result},
        "SUCCESS" if result["status"] == "success" else "FAILURE"
    )

    return {"last_execution_output": output, "terminated": True}

def should_continue(state: AetherState):
    if state.get("terminated"):
        return END
    if state["convergence_score"] >= 1.0:
        return "execute"
    if state["iteration_count"] > 5:
        return END
    return "alpha"

# Define Graph
workflow = StateGraph(AetherState)

workflow.add_node("alpha", alpha_node)
workflow.add_node("omega", omega_node)
workflow.add_node("sigma", sigma_node)
workflow.add_node("outcome", outcome_node)
workflow.add_node("execute", execute_node)

workflow.set_entry_point("alpha")
workflow.add_edge("alpha", "omega")
workflow.add_edge("omega", "sigma")
workflow.add_edge("sigma", "outcome")

workflow.add_conditional_edges(
    "outcome",
    should_continue,
    {
        "alpha": "alpha",
        "execute": "execute",
        END: END
    }
)
workflow.add_edge("execute", END)

app = workflow.compile()
