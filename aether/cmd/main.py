import asyncio
from rich.live import Live
from rich.panel import Panel

async def main():
    with Live(Panel("AETHER Autonomous Watchdog Active", title="AETHER"), screen=True):
        while True:
            await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(main())
