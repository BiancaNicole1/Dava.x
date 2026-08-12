import json
import os
from pathlib import Path

import chromadb
from dotenv import load_dotenv
from openai import OpenAI


# ---------------------------------------------------------
# ENVIRONMENT
# ---------------------------------------------------------

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError(
        "OPENAI_API_KEY was not found in the .env file."
    )


# ---------------------------------------------------------
# OPENAI CLIENT
# ---------------------------------------------------------

openai_client = OpenAI(
    api_key=OPENAI_API_KEY
)


# ---------------------------------------------------------
# CHROMADB CLIENT
# ---------------------------------------------------------

chroma_client = chromadb.PersistentClient(
    path="chroma_db"
)

collection = chroma_client.get_or_create_collection(
    name="book_summaries"
)


# ---------------------------------------------------------
# LOAD BOOKS
# ---------------------------------------------------------

def load_books() -> list[dict]:
    file_path = Path(
        "data/book_summaries.json"
    )

    with file_path.open(
        "r",
        encoding="utf-8",
    ) as file:
        return json.load(file)


# ---------------------------------------------------------
# CREATE EMBEDDING
# ---------------------------------------------------------

def create_embedding(
    text: str,
) -> list[float]:

    response = (
        openai_client.embeddings.create(
            model="text-embedding-3-small",
            input=text,
        )
    )

    return response.data[0].embedding


# ---------------------------------------------------------
# BUILD VECTOR DATABASE
# ---------------------------------------------------------

def build_vector_database() -> None:

    books = load_books()

    for index, book in enumerate(
        books
    ):

        text_for_embedding = (
            f"Title: {book['title']}\n"
            f"Author: {book['author']}\n"
            f"Themes: {', '.join(book['themes'])}\n"
            f"Summary: {book['summary']}"
        )

        embedding = create_embedding(
            text_for_embedding
        )

        collection.upsert(
            ids=[
                str(index)
            ],
            documents=[
                text_for_embedding
            ],
            embeddings=[
                embedding
            ],
            metadatas=[
                {
                    "title": book["title"],
                    "author": book["author"],
                    "themes": ", ".join(
                        book["themes"]
                    ),
                }
            ],
        )

        print(
            f"Added to ChromaDB: "
            f"{book['title']}"
        )

    print(
        f"\nThe vector database contains "
        f"{collection.count()} books."
    )


# ---------------------------------------------------------
# SEMANTIC SEARCH
# ---------------------------------------------------------

def search_books(
    query: str,
    number_of_results: int = 3,
) -> list[dict]:

    if not query.strip():
        raise ValueError(
            "The search query cannot be empty."
        )

    query_embedding = create_embedding(
        query
    )

    results = collection.query(
        query_embeddings=[
            query_embedding
        ],
        n_results=number_of_results,
        include=[
            "documents",
            "metadatas",
            "distances",
        ],
    )

    books = []

    for metadata, document, distance in zip(
        results["metadatas"][0],
        results["documents"][0],
        results["distances"][0],
    ):

        books.append(
            {
                "title": metadata["title"],
                "author": metadata["author"],
                "themes": metadata["themes"],
                "document": document,
                "distance": distance,
            }
        )

    return books

if __name__ == "__main__":
    build_vector_database()