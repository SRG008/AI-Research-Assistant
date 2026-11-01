
from typing import Any, Protocol


class LLMClient(Protocol):
    """
    Common contract for AI providers.
    """

    def generate_response(self, prompt: str) -> str:
        ...

    def generate_with_tools(
        self,
        contents: Any,
        tools: list[Any]
    ) -> Any:
        ...
