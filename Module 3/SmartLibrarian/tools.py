import json
from pathlib import Path


FULL_SUMMARIES_PATH = Path(
    "data/full_summaries.json"
)


# ---------------------------------------------------------
# LOAD FULL SUMMARIES
# ---------------------------------------------------------

def load_full_summaries() -> dict[str, str]:
    """
    Loads the complete book summaries
    from the JSON file.
    """

    if not FULL_SUMMARIES_PATH.exists():

        raise FileNotFoundError(
            f"The file was not found: "
            f"{FULL_SUMMARIES_PATH.resolve()}"
        )

    with FULL_SUMMARIES_PATH.open(
        "r",
        encoding="utf-8",
    ) as file:

        summaries = json.load(file)

    if not isinstance(
        summaries,
        dict,
    ):

        raise ValueError(
            "full_summaries.json must contain "
            "a JSON object."
        )

    return summaries


# ---------------------------------------------------------
# GET SUMMARY BY TITLE
# ---------------------------------------------------------

def get_summary_by_title(
    title: str,
) -> str:
    """
    Returns the complete summary for an exact
    book title.

    The search is case-insensitive.
    """

    summaries = load_full_summaries()

    normalized_title = (
        title
        .strip()
        .lower()
    )

    for stored_title, summary in (
        summaries.items()
    ):

        if (
            stored_title
            .strip()
            .lower()
            == normalized_title
        ):

            return summary

    return (
        f"No complete summary was found "
        f"for the book '{title}'."
    )

if __name__ == "__main__":

    print(
        get_summary_by_title(
            "1984"
        )
    )