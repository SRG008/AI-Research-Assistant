
from google.genai import types


def get_gemini_tool_definitions():

    # Tool 1: Web Search
    search_web_declaration = types.FunctionDeclaration(
        name="search_web",
        description=(
            "Search the internet ONLY when the user needs "
            "current, latest, recent, breaking, or time-sensitive "
            "information, or explicitly asks you to search the web. "
            "Do NOT use this tool for ordinary educational questions, "
            "definitions, explanations, programming concepts, "
            "or general knowledge that you can answer yourself."
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

    # Tool 2: Current Date and Time
    datetime_declaration = types.FunctionDeclaration(
        name="get_current_datetime",
        description=(
            "Get the current local date, time, day and timezone. "
            "Use this tool when the user asks about today's date, "
            "the current time or the current day."
        ),
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={},
            required=[]
        )
    )

    # Return both tools to Gemini
    return [
        types.Tool(
            function_declarations=[
                search_web_declaration,
                datetime_declaration
            ]
        )
    ]
