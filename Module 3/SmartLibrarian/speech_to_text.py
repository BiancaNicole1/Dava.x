import os
import tempfile

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("OPENAI_API_KEY was not found.")

client = OpenAI(api_key=api_key)


def transcribe_audio(audio_bytes: bytes) -> str:
    if not audio_bytes:
        raise ValueError("No audio data received.")

    with tempfile.NamedTemporaryFile(
        suffix=".wav",
        delete=False,
    ) as temp_audio:

        temp_audio.write(audio_bytes)

        temp_path = temp_audio.name

    try:
        with open(temp_path, "rb") as audio_file:
            transcription = client.audio.transcriptions.create(
                model="gpt-4o-mini-transcribe",
                file=audio_file,
            )

        return transcription.text.strip()

    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)