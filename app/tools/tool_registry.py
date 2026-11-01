
from app.tools.search_tool import WebSearchTool


class ToolRegistry:
    """
    Maintains all tools available to the AI agent.
    """

    def __init__(self, search_tool: WebSearchTool):

        self.tools = {
            "search_web": search_tool.search_web
        }

    def get_tool(self, tool_name: str):
        """
        Returns a tool based on its name.
        """

        return self.tools.get(tool_name)

    def get_all_tools(self) -> dict:
        """
        Returns all registered tools.
        """

        return self.tools
