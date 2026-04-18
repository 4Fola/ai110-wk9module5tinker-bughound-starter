# WK09 Part 2–5: AI-assisted analysis with strict validation

from llm_client import GeminiClient


class AIAnalyzer:
    def __init__(self):
        self.client = GeminiClient()

    def analyze(self, code: str):
        prompt = (
            "Analyze the following Python code.\n"
            "Return a JSON list of detected issues.\n"
            "Do not include explanations.\n\n"
            f"{code}"
        )

        raw = self.client.generate(prompt)

        # NOTE:
        # Parsing is intentionally fragile.
        # BugHound relies on fallback logic when this fails.
        import json
        return json.loads(raw)
