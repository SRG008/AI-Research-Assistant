
from app.services.research_service import ResearchService


class ConsoleInterface:
    """
    Handles user interaction through the terminal.
    """

    def __init__(self, research_service: ResearchService):

        self.research_service = research_service

    def start(self):
        """
        Start the interactive console application.
        """

        print("=" * 55)
        print("             AI RESEARCH ASSISTANT")
        print("=" * 55)

        print("\nAsk me a research question.")
        print("Type 'exit' or 'quit' to stop.")

        while True:

            try:

                question = input("\nYou: ").strip()

                if question.lower() in {"exit", "quit"}:
                    print("\nGoodbye!")
                    break

                if not question:
                    print("Please enter a question.")
                    continue

                print("\nResearch Assistant: Thinking...\n")

                answer = self.research_service.answer_question(
                    question
                )

                print("Research Assistant:")
                print(answer)

            except KeyboardInterrupt:

                print("\n\nApplication interrupted. Goodbye!")
                break

            except Exception as exc:

                print(
                    f"\nSomething went wrong: "
                    f"{type(exc).__name__}: {exc}"
                )
