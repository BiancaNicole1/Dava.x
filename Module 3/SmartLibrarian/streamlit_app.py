import streamlit as st

from app import recommend_book_with_title
from audio import generate_speech
from image_generator import generate_book_image
from moderation import is_content_safe
from speech_to_text import transcribe_audio


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Smart Librarian",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# =========================================================
# STYLE
# =========================================================

st.markdown(
    """
<style>
:root {
    --bg: #f5f1e8;
    --surface: #fcfbf7;
    --surface-soft: #efebe2;
    --text: #282822;
    --muted: #77766e;
    --border: #dcd8cd;
    --sage: #69715d;
    --sage-dark: #515946;
}

.stApp {
    background: var(--bg);
}

[data-testid="stHeader"] {
    background: transparent;
    height: 2rem;
}

.block-container {
    max-width: 1450px;
    padding-top: 0.8rem;
    padding-bottom: 0.5rem;
}

h1, h2, h3 {
    font-family: Georgia, "Times New Roman", serif;
    color: var(--text);
}

p {
    color: var(--text);
}

/* Header */

.app-title {
    font-family: Georgia, "Times New Roman", serif;
    font-size: 1.75rem;
    font-weight: 700;
    letter-spacing: -0.03em;
    color: var(--text);
}

.header-line {
    border-bottom: 1px solid var(--border);
    margin-top: 0.45rem;
    margin-bottom: 1rem;
}

/* Left intro */

.kicker {
    font-size: 0.68rem;
    text-transform: uppercase;
    letter-spacing: 0.14em;
    font-weight: 700;
    color: var(--sage);
    margin-bottom: 0.3rem;
}

.hero-title {
    font-family: Georgia, "Times New Roman", serif;
    font-size: 2.25rem;
    font-weight: 700;
    letter-spacing: -0.035em;
    line-height: 1.08;
    color: var(--text);
    margin-bottom: 0.45rem;
}

.hero-copy {
    color: var(--muted);
    font-size: 0.9rem;
    line-height: 1.55;
    max-width: 620px;
    margin-bottom: 0.6rem;
}

.section-label {
    font-size: 0.66rem;
    text-transform: uppercase;
    letter-spacing: 0.13em;
    font-weight: 700;
    color: var(--muted);
    margin-bottom: 0.35rem;
}

/* Native containers */

[data-testid="stVerticalBlockBorderWrapper"] {
    border-color: var(--border);
    background: var(--surface);
    border-radius: 16px;
}

/* Chat */

[data-testid="stChatMessage"] {
    background: #ffffff;
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 0.65rem 0.8rem;
    margin-bottom: 0.4rem;
}

[data-testid="stChatMessageContent"] {
    font-size: 0.88rem;
    line-height: 1.5;
}

/* Inputs */

.stTextInput input {
    border-radius: 10px;
    border: 1px solid var(--border);
    background: #ffffff;
    min-height: 42px;
}

.stTextInput input:focus {
    border-color: var(--sage);
    box-shadow: 0 0 0 1px var(--sage);
}

/* Buttons */

.stButton > button,
.stFormSubmitButton > button {
    border-radius: 10px;
    border: 1px solid var(--border);
    background: var(--surface);
    color: var(--text);
    font-weight: 600;
    min-height: 40px;
    box-shadow: none;
}

.stButton > button:hover,
.stFormSubmitButton > button:hover {
    border-color: #aaa99f;
    background: var(--surface-soft);
    color: var(--text);
}

/* Primary-looking form button */

.stFormSubmitButton > button {
    background: var(--sage);
    color: white;
    border-color: var(--sage);
}

.stFormSubmitButton > button:hover {
    background: var(--sage-dark);
    color: white;
    border-color: var(--sage-dark);
}

/* Recommendation */

.book-label {
    font-size: 0.66rem;
    text-transform: uppercase;
    letter-spacing: 0.14em;
    font-weight: 700;
    color: var(--sage);
}

.book-title {
    font-family: Georgia, "Times New Roman", serif;
    font-size: 2rem;
    font-weight: 700;
    line-height: 1.08;
    color: var(--text);
    margin-top: 0.15rem;
    margin-bottom: 0.5rem;
}

.placeholder {
    height: 235px;
    border: 1px dashed #c9c5b9;
    border-radius: 13px;
    background: linear-gradient(145deg, #eeebe2, #faf8f3);
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: 1.5rem;
}

.placeholder-title {
    font-family: Georgia, "Times New Roman", serif;
    font-size: 1.25rem;
    font-weight: 700;
    color: var(--text);
    margin-bottom: 0.4rem;
}

.placeholder-copy {
    max-width: 310px;
    margin: auto;
    color: var(--muted);
    font-size: 0.84rem;
    line-height: 1.5;
}

.content-title {
    font-family: Georgia, "Times New Roman", serif;
    font-size: 1.15rem;
    font-weight: 700;
    color: var(--text);
}

.helper {
    color: var(--muted);
    font-size: 0.82rem;
    line-height: 1.45;
}

/* Generated image */

[data-testid="stImage"] img {
    border-radius: 13px;
    border: 1px solid var(--border);
    max-height: 300px;
    object-fit: cover;
}

/* Audio */

audio {
    width: 100%;
}

/* Expander */

[data-testid="stExpander"] {
    border-color: var(--border);
    border-radius: 10px;
    background: var(--surface);
}

/* Hide Streamlit footer */

footer {
    visibility: hidden;
}

@media (max-width: 900px) {
    .hero-title {
        font-size: 1.8rem;
    }

    .placeholder {
        height: 200px;
    }
}

/* =====================================================
   FINAL BOOKISH POLISH
===================================================== */


/* -----------------------------------------------------
   BACKGROUND
----------------------------------------------------- */

.stApp {
    background:
        radial-gradient(
            circle at 8% 12%,
            rgba(123, 100, 80, 0.045) 0px,
            rgba(123, 100, 80, 0.045) 70px,
            transparent 71px
        ),
        radial-gradient(
            circle at 94% 88%,
            rgba(105, 113, 93, 0.05) 0px,
            rgba(105, 113, 93, 0.05) 90px,
            transparent 91px
        ),
        #f5f1e8;
}


/* -----------------------------------------------------
   MAIN SEARCH BUTTON
----------------------------------------------------- */

.stFormSubmitButton > button {
    background: #e7d8c8 !important;
    color: #4c4038 !important;

    border: 1px solid #cfbaa7 !important;
    border-radius: 11px !important;

    min-height: 42px;

    font-weight: 600;

    box-shadow:
        0 3px 10px rgba(73, 57, 45, 0.06) !important;

    transition:
        background 0.15s ease,
        border-color 0.15s ease,
        transform 0.15s ease,
        box-shadow 0.15s ease;
}


.stFormSubmitButton > button:hover {
    background: #ddc7b4 !important;
    color: #3d332d !important;

    border-color: #bfa28d !important;

    transform: translateY(-1px);

    box-shadow:
        0 5px 14px rgba(73, 57, 45, 0.09) !important;
}


/* -----------------------------------------------------
   SECONDARY BUTTONS
----------------------------------------------------- */

.stButton > button {
    background: #fbf9f4 !important;
    color: #514d47 !important;

    border: 1px solid #d8d3c9 !important;
    border-radius: 10px !important;

    box-shadow:
        0 2px 6px rgba(55, 50, 42, 0.03);

    transition:
        background 0.15s ease,
        border-color 0.15s ease,
        transform 0.15s ease;
}


.stButton > button:hover {
    background: #eee8de !important;
    color: #3f3c37 !important;

    border-color: #beb7aa !important;

    transform: translateY(-1px);
}


/* -----------------------------------------------------
   PANELS
----------------------------------------------------- */

[data-testid="stVerticalBlockBorderWrapper"] {
    background: rgba(252, 251, 247, 0.96);

    border: 1px solid #ddd8cd;

    box-shadow:
        0 10px 28px rgba(55, 49, 39, 0.04);
}


/* -----------------------------------------------------
   INPUT
----------------------------------------------------- */

.stTextInput input {
    background: #fffdfa !important;

    border: 1px solid #d8d1c5 !important;

    color: #282822 !important;
}


.stTextInput input:focus {
    border-color: #bba591 !important;

    box-shadow:
        0 0 0 2px rgba(187, 165, 145, 0.12) !important;
}


/* -----------------------------------------------------
   BOOK TITLE
----------------------------------------------------- */

.book-title {
    color: #35312d;
    font-size: 2.05rem;
    letter-spacing: -0.04em;
}


/* -----------------------------------------------------
   PLACEHOLDER
----------------------------------------------------- */

.placeholder {
    background:
        linear-gradient(
            145deg,
            #eee8dd,
            #faf7f0
        );

    border-color: #d0c5b8;

    box-shadow:
        inset 0 0 35px rgba(114, 93, 73, 0.025);
}


/* -----------------------------------------------------
   SMALL BOOKISH ACCENTS
----------------------------------------------------- */

.app-title::after {
    content: "  /  library notes";

    font-family: Georgia, "Times New Roman", serif;

    font-size: 0.72rem;
    font-weight: 400;
    font-style: italic;

    letter-spacing: 0;

    color: #9a8d80;

    margin-left: 0.5rem;
}


/* -----------------------------------------------------
   EXPANDER
----------------------------------------------------- */

[data-testid="stExpander"] {
    background: #faf8f3;

    border: 1px solid #ddd7cb;

    border-radius: 10px;
}

</style>
""",
    unsafe_allow_html=True,
)


