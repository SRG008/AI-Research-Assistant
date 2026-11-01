
from app.tools.search_tool import WebSearchTool
from app.tools.datetime_tool import DateTimeTool


class ToolRegistry:
    """
    Maintains all tools available to the AI agent.
    """

    def __init__(
        self,
        search_tool: WebSearchTool,
        datetime_tool: DateTimeTool
    ):

        self.tools = {
            "search_web": search_tool.search_web,
            "get_current_datetime": datetime_tool.get_current_datetime
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
