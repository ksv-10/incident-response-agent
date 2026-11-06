import os
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from backend/.env
ENV_PATH = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(ENV_PATH)


def get_xai_client():
    api_key = os.getenv("XAI_API_KEY")

    if not api_key:
        raise ValueError("XAI_API_KEY missing from .env")

    client = OpenAI(
        api_key=api_key,
        base_url="https://api.x.ai/v1"
    )

    return client