# =========================================================
# SESSION STATE
# =========================================================

DEFAULT_STATE = {
    "messages": [],
    "recommended_title": None,
    "latest_answer": None,
    "generated_image": None,
    "generated_audio": None,
    "moderation_error": None,
}

for key, default in DEFAULT_STATE.items():
    if key not in st.session_state:
        st.session_state[key] = default


# =========================================================
# HELPERS
# =========================================================

def reset_app():
    st.session_state.messages = []
    st.session_state.recommended_title = None
    st.session_state.latest_answer = None
    st.session_state.generated_image = None
    st.session_state.generated_audio = None
    st.session_state.moderation_error = None


def process_safe_query(question: str):
    """
    Processes a request that has already passed moderation.
    """

    question = question.strip()

    if not question:
        return

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question,
        }
    )

    with st.spinner(
        "Searching the library..."
    ):
        result = recommend_book_with_title(
            question
        )

    answer = str(
        result["answer"]
    )

    title = result["title"]

    st.session_state.latest_answer = answer
    st.session_state.recommended_title = title

    # A new recommendation should not keep
    # media generated for the previous book.
    st.session_state.generated_image = None
    st.session_state.generated_audio = None

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer,
        }
    )


def moderate_and_process(question: str) -> bool:
    """
    Moderates a request and processes it only
    when the request is considered safe.

    Returns True when the request was processed.
    Returns False when moderation blocked it.
    """

    question = question.strip()

    if not question:
        return False

    is_safe, moderation_message = (
        is_content_safe(question)
    )

    if not is_safe:
        st.session_state.moderation_error = (
            "This request cannot be processed because "
            "it may contain unsafe or inappropriate content. "
            "Please try a different reading request."
        )

        return False

    st.session_state.moderation_error = None

    process_safe_query(question)

    return True


