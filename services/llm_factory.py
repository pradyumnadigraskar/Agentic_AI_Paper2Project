from google import genai
import subprocess
import os

class LLMProvider:
    def __init__(self, provider="ollama"):
        self.provider = provider
        if provider == "gemini":
            print("LOG: Initializing Gemini Client...")
            self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
            self.model_id = "gemini-2.0-flash"

    def generate(self, prompt: str) -> str:
        if self.provider == "gemini":
            try:
                print(f"LOG: Sending request to Gemini...")
                response = self.client.models.generate_content(model=self.model_id, contents=prompt)
                return response.text
            except Exception as e:
                return f"Gemini Error: {str(e)}"
        else:
            try:
                print(f"LOG: Calling Local Ollama ({os.getenv('OLLAMA_MODEL')})...")
                result = subprocess.run(
                    ["ollama", "run", os.getenv("OLLAMA_MODEL", "mistral")],
                    input=prompt, text=True, capture_output=True, encoding="utf-8"
                )
                return result.stdout.strip()
            except Exception as e:
                return f"Ollama Error: {str(e)}"