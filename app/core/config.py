
import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(PROJECT_ROOT / ".env")


@dataclass(frozen=True)
class Settings:
    gemini_api_key: str
    gemini_model: str
    gemini_timeout: int
    tavily_api_key: str


def load_settings() -> Settings:

    gemini_api_key = os.getenv("GEMINI_API_KEY")
    tavily_api_key = os.getenv("TAVILY_API_KEY")

    if not gemini_api_key:
        raise ValueError("GEMINI_API_KEY is missing.")

    if not tavily_api_key:
        raise ValueError("TAVILY_API_KEY is missing.")

    model = os.getenv(
        "GEMINI_MODEL",
        "gemini-3.6-flash"
    )

    timeout = int(
        os.getenv("GEMINI_TIMEOUT", "60000")
    )

    if timeout <= 0:
        raise ValueError(
            "GEMINI_TIMEOUT must be greater than zero."
        )

    return Settings(
        gemini_api_key=gemini_api_key,
        gemini_model=model,
        gemini_timeout=timeout,
        tavily_api_key=tavily_api_key
    )
