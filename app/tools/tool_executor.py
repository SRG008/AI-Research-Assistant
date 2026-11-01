
from typing import Any

from app.tools.tool_registry import ToolRegistry


class ToolExecutor:
    """
    Responsible for executing tools requested by the AI.
    """

    def __init__(self, tool_registry: ToolRegistry):

        self.tool_registry = tool_registry

    def execute(
        self,
        tool_name: str,
        arguments: dict[str, Any]
    ) -> Any:
        """
        Finds and executes the requested tool.
        """

        # Step 1: Find the requested function
        tool_function = self.tool_registry.get_tool(
            tool_name
        )

        # Step 2: Check whether the tool exists
        if tool_function is None:
            raise ValueError(
                f"Tool '{tool_name}' is not registered."
            )

        # Step 3: Execute the function with its arguments
        try:
            result = tool_function(**arguments)

            return result

        except Exception as exc:
            raise RuntimeError(
                f"Failed to execute tool '{tool_name}': {exc}"
            ) from exc
