
from google.genai import types

from app.clients.llm_client import LLMClient
from app.tools.tool_executor import ToolExecutor
from app.tools.tool_definitions import get_gemini_tool_definitions


class ResearchService:
    """
    Coordinates research requests, AI responses
    and tool execution.
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
        Runs the AI tool-calling loop until
        Gemini generates a final answer.
        """

        if not question or not question.strip():
            raise ValueError(
                "Research question cannot be empty."
            )

        contents = [
            types.Content(
                role="user",
                parts=[
                    types.Part.from_text(
                        text=f"""
                        You are an AI Research Assistant.

                        Your responsibility is to provide
                        accurate, structured research answers.

                        You have access to a web search tool.

                        Instructions:

                        1. Understand the user's question.

                        2. Use web search when current
                           information is required.

                        3. For a request asking for the
                           biggest five news stories today,
                           perform a focused news search.

                        4. Avoid unnecessary repeated searches.
                           Use a maximum of five tool calls.

                        5. Analyse the search results before
                           preparing your final answer.

                        6. Include relevant source URLs.

                        7. Do not invent facts or sources.

                        8. If information is insufficient,
                           clearly mention the limitation.

                        9. After receiving search results,
                           prepare the final answer instead
                           of continuing to search unnecessarily.

                        User question:
                        {question}
                        """
                    )
                ]
            )
        ]

        max_iterations = 8
        max_tool_calls = 5
        total_tool_calls = 0

        for iteration in range(max_iterations):

            print(
                f"\nAgent iteration: {iteration + 1}"
            )

            # Once the search limit is reached,
            # do not allow additional tool calls.
            available_tools = (
                self.tools
                if total_tool_calls < max_tool_calls
                else []
            )

            if not available_tools:
                print(
                    "Search limit reached. "
                    "Requesting final answer from Gemini."
                )

            response = self.llm_client.generate_with_tools(
                contents=contents,
                tools=available_tools
            )

            function_calls = response.function_calls or []

            # Gemini has generated a normal text response.
            if not function_calls:

                if response.text:
                    return response.text

                raise RuntimeError(
                    "Gemini returned neither a final answer "
                    "nor a function call."
                )

            # Preserve Gemini's function-call message.
            candidate = response.candidates[0]

            contents.append(candidate.content)

            # Execute requested functions.
            for function_call in function_calls:

                if total_tool_calls >= max_tool_calls:
                    raise RuntimeError(
                        "Gemini requested additional tools "
                        "after reaching the tool-call limit."
                    )

                total_tool_calls += 1

                tool_name = function_call.name

                arguments = dict(
                    function_call.args or {}
                )

                print(f"Executing tool: {tool_name}")
                print(f"Arguments: {arguments}")

                result = self.tool_executor.execute(
                    tool_name=tool_name,
                    arguments=arguments
                )

                print(
                    f"Tool execution completed: {tool_name}"
                )

                # Send the tool result back to Gemini.
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

        raise RuntimeError(
            "Agent reached the maximum number of iterations "
            "without generating a final answer."
        )
