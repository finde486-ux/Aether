import os
import json
import re
from typing import Dict, Any
from aether.config.models import ModelFactory

class AlphaAgent:
    def __init__(self, provider: str = None, model_name: str = None):
        try:
            self.model = ModelFactory.get_model(provider, model_name)
        except Exception as e:
            print(f"AlphaAgent Initialization Error: {e}")
            self.model = None

    async def propose(self, intent: str, context: list) -> Dict[str, Any]:
        """Alpha Generation: Provider-agnostic engineering proposals."""
        print(f"--- ALPHA: Generating proposal for intent -> {intent} ---")

        if not self.model:
            return {"cmd": "ls -la", "goal": "Fallback to exploration due to model unavailability"}

        prompt = f"""
        Act as Agent ALPHA (The Architect) for Project AETHER.
        User Intent: {intent}
        System Context: {context}

        Generate a specific terminal command to achieve this intent.
        Provide your response in raw JSON format (no markdown):
        {{
            "cmd": "the command",
            "goal": "your internal monologue / reasoning"
        }}
        """

        try:
            # LangChain consistent interface
            response = await self.model.ainvoke(prompt)
            content = response.content

            # Clean and parse JSON
            match = re.search(r'\{.*\}', content, re.DOTALL)
            if match:
                return json.loads(match.group())
        except Exception as e:
            print(f"Alpha AI Reasoning Error: {e}")

        return {"cmd": "ls -la", "goal": "Defaulting to safe exploration due to reasoning failure"}