# =========================================================
# HEADER
# =========================================================

st.markdown(
    '<div class="app-title">Smart Librarian</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="header-line"></div>',
    unsafe_allow_html=True,
)

# =========================================================
# MAIN TWO-COLUMN LAYOUT
# =========================================================

left_col, right_col = st.columns(
    [1, 1],
    gap="large",
)


# =========================================================
# LEFT — CONVERSATION
# =========================================================

with left_col:

    st.markdown(
        '<div class="kicker">'
        'Personal reading assistant'
        '</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="hero-title">'
        'Find the book you want to read next.'
        '</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="hero-copy">'
        'Describe a mood, theme, setting or idea. '
        'Smart Librarian will search the collection '
        'and recommend the closest match.'
        '</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="section-label">'
        'Conversation'
        '</div>',
        unsafe_allow_html=True,
    )


    # -----------------------------------------------------
    # CONVERSATION
    # -----------------------------------------------------

    chat_area = st.container(
        height=245,
        border=True,
    )

    with chat_area:

        if not st.session_state.messages:

            st.caption(
                'Example: "I want a thought-provoking '
                'book about freedom and social control."'
            )

        for message in st.session_state.messages:

            with st.chat_message(
                message["role"]
            ):
                st.markdown(
                    message["content"]
                )


    # -----------------------------------------------------
    # SEARCH FORM
    # -----------------------------------------------------

    with st.form(
        "search_form",
        clear_on_submit=True,
    ):

        typed_query = st.text_input(
            "Book request",
            placeholder=(
                "Describe a theme, mood or kind of story..."
            ),
            label_visibility="collapsed",
        )

        submit_search = (
            st.form_submit_button(
                "Find a book",
                use_container_width=True,
            )
        )


    # -----------------------------------------------------
    # FIXED MODERATION MESSAGE AREA
    # -----------------------------------------------------

    moderation_placeholder = st.empty()


    if st.session_state.moderation_error:

        moderation_placeholder.error(
            st.session_state.moderation_error,
            icon=None,
        )


    # -----------------------------------------------------
    # PROCESS TYPED REQUEST
    # -----------------------------------------------------

    if submit_search and typed_query.strip():

        try:

            # Remove an old warning before evaluating
            # the newly submitted request.
            st.session_state.moderation_error = None

            is_safe, moderation_message = (
                is_content_safe(
                    typed_query.strip()
                )
            )


            # ---------------------------------------------
            # BLOCKED REQUEST
            # ---------------------------------------------

            if not is_safe:

                st.session_state.moderation_error = (
                    "This request cannot be processed because "
                    "it may contain unsafe or inappropriate "
                    "content. Please try a different "
                    "reading request."
                )

                # Display it NOW in the placeholder that
                # sits directly below the search button.
                moderation_placeholder.error(
                    st.session_state.moderation_error,
                    icon=None,
                )


            # ---------------------------------------------
            # SAFE REQUEST
            # ---------------------------------------------

            else:

                moderation_placeholder.empty()

                process_safe_query(
                    typed_query.strip()
                )

                st.rerun()


        except Exception as error:

            moderation_placeholder.error(
                "The request could not be processed.",
                icon=None,
            )

            st.exception(error)


    # -----------------------------------------------------
    # VOICE SEARCH
    # -----------------------------------------------------

    with st.expander(
        "Voice search",
        expanded=False,
    ):

        st.caption(
            "Record a short description of the "
            "book you would like to discover."
        )

        recorded_audio = st.audio_input(
            "Record your request",
            label_visibility="collapsed",
        )


        if recorded_audio is not None:

            if st.button(
                "Transcribe and search",
                key="voice_search_button",
                use_container_width=True,
            ):

                try:

                    with st.spinner(
                        "Transcribing..."
                    ):

                        transcription = (
                            transcribe_audio(
                                recorded_audio.getvalue()
                            )
                        )


                    if transcription:

                        is_safe, moderation_message = (
                            is_content_safe(
                                transcription
                            )
                        )


                        if not is_safe:

                            st.session_state.moderation_error = (
                                "This request cannot be "
                                "processed because it may "
                                "contain unsafe or inappropriate "
                                "content. Please try a different "
                                "reading request."
                            )

                            st.rerun()


                        else:

                            st.session_state.moderation_error = (
                                None
                            )

                            process_safe_query(
                                transcription
                            )

                            st.rerun()


                except Exception as error:

                    st.error(
                        "The recording could not "
                        "be processed."
                    )

                    st.exception(error)


    # -----------------------------------------------------
    # CLEAR CONVERSATION
    # -----------------------------------------------------

    if st.session_state.messages:

        if st.button(
            "Clear conversation",
            key="clear_conversation",
            use_container_width=True,
        ):

            reset_app()

            st.rerun()

