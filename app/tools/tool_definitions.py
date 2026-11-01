
from google.genai import types


def get_gemini_tool_definitions():

    search_web_declaration = types.FunctionDeclaration(
        name="search_web",
        description=(
            "Search the internet for current information "
            "about a topic. Use this tool when the user "
            "needs recent information or web research."
        ),
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "query": types.Schema(
                    type=types.Type.STRING,
                    description=(
                        "The search query to send to Tavily."
                    )
                ),
                "max_results": types.Schema(
                    type=types.Type.INTEGER,
                    description=(
                        "Maximum number of search results. "
                        "Must be between 1 and 10."
                    )
                )
            },
            required=["query"]
        )
    )

    return [
        types.Tool(
            function_declarations=[
                search_web_declaration
            ]
        )
    ]
