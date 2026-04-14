import os
from google import genai
from typing import Dict, Any

class AlphaAgent:
    def __init__(self):
        api_key = os.getenv("GOOGLE_API_KEY")
        if api_key:
            self.client = genai.Client(api_key=api_key)
            self.model_id = "gemini-2.0-flash"
        else:
            self.client = None

    async def propose(self, intent: str, context: list) -> Dict[str, Any]:
        """A. Alpha Generation: Uses Gemini 2.0 to generate engineering proposals."""
        print(f"--- ALPHA: Generating proposal for intent -> {intent} ---")

        if not self.client:
            return {"cmd": "echo 'AI not configured'", "goal": "Fallback"}

        prompt = f"""
        Act as Agent ALPHA (The Architect) for Project AETHER.
        User Intent: {intent}
        System Context: {context}

        Generate a specific terminal command to achieve this intent.
        Provide your response in JSON format:
        {{
            "cmd": "the command",
            "goal": "your internal monologue / reasoning"
        }}
        """

        try:
            response = self.client.models.generate_content(
                model=self.model_id,
                contents=prompt
            )

            import json
            import re
            match = re.search(r'\{.*\}', response.text, re.DOTALL)
            if match:
                return json.loads(match.group())
        except Exception as e:
            print(f"Alpha AI Error: {e}")

        return {"cmd": "ls -la", "goal": "Defaulting to safe exploration due to AI failure"}
