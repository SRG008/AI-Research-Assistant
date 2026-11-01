
from typing import Any

from google import genai
from google.genai import types

from app.core.config import Settings


class GeminiClient:
    """
    Handles communication with Google Gemini.
    """

    def __init__(self, settings: Settings):

        self.model = settings.gemini_model

        self.client = genai.Client(
            api_key=settings.gemini_api_key,
            http_options=types.HttpOptions(
                timeout=settings.gemini_timeout
            )
        )

    def generate_response(self, prompt: str) -> str:

        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt
        )

        if not response.text:
            raise RuntimeError(
                "Gemini returned an empty response."
            )

        return response.text

    def generate_with_tools(
        self,
        contents: Any,
        tools: list[Any]
    ) -> Any:
        """
        Sends conversation history and tool definitions
        to Gemini and returns its complete response.
        """

        response = self.client.models.generate_content(
            model=self.model,
            contents=contents,
            config=types.GenerateContentConfig(
                tools=tools
            )
        )

        return response
