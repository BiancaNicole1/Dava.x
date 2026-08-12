import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("OPENAI_API_KEY was not found.")

client = OpenAI(api_key=api_key)


AUDIO_FOLDER = Path("generated_audio")
AUDIO_FOLDER.mkdir(exist_ok=True)


def safe_filename(title: str) -> str:
    result = []

    for character in title.lower():
        if character.isalnum():
            result.append(character)
        elif character in {" ", "-", "_"}:
            result.append("_")

    filename = "".join(result)

    while "__" in filename:
        filename = filename.replace("__", "_")

    return filename.strip("_") or "recommendation"


def generate_speech(
    text: str,
    title: str,
) -> Path:
    if not text.strip():
        raise ValueError(
            "The text cannot be empty."
        )

    output_path = (
        AUDIO_FOLDER
        / f"{safe_filename(title)}.mp3"
    )

    with client.audio.speech.with_streaming_response.create(
        model="gpt-4o-mini-tts",
        voice="alloy",
        input=text,
    ) as response:
        response.stream_to_file(output_path)

    return output_path