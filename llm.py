import os
from google import genai
from google.genai import types
from typing import List, Dict, Any
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


class GeminiLLMClient:
    def __init__(self, model_name: str = os.getenv("MODEL_NAME")):
        self.model = model_name

    def call(
        self,
        messages: List[Dict[str, str]],
        tools: List[Dict[str, Any]] | None = None,
    ):
        contents = self._convert_messages(messages)
        config = None
        if tools:
            config = types.GenerateContentConfig(tools=tools)

        response = client.models.generate_content(
            contents=contents,
            model=self.model,
            config=config
        )
        
        return response

    @staticmethod
    def _convert_messages(messages):
        contents = []

        for msg in messages:
            if msg["role"] == "assistant":
                role = "model"
            else:
                role = "user"

            contents.append(
                {
                    "role": role,
                    "parts": [{"text": msg["content"]}],
                }
            )
        return contents
    
    @staticmethod
    def _parse_gemini_response(response):
        candidate = response.candidates[0]
        parts = candidate.content.parts

        for part in parts:
            if hasattr(part, "function_call") and part.function_call:
                return {
                    "type": "tool_call",
                    "name": part.function_call.name,
                    "args": dict(part.function_call.args),
                }

            if hasattr(part, "text"):
                return {
                    "type": "text",
                    "content": part.text,
                }

        return {"type": "unknown"}