# =========================================================
# RIGHT — BOOK / ARTWORK / AUDIO
# =========================================================

with right_col:

    recommendation_panel = st.container(
        border=True,
    )

    with recommendation_panel:

        # ---------------------------------------------
        # EMPTY STATE
        # ---------------------------------------------

        if not st.session_state.recommended_title:

            st.markdown(
                """
<div class="placeholder">
    <div>
        <div class="placeholder-title">
            Your next book starts here
        </div>
        <div class="placeholder-copy">
            Your recommendation, generated artwork and
            listening options will appear here.
        </div>
    </div>
</div>
""",
                unsafe_allow_html=True,
            )

            st.caption(
                "Start by describing what you would like "
                "to read on the left."
            )


        # ---------------------------------------------
        # BOOK FOUND
        # ---------------------------------------------

        else:

            title = st.session_state.recommended_title

            st.markdown(
                '<div class="book-label">'
                'Recommended for you'
                '</div>',
                unsafe_allow_html=True,
            )

            st.markdown(
                f'<div class="book-title">{title}</div>',
                unsafe_allow_html=True,
            )


            # -----------------------------------------
            # ARTWORK AREA
            # -----------------------------------------

            image_col, control_col = st.columns(
                [1.25, 0.75],
                vertical_alignment="center",
            )

            with image_col:

                if st.session_state.generated_image:

                    st.image(
                        st.session_state.generated_image,
                        use_container_width=True,
                    )

                else:

                    st.markdown(
                        """
<div class="placeholder">
    <div>
        <div class="placeholder-title">
            Visual interpretation
        </div>
        <div class="placeholder-copy">
            Create an original illustration inspired by
            the atmosphere of this book.
        </div>
    </div>
</div>
""",
                        unsafe_allow_html=True,
                    )


            with control_col:

                st.markdown(
                    '<div class="content-title">'
                    'Artwork'
                    '</div>',
                    unsafe_allow_html=True,
                )

                st.markdown(
                    '<div class="helper">'
                    'Generate a visual inspired by the '
                    'book without reproducing its cover.'
                    '</div>',
                    unsafe_allow_html=True,
                )

                if st.button(
                    "Generate artwork",
                    key=f"art_{title}",
                    use_container_width=True,
                ):

                    try:

                        with st.spinner(
                            "Creating artwork..."
                        ):

                            image_path = generate_book_image(
                                title
                            )

                        st.session_state.generated_image = (
                            str(image_path)
                        )

                        st.rerun()

                    except Exception as error:

                        st.error(
                            "The artwork could not be generated."
                        )

                        st.exception(error)


            # -----------------------------------------
            # RECOMMENDATION
            # -----------------------------------------

            if st.session_state.latest_answer:

                st.divider()

                details_col, audio_col = st.columns(
                    [1.4, 0.6],
                    vertical_alignment="top",
                )


                with details_col:

                    st.markdown(
                        '<div class="content-title">'
                        'Why this book'
                        '</div>',
                        unsafe_allow_html=True,
                    )

                    summary_area = st.container(
                        height=155,
                    )

                    with summary_area:

                        st.markdown(
                            st.session_state.latest_answer
                        )


                # -------------------------------------
                # AUDIO
                # -------------------------------------

                with audio_col:

                    st.markdown(
                        '<div class="content-title">'
                        'Listen'
                        '</div>',
                        unsafe_allow_html=True,
                    )

                    st.markdown(
                        '<div class="helper">'
                        'Hear the recommendation and summary.'
                        '</div>',
                        unsafe_allow_html=True,
                    )

                    if st.session_state.generated_audio:

                        st.audio(
                            st.session_state.generated_audio,
                            format="audio/mp3",
                        )

                    else:

                        if st.button(
                            "Generate audio",
                            key=f"audio_{title}",
                            use_container_width=True,
                        ):

                            try:

                                with st.spinner(
                                    "Preparing audio..."
                                ):

                                    audio_path = generate_speech(
                                        st.session_state.latest_answer,
                                        title,
                                    )

                                st.session_state.generated_audio = (
                                    str(audio_path)
                                )

                                st.rerun()

                            except Exception as error:

                                st.error(
                                    "The audio could not be generated."
                                )

                                st.exception(error)