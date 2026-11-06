import os
from pathlib import Path
from dotenv import load_dotenv
from hindsight_client import Hindsight

# Load backend environment variables
ENV_PATH = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(ENV_PATH)

def get_hindsight_client():
    api_key = os.getenv("HINDSIGHT_API_KEY")
    base_url = os.getenv(
        "HINDSIGHT_BASE_URL",
        "https://api.hindsight.vectorize.io"
    )

    if not api_key:
        raise ValueError("HINDSIGHT_API_KEY missing from .env")

    client = Hindsight(
        base_url=base_url,
        api_key=api_key
    )

    return client


def get_memory_bank_id():
    return os.getenv(
        "HINDSIGHT_BANK_ID",
        "incident-response-agent"
    )