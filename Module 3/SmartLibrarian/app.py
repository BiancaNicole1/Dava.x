import json
import os
from typing import Any

from dotenv import load_dotenv
from openai import OpenAI

from rag import search_books
from tools import get_summary_by_title


# ---------------------------------------------------------
# OPENAI CONFIG
# ---------------------------------------------------------

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError(
        "OPENAI_API_KEY was not found."
    )

client = OpenAI(api_key=api_key)


# ---------------------------------------------------------
# TOOL DEFINITION
# ---------------------------------------------------------

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_summary_by_title",
            "description": (
                "Returns the complete summary of a book "
                "using its exact title."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {
                        "type": "string",
                        "description": "The exact title of the book.",
                    }
                },
                "required": ["title"],
                "additionalProperties": False,
            },
        },
    }
]


# ---------------------------------------------------------
# BUILD RAG CONTEXT
# ---------------------------------------------------------

def build_context(
    books: list[dict[str, Any]],
) -> str:

    context_parts = []

    for index, book in enumerate(
        books,
        start=1,
    ):
        context_parts.append(
            f"""
Book {index}

Title: {book["title"]}
Author: {book["author"]}
Themes: {book["themes"]}

Description:
{book["document"]}
""".strip()
        )

    return "\n\n".join(context_parts)


# ---------------------------------------------------------
# EXECUTE TOOL
# ---------------------------------------------------------

def execute_tool(
    tool_name: str,
    arguments: dict[str, Any],
) -> str:

    if tool_name == "get_summary_by_title":

        title = arguments.get(
            "title",
            "",
        )

        return get_summary_by_title(title)

    return f"Unknown tool: {tool_name}"


# ---------------------------------------------------------
# RECOMMEND BOOK
# ---------------------------------------------------------

def recommend_book_with_title(
    question: str,
) -> dict[str, str | None]:

    if not question.strip():

        return {
            "answer": "Please enter a question.",
            "title": None,
        }


    # -----------------------------------------------------
    #  RAG
    # -----------------------------------------------------

    relevant_books = search_books(
        question,
        number_of_results=3,
    )

    context = build_context(
        relevant_books
    )


    # -----------------------------------------------------
    # PROMPT
    # -----------------------------------------------------

    system_message = """
You are Smart Librarian, an AI assistant specialized
in book recommendations.

Rules:

1. Recommend only books that appear in the provided context.

2. Select exactly one book that best matches the user's request.

3. Briefly explain why the book is a good match.

4. After selecting the book, you must call the
   get_summary_by_title tool using the exact title from the context.

5. After receiving the tool result, include the complete
   summary in your final response.

6. Never invent books, authors or information.

7. Always respond in English.
""".strip()


    user_message = f"""
User request:

{question}

Books retrieved through RAG:

{context}
""".strip()


    messages: list[dict[str, Any]] = [
        {
            "role": "system",
            "content": system_message,
        },
        {
            "role": "user",
            "content": user_message,
        },
    ]


    # -----------------------------------------------------
    # GPT DECIDES WHICH TOOL TO CALL
    # -----------------------------------------------------

    first_response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=messages,
        tools=TOOLS,
        tool_choice="auto",
    )


    assistant_message = (
        first_response
        .choices[0]
        .message
    )


    messages.append(
        {
            "role": "assistant",
            "content": assistant_message.content,
            "tool_calls": assistant_message.tool_calls,
        }
    )


    if not assistant_message.tool_calls:

        return {
            "answer": (
                assistant_message.content
                or "I could not generate a recommendation."
            ),
            "title": None,
        }


    # -----------------------------------------------------
    # EXECUTE TOOL
    # -----------------------------------------------------

    recommended_title = None


    for tool_call in assistant_message.tool_calls:

        try:

            function_arguments = json.loads(
                tool_call.function.arguments
            )

        except json.JSONDecodeError:

            function_arguments = {}


        if (
            tool_call.function.name
            == "get_summary_by_title"
        ):

            recommended_title = (
                function_arguments.get("title")
            )


        tool_result = execute_tool(
            tool_name=tool_call.function.name,
            arguments=function_arguments,
        )


        messages.append(
            {
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": tool_result,
            }
        )


    # -----------------------------------------------------
    # FINAL GPT RESPONSE
    # -----------------------------------------------------

    final_response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=messages,
        tools=TOOLS,
    )


    answer = (
        final_response
        .choices[0]
        .message
        .content
        or "I could not generate the final response."
    )


    return {
        "answer": answer,
        "title": recommended_title,
    }


# ---------------------------------------------------------
# SIMPLE VERSION
# ---------------------------------------------------------

def recommend_book(
    question: str,
) -> str:

    result = recommend_book_with_title(
        question
    )

    return str(
        result["answer"]
    )


# ---------------------------------------------------------
# CLI TEST
# ---------------------------------------------------------

def main() -> None:

    print("=" * 60)
    print("SMART LIBRARIAN")
    print("Type 'exit' to close the application.")
    print("=" * 60)


    while True:

        question = input(
            "\nWhat kind of book are you looking for? "
        ).strip()


        if question.lower() in {
            "exit",
            "quit",
            "q",
        }:

            print(
                "\nSmart Librarian has been closed."
            )

            break


        try:

            result = (
                recommend_book_with_title(
                    question
                )
            )


            print(
                "\nRecommended book:"
            )

            print(
                result["title"]
            )


            print(
                "\nRecommendation:"
            )

            print(
                result["answer"]
            )


        except Exception as error:

            print(
                f"\nAn error occurred: "
                f"{error}"
            )


if __name__ == "__main__":
    main()