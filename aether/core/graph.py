from langgraph.graph import StateGraph, END
from aether.core.state import AetherState
from aether.core.outcome import OutcomeEngine
from aether.agents.omega.evaluator import OmegaEvaluator
from aether.agents.sigma.monitor import SigmaMonitor
from aether.agents.alpha.optimizer import AlphaOptimizer
from aether.memory.graphiti_v2 import TemporalMemory
from aether.transport.mcp_bridge import MCPBridge
from aether.memory.synthesis import MemorySynthesizer

from aether.agents.alpha.base import AlphaAgent

# Initialize shared resources
omega_eval = OmegaEvaluator()
alpha_agent = AlphaAgent()
alpha_opt = AlphaOptimizer()
temporal_mem = TemporalMemory()

class AetherBridge(MCPBridge):
    async def audit_command(self, command: str, context: dict) -> bool:
        report = await omega_eval.audit(command)
        return report["status"] == "SAFE"

mcp_bridge = AetherBridge(shadow_mode=True)

async def alpha_node(state: AetherState):
    """Agent ALPHA: Proposes engineering/command changes and system optimizations."""
    print(f"--- ALPHA (Iteration {state['iteration_count']}) ---")

    # Use LLM-driven Alpha if configured
    if alpha_agent.client:
        proposal = await alpha_agent.propose(state["intent"], state["temporal_context"])
        return {
            "alpha_proposal": proposal,
            "iteration_count": state["iteration_count"] + 1
        }

    if "Optimization" in state["intent"]:
        # Phase 5: Autonomous Optimization logic
        issues = await alpha_opt.scan_inefficiencies()
        current_issue = issues[0] # Propose fix for first inefficiency
        return {
            "alpha_proposal": {
                "cmd": current_issue["repair_cmd"],
                "goal": f"Optimization: {current_issue['target']}",
                "monologue": current_issue["monologue"],
                "is_batch": True
            },
            "iteration_count": state["iteration_count"] + 1
        }

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
    """Outcome-Check Node: Handles Batch Optimization and Multi-Sig pausing."""
    score = OutcomeEngine.evaluate_convergence(state)
    await temporal_mem.record_event("ITERATION_RESULT", {"proposal": state["alpha_proposal"], "score": score}, "SUCCESS" if score >= 1.0 else "FAILURE")

    # Phase 5: Multi-Sig pause for Batch Optimization
    if state["alpha_proposal"].get("is_batch") and score >= 1.0:
        print("--- AETHER: Batch Optimization Proposal generated. Awaiting Multi-Sig confirmation (Y/N) ---")
        # In a real system, this would wait for user input. We'll simulate a 'PAUSED' state.
        return {"convergence_score": score, "terminated": False, "awaiting_user": True}

    return {"convergence_score": score, "strategy_pivot": state["system_health"].get("trigger_pivot", False)}

async def execute_node(state: AetherState):
    """The 'Black-Box' Recorder: Finalize Forensic trace reporting."""
    print("--- EXECUTE: Invoking MCP Bridge ---")
    mcp_bridge.shadow_mode = state.get("shadow_mode", True)
    cmd = state["alpha_proposal"].get("cmd")

    # Execute with pre/post forensic snapshots
    result = await mcp_bridge.execute_command(cmd, {"state": "active"})

    # Generate trace_report.json (Trace Snapshot)
    trace_report = {
        "intent": state["intent"],
        "command": cmd,
        "internal_monologue": state["alpha_proposal"].get("goal"),
        "forensics": result.get("forensics"),
        "outcome": result["status"]
    }

    import json
    with open("trace_report.json", "w") as f:
        json.dump(trace_report, f, indent=2)

    await temporal_mem.record_event(
        "EXECUTION_COMPLETE",
        {"cmd": cmd, "result": result, "trace": trace_report},
        "SUCCESS" if result["status"] == "success" else "FAILURE"
    )
    return {"last_execution_output": result.get("output", result.get("message")), "terminated": True}

def should_continue(state: AetherState):
    if state.get("terminated"): return END
    if state.get("awaiting_user"): return END # Wait for manual signal
    if state["convergence_score"] >= 1.0: return "execute"
    if state["iteration_count"] > 10: return END
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
