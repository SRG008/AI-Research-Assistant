from app.core.config import load_settings

from app.clients.gemini_client import GeminiClient

from app.tools.search_tool import WebSearchTool
from app.tools.tool_registry import ToolRegistry
from app.tools.tool_executor import ToolExecutor

from app.services.research_service import ResearchService
from app.interfaces.console import ConsoleInterface


def main():

    # 1. Load application configuration
    settings = load_settings()

    # 2. Initialize AI client
    llm_client = GeminiClient(settings)

    # 3. Initialize web search tool
    search_tool = WebSearchTool(settings)

    # 4. Register available tools
    tool_registry = ToolRegistry(search_tool)

    # 5. Initialize tool executor
    tool_executor = ToolExecutor(tool_registry)

    # 6. Initialize research service
    research_service = ResearchService(
        llm_client=llm_client,
        tool_executor=tool_executor
    )

    # 7. Start console application
    console = ConsoleInterface(research_service)

    console.start()


if __name__ == "__main__":
    main()