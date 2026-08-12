import base64
import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("OPENAI_API_KEY was not found.")

client = OpenAI(api_key=api_key)


OUTPUT_FOLDER = Path("generated_images")
OUTPUT_FOLDER.mkdir(exist_ok=True)


def safe_filename(title: str) -> str:
    characters = []

    for char in title.lower():
        if char.isalnum():
            characters.append(char)
        elif char in {" ", "-", "_"}:
            characters.append("_")

    filename = "".join(characters)

    while "__" in filename:
        filename = filename.replace("__", "_")

    return filename.strip("_") or "book_artwork"


def generate_book_image(title: str) -> Path:
    if not title.strip():
        raise ValueError("Book title cannot be empty.")

    prompt = f"""
Create an original literary illustration inspired by the themes,
mood and atmosphere of the book "{title}".

The illustration should have:
- an elegant editorial aesthetic
- a sophisticated bookish atmosphere
- warm and cinematic lighting
- rich but tasteful visual details
- no written text
- no logos
- no author name
- no book title
- no reproduction of an existing book cover

The artwork should look suitable for a premium reading
recommendation application.
""".strip()

    response = client.images.generate(
        model="gpt-image-1",
        prompt=prompt,
        size="1024x1024",
    )

    image_base64 = response.data[0].b64_json

    if not image_base64:
        raise RuntimeError(
            "The image generation API returned no image data."
        )

    image_bytes = base64.b64decode(image_base64)

    image_path = (
        OUTPUT_FOLDER
        / f"{safe_filename(title)}.png"
    )

    image_path.write_bytes(image_bytes)

    return image_path