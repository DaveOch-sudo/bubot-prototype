import os
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI
from openai.types.chat import ChatCompletionUserMessageParam

from .provider import LLMProvider

# Load the .env file from the project root.
PROJECT_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(PROJECT_ROOT / ".env")

class NVIDIAProvider(LLMProvider):

    def __init__(self):
        self.client = OpenAI(
            base_url="https://integrate.api.nvidia.com/v1",
            api_key=os.getenv("NVIDIA_API_KEY"),
            timeout=30.0,
            max_retries=0,
        )
        self.model = os.getenv("NVIDIA_MODEL")

    def generate(self, prompt: str) -> str:
        if not self.model:
            raise ValueError("NVIDIA_MODEL is not configured.")

        messages: list[ChatCompletionUserMessageParam] = [
            {
                "role": "user",
                "content": prompt,
            }
        ]

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.3,
            max_tokens=500,
        )

        return response.choices[0].message.content or ""