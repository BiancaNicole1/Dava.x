import os

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("OPENAI_API_KEY was not found.")

client = OpenAI(api_key=api_key)


def is_content_safe(text: str) -> tuple[bool, str]:
    if not text.strip():
        return False, "The message is empty."

    response = client.moderations.create(
        model="omni-moderation-latest",
        input=text,
    )

    result = response.results[0]

    if result.flagged:
        return (
            False,
            "This request was blocked because it may contain unsafe content.",
        )

    return True, ""