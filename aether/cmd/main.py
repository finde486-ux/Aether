import asyncio
from aether.core.graph import app

async def run_aether(intent: str):
    print(f"=== Starting AETHER Session: {intent} ===")
    initial_state = {
        "intent": intent,
        "temporal_context": [],
        "alpha_proposal": {},
        "omega_report": [],
        "sigma_trace": [],
        "system_health": {"status": "OK"},
        "last_output": None,
        "iteration_count": 0,
        "strategy_pivot": False,
        "convergence_score": 0.0,
        "shadow_mode": True,
        "terminated": False
    }

    config = {"configurable": {"thread_id": "aether_dev_v1"}}

    async for event in app.astream(initial_state, config):
        for node_name, output in event.items():
            print(f"Output from node '{node_name}': {output}")

if __name__ == "__main__":
    asyncio.run(run_aether("Initialize system diagnostics"))
