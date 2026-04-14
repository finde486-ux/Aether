from langgraph.graph import StateGraph, END
from aether.core.state import AetherState
from aether.core.outcome import OutcomeEngine

async def alpha_node(state: AetherState):
    print(f"--- ALPHA: Generating Proposal (Iteration {state['iteration_count']}) ---")
    return {
        "alpha_proposal": {"cmd": "echo 'Hello AETHER'", "plan": "Initialize system"},
        "iteration_count": state["iteration_count"] + 1
    }

async def omega_node(state: AetherState):
    print("--- OMEGA: Adversarial Audit ---")
    # Simulate audit logic
    proposal = state["alpha_proposal"]
    is_safe = "rm -rf" not in proposal.get("cmd", "")
    return {
        "omega_report": [{"status": "SAFE" if is_safe else "VULNERABLE", "reasoning": "No dangerous patterns detected"}]
    }

async def sigma_node(state: AetherState):
    print("--- SIGMA: Observability Check ---")
    return {
        "sigma_trace": [{"event": "logic_check", "status": "ALIGNED"}]
    }

async def outcome_node(state: AetherState):
    print("--- OUTCOME: Evaluating Convergence ---")
    score = OutcomeEngine.evaluate_convergence(state)
    pivot = OutcomeEngine.should_pivot(state)

    updates = {
        "convergence_score": score,
        "strategy_pivot": pivot
    }

    if score >= 1.0:
        updates["terminated"] = True

    return updates

def route_next(state: AetherState):
    if state.get("terminated"):
        return "deploy"
    if state["iteration_count"] > 5:
        return END
    return "alpha"

workflow = StateGraph(AetherState)

workflow.add_node("alpha", alpha_node)
workflow.add_node("omega", omega_node)
workflow.add_node("sigma", sigma_node)
workflow.add_node("outcome", outcome_node)
# Implementation of deployment node will come in next step

workflow.set_entry_point("alpha")
workflow.add_edge("alpha", "omega")
workflow.add_edge("omega", "sigma")
workflow.add_edge("sigma", "outcome")

workflow.add_conditional_edges(
    "outcome",
    route_next,
    {
        "alpha": "alpha",
        "deploy": END, # Will point to deploy node later
        END: END
    }
)

app = workflow.compile()
