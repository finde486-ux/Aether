from langgraph.graph import StateGraph, END
from aether.core.state import AetherState
from aether.core.outcome import OutcomeEngine

async def alpha_node(state: AetherState):
    """Agent ALPHA: Proposes engineering/command changes."""
    print(f"--- ALPHA (Iteration {state['iteration_count']}) ---")
    return {
        "alpha_proposal": {"cmd": "ls -la", "goal": "System exploration"},
        "iteration_count": state["iteration_count"] + 1
    }

async def omega_node(state: AetherState):
    """Agent OMEGA: Performs adversarial audit on ALPHA's proposal."""
    print("--- OMEGA: Security Audit ---")
    proposal = state["alpha_proposal"]
    cmd = proposal.get("cmd", "")
    is_safe = "rm -rf" not in cmd and ";" not in cmd

    report = {
        "status": "SAFE" if is_safe else "BLOCKED",
        "risk_level": "LOW" if is_safe else "CRITICAL",
        "reasoning": "Standard system command" if is_safe else "Unsafe command pattern detected"
    }
    return {"adversarial_report": [report]}

async def sigma_node(state: AetherState):
    """Agent SIGMA: Observability and logic drift check."""
    print("--- SIGMA: Health Monitor ---")
    return {"system_health": {"status": "STABLE", "logic_drift": "NONE"}}

async def outcome_node(state: AetherState):
    """Outcome-Check Node: Evaluates convergence and determines next steps."""
    print("--- OUTCOME: Evaluating Convergence ---")
    score = OutcomeEngine.evaluate_convergence(state)
    pivot = OutcomeEngine.should_pivot(state)

    return {
        "convergence_score": score,
        "strategy_pivot": pivot
    }

async def execute_node(state: AetherState):
    """Final Execution Logic (using Shadow Mode if enabled)."""
    print("--- EXECUTE: Processing Authorized Commands ---")
    last_report = state["adversarial_report"][-1]

    if last_report["status"] != "SAFE":
        return {"last_execution_output": "Execution halted: OMEGA security block.", "terminated": True}

    cmd = state["alpha_proposal"].get("cmd")
    if state["shadow_mode"]:
        output = f"[SHADOW] Executed: {cmd}"
    else:
        output = f"[LIVE] Executed: {cmd}"

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
