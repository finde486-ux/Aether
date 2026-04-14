import asyncio
from rich.live import Live
from rich.layout import Layout
from rich.panel import Panel
from rich.table import Table
from rich.console import Console
from datetime import datetime
from aether.core.graph import app, temporal_mem
from aether.spec.tir import ResourceGuard

console = Console()
resource_guard = ResourceGuard()

def create_dashboard(active_node: str, events: list, tension: dict) -> Layout:
    layout = Layout()
    layout.split_column(
        Layout(name="header", size=3),
        Layout(name="main"),
        Layout(name="footer", size=3)
    )
    layout["main"].split_row(
        Layout(name="nervous_system", ratio=1),
        Layout(name="graphiti_log", ratio=2)
    )

    layout["header"].update(Panel(f"AETHER Autonomous Watchdog | Active Node: [bold green]{active_node}[/bold green]", title="System Control"))

    color = "red" if tension["is_critical"] else "yellow" if tension["tension_score"] > 0.8 else "green"
    layout["footer"].update(Panel(f"System Tension: [{color}]{tension['tension_score']}[/{color}] | RAM: {tension['ram_used_gb']}GB ({tension['ram_percent']}%)", title="TIR Resource Guard"))

    triad_table = Table(title="Adversarial Triad")
    triad_table.add_column("Agent", style="cyan")
    triad_table.add_column("Status", style="magenta")
    triad_table.add_row("ALPHA (Architect)", "WAITING" if active_node != "alpha" else "[bold green]ACTIVE[/bold green]")
    triad_table.add_row("OMEGA (Adversary)", "WAITING" if active_node != "omega" else "[bold red]ACTIVE[/bold red]")
    triad_table.add_row("SIGMA (Observer)", "WAITING" if active_node != "sigma" else "[bold blue]ACTIVE[/bold blue]")
    layout["nervous_system"].update(Panel(triad_table, title="Nervous System"))

    event_table = Table(title="Graphiti Temporal Log", expand=True)
    event_table.add_column("Time", width=12)
    event_table.add_column("Type", style="bold")
    event_table.add_column("Status")

    for event in reversed(events[-10:]):
        time_str = event["timestamp"].split("T")[1][:8]
        status_color = "green" if event["status"] == "SUCCESS" else "red"
        event_table.add_row(time_str, event["event_type"], f"[{status_color}]{event['status']}[/{status_color}]")

    layout["graphiti_log"].update(Panel(event_table, title="Knowledge Graph"))
    return layout

async def run_dashboard():
    active_node = "BOOTING"
    intent = "Autonomous System Maintenance"

    state = {
        "intent": intent, "temporal_context": [], "alpha_proposal": {}, "adversarial_report": [],
        "system_health": {"status": "OK"}, "last_execution_output": None, "iteration_count": 0,
        "strategy_pivot": False, "convergence_score": 0.0, "shadow_mode": True, "terminated": False
    }

    config = {"configurable": {"thread_id": "aether_prod_v1"}}

    with Live(refresh_per_second=4, screen=True) as live:
        # Initial cold boot pre-fetch simulation
        await asyncio.sleep(1)
        active_node = "INITIALIZING"

        async for event in app.astream(state, config):
            for node_name, output in event.items():
                active_node = node_name
                # Refresh events from temporal memory dynamically
                events = await temporal_mem.get_recent_history(limit=15)
                tension = resource_guard.get_system_tension()
                live.update(create_dashboard(active_node, events, tension))
            await asyncio.sleep(0.2) # Throttled UI update

        active_node = "STANDBY"
        while True: # Keep dashboard alive in standby mode
            events = await temporal_mem.get_recent_history(limit=15)
            tension = resource_guard.get_system_tension()
            live.update(create_dashboard(active_node, events, tension))
            await asyncio.sleep(2)

if __name__ == "__main__":
    asyncio.run(run_dashboard())
