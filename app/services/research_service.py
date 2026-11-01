
from google.genai import types

from app.clients.llm_client import LLMClient
from app.tools.tool_executor import ToolExecutor
from app.tools.tool_definitions import get_gemini_tool_definitions


class ResearchService:
    """
    Coordinates research requests, AI responses
    and tool execution.

    Maximum Gemini API calls:
    - General questions: 1
    - Research questions: 2
    """

    def __init__(
        self,
        llm_client: LLMClient,
        tool_executor: ToolExecutor
    ):
        self.llm_client = llm_client
        self.tool_executor = tool_executor
        self.tools = get_gemini_tool_definitions()

    def answer_question(self, question: str) -> str:
        """
        Handles a user question using a maximum
        of two Gemini API calls.
        """

        if not question or not question.strip():
            raise ValueError(
                "Research question cannot be empty."
            )

        # Get current date and time using Python.
        # This does not consume a Gemini API call.
        current_datetime = self.tool_executor.execute(
            tool_name="get_current_datetime",
            arguments={}
        )

        instructions = f"""
You are an AI Research Assistant.

CURRENT DATE AND TIME:
{current_datetime}

TOOL SELECTION RULES:

1. Answer general knowledge, definitions,
   educational and programming questions directly.
   Do not use web search unnecessarily.

2. Use search_web when:
   - The user explicitly requests internet research.
   - The user asks for latest, current, recent or today's information.
   - You do not have enough reliable information.

3. For latest news, use the current date and year
   when constructing the search query.

4. For date and time questions, use the supplied
   current date and time. Do not call any tool.

5. Perform only ONE focused web search.

RESEARCH RULES:

6. Use only information supported by search results.
7. Never invent facts, dates or source URLs.
8. Include relevant source URLs.
9. If information cannot be verified, say so.
10. Do not request additional searches.

RESPONSE RULES:

11. Use clear headings and bullet points.
12. Explain technical concepts in simple language.
13. Keep answers concise but complete.
14. Provide a complete final answer.
15. If information is insufficient, explain the limitation.
"""

        contents = [
            types.Content(
                role="user",
                parts=[
                    types.Part.from_text(
                        text=(
                            f"{instructions}\n\n"
                            f"USER QUESTION:\n{question.strip()}"
                        )
                    )
                ]
            )
        ]

        # -----------------------------------------
        # GEMINI API CALL 1
        # Understand the question and decide
        # whether web search is required.
        # -----------------------------------------

        print("\nGemini API call: 1")

        response = self.llm_client.generate_with_tools(
            contents=contents,
            tools=self.tools
        )

        function_calls = response.function_calls or []

        # If no tool is required, return the direct answer.
        if not function_calls:

            if response.text:
                return response.text

            raise RuntimeError(
                "Gemini returned an empty response."
            )

        # Allow only one tool call.
        if len(function_calls) > 1:
            raise RuntimeError(
                "Gemini requested multiple tools. "
                "Only one tool call is allowed."
            )

        function_call = function_calls[0]

        tool_name = function_call.name
        arguments = dict(function_call.args or {})

        # Only web search is allowed here.
        if tool_name != "search_web":
            raise RuntimeError(
                f"Unexpected tool requested: {tool_name}"
            )

        print(f"Executing tool: {tool_name}")
        print(f"Arguments: {arguments}")

        # Execute Tavily search.
        # This does not consume a Gemini API call.
        result = self.tool_executor.execute(
            tool_name=tool_name,
            arguments=arguments
        )

        print("Web search completed.")

        # Preserve Gemini's function-call message.
        if not response.candidates:
            raise RuntimeError(
                "Gemini returned no candidate for its tool call."
            )

        contents.append(
            response.candidates[0].content
        )

        # Send search results back to Gemini.
        function_response = (
            types.Part.from_function_response(
                name=tool_name,
                response={
                    "result": result
                }
            )
        )

        contents.append(
            types.Content(
                role="user",
                parts=[function_response]
            )
        )

        # Explicitly request a final answer.
        contents.append(
            types.Content(
                role="user",
                parts=[
                    types.Part.from_text(
                        text=(
                            "Prepare your final research answer "
                            "using the search results provided above. "
                            "Do not request another tool or search. "
                            "Include relevant source URLs. "
                            "Provide a complete, accurate and concise "
                            "answer. If the results are insufficient, "
                            "clearly explain the limitations."
                        )
                    )
                ]
            )
        )

        # -----------------------------------------
        # GEMINI API CALL 2
        # Analyse search results and generate
        # the final answer without tools.
        # -----------------------------------------

        print("\nGemini API call: 2")

        final_response = self.llm_client.generate_with_tools(
            contents=contents,
            tools=[]
        )

        if not final_response.text:
            raise RuntimeError(
                "Gemini did not generate a final answer."
            )

        return final_response.text
