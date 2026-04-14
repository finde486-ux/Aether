import os
from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.panel import Panel

console = Console()

def run_setup():
    console.print(Panel("[bold cyan]Project AETHER: Neural-Native Agent Setup[/bold cyan]", title="Initialization"))

    console.print("\n[yellow]Welcome, Technician. Let's configure your AETHER core.[/yellow]")

    # 1. Provider Selection
    providers = ["google", "openai", "anthropic", "mistral", "ollama", "minimax", "nvidia", "glm"]
    provider = Prompt.ask("Select your AI Provider", choices=providers, default="google")

    # 2. API Key
    if provider != "ollama":
        api_key = Prompt.ask(f"Enter your [bold green]{provider.upper()}_API_KEY[/bold green]", password=True)
    else:
        api_key = "local-ollama"

    # 3. Model Name
    model_defaults = {
        "google": "gemini-2.0-flash",
        "openai": "gpt-4o",
        "anthropic": "claude-3-5-sonnet-20240620",
        "mistral": "mistral-large-latest",
        "ollama": "llama3.1",
        "minimax": "minimax-abab6.5-chat"
    }
    model_name = Prompt.ask("Specify Model Name", default=model_defaults.get(provider, "default"))

    # 4. Save to .env
    with open(".env", "w") as f:
        f.write(f"AETHER_PROVIDER={provider}\n")
        f.write(f"{provider.upper()}_API_KEY={api_key}\n")
        f.write(f"{provider.upper()}_MODEL={model_name}\n")

    console.print("\n[bold green]Success![/bold green] Configuration saved to [bold].env[/bold].")
    console.print("You can now run AETHER using: [bold]PYTHONPATH=. python3 aether/cmd/main.py[/bold]\n")

if __name__ == "__main__":
    run_setup()
