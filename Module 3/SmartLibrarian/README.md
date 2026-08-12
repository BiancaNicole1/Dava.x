# Smart Librarian

Smart Librarian is an AI-powered book recommendation application built with OpenAI, ChromaDB, Retrieval-Augmented Generation (RAG), tool calling, and Streamlit.

The application allows users to describe the type of book they would like to read using either text or voice. Smart Librarian searches a vector database containing book summaries, retrieves the most relevant books, and uses an OpenAI language model to generate a personalized recommendation.

The application also supports image generation, text-to-speech, speech-to-text, and content moderation.

---

## Features

### Semantic Book Search

Book summaries are converted into vector embeddings using:

`text-embedding-3-small`

The embeddings are stored in ChromaDB and used for semantic similarity search.

---

### Retrieval-Augmented Generation

When a user submits a request:

1. The request is converted into an embedding.
2. ChromaDB retrieves the most relevant books.
3. The retrieved book information is added to the model context.
4. The language model selects the most appropriate recommendation.

---

### AI Book Recommendation

The application uses:

`gpt-4.1-mini`

The model receives the user's request together with the books retrieved through RAG and selects one book that best matches the user's interests.

---

### Tool Calling

The application exposes the following function to the language model:

```python
get_summary_by_title(title: str)
```

After selecting a book, the model calls this function using the exact book title.

The tool retrieves the complete summary from:

```text
data/full_summaries.json
```

The returned summary is then included in the final recommendation.

---

### Content Moderation

User requests are checked before being processed using:

`omni-moderation-latest`

Unsafe requests are blocked before reaching the recommendation pipeline.

---

### Image Generation

Users can generate an original visual interpretation of the recommended book.

The application uses:

`gpt-image-1`

Generated images are stored in:

```text
generated_images/
```

The generated artwork is inspired by the themes and atmosphere of the selected book and does not attempt to reproduce an existing book cover.

---

### Text-to-Speech

The recommendation and complete book summary can be converted into audio.

The application uses:

`gpt-4o-mini-tts`

Generated audio files are stored in:

```text
generated_audio/
```

---

### Speech-to-Text

Users can record their book request directly from the Streamlit interface.

The recording is transcribed using:

`gpt-4o-mini-transcribe`

The transcription is then processed through the same moderation, RAG, recommendation, and tool-calling pipeline as a typed request.

---

## Technology Stack

* Python 3.13
* OpenAI API
* ChromaDB
* Streamlit
* Docker / Rancher Desktop
* OpenAI Embeddings
* OpenAI Tool Calling
* OpenAI Moderation
* OpenAI Image Generation
* OpenAI Text-to-Speech
* OpenAI Speech-to-Text

---

## Project Structure

```text
SmartLibrarian/
│
├── app.py
├── rag.py
├── tools.py
├── moderation.py
├── image_generator.py
├── audio.py
├── speech_to_text.py
├── streamlit_app.py
│
├── Dockerfile
├── requirements.txt
├── README.md
├── .env
├── .gitignore
├── .dockerignore
│
├── data/
│   ├── book_summaries.json
│   └── full_summaries.json
│
├── chroma_db/
├── generated_images/
└── generated_audio/
```

---

## Main Components

### `rag.py`

Responsible for:

* loading the book dataset
* generating OpenAI embeddings
* storing embeddings in ChromaDB
* performing semantic search
* returning the most relevant books

---

### `tools.py`

Contains:

```python
get_summary_by_title(title: str)
```

The function retrieves the complete summary for an exact book title.

---

### `app.py`

Contains the main recommendation pipeline:

```text
User request
      |
      v
RAG retrieval
      |
      v
Relevant books
      |
      v
GPT recommendation
      |
      v
Tool Calling
      |
      v
get_summary_by_title()
      |
      v
Final response
```

---

### `moderation.py`

Checks user input before it is sent to the recommendation pipeline.

---

### `image_generator.py`

Generates original artwork inspired by the selected book.

---

### `audio.py`

Converts the recommendation and summary into spoken audio.

---

### `speech_to_text.py`

Transcribes recorded user requests into text.

---

### `streamlit_app.py`

Provides the graphical user interface.

The interface contains:

* text search
* voice search
* conversation history
* book recommendation
* generated artwork
* recommendation explanation
* complete summary
* audio generation

---

# Running the Project with Docker

## 1. Open the Project

Open PowerShell and navigate to the project directory:

---

## 2. Configure the OpenAI API Key

Create a `.env` file in the project root.

Add:

```text
OPENAI_API_KEY=your_openai_api_key
```

Do not upload the `.env` file to a public repository.

---

## 3. Build the Docker Image

Run:

```powershell
docker build -t smart-librarian .
```

---

## 4. Create the ChromaDB Volume

Run:

```powershell
docker volume create smart-librarian-chroma
```

---

## 5. Initialize the Vector Database

Run:

```powershell
docker run --rm `
  --env-file .env `
  -v smart-librarian-chroma:/app/chroma_db `
  smart-librarian python rag.py
```

The expected result is similar to:

```text
Added to ChromaDB: 1984
Added to ChromaDB: The Hobbit
...
The vector database contains 10 books.
```

This initialization is required before using the recommendation application.

---

## 6. Verify ChromaDB

Run:

```powershell
docker run --rm `
  --env-file .env `
  -v smart-librarian-chroma:/app/chroma_db `
  smart-librarian python -c "from rag import collection; print('Books in ChromaDB:', collection.count())"
```

Expected result:

```text
Books in ChromaDB: 10
```

---

## 7. Run the Streamlit Application

Run:

```powershell
docker run --rm `
  -p 8501:8501 `
  --env-file .env `
  -v smart-librarian-chroma:/app/chroma_db `
  smart-librarian
```

Open the application in a browser:

```text
http://localhost:8501
```

---

# CLI Testing

The recommendation system can also be tested without Streamlit.

Run:

```powershell
docker run --rm -it `
  --env-file .env `
  -v smart-librarian-chroma:/app/chroma_db `
  smart-librarian python app.py
```

The application will display:

```text
SMART LIBRARIAN
Type 'exit' to close the application.

What kind of book are you looking for?
```

Example:

```text
I want a dystopian novel about surveillance and social control.
```

A suitable recommendation is:

```text
1984
```

---

# Example Queries

### Dystopian fiction

```text
I want a dystopian novel about surveillance and social control.
```

Expected recommendation:

```text
1984
```

### Fantasy

```text
I want a fantasy adventure with a dragon.
```

Expected recommendation:

```text
The Hobbit
```

### Personal development

```text
I want a reflective book about destiny and self-discovery.
```

Expected recommendation:

```text
The Alchemist
```

### Romance

```text
I want a novel about love, relationships and overcoming prejudice.
```

Expected recommendation:

```text
Pride and Prejudice
```

---

# Testing the Summary Tool

Run:

```powershell
docker run --rm smart-librarian python tools.py
```

The application should return the complete English summary for:

```text
1984
```

---

# Testing Semantic Retrieval

Run:

```powershell
docker run --rm `
  --env-file .env `
  -v smart-librarian-chroma:/app/chroma_db `
  smart-librarian python -c "from rag import search_books; results=search_books('freedom and social control', 3); [print(r['title']) for r in results]"
```

`1984` should appear among the most relevant results.

---

# Application Flow

```text
User
 |
 | Text or Voice
 v
Speech-to-Text
 |
 v
Content Moderation
 |
 v
OpenAI Embedding
 |
 v
ChromaDB
 |
 | Semantic Search
 v
Top Relevant Books
 |
 v
GPT-4.1 Mini
 |
 | Book Selection
 v
Tool Calling
 |
 v
get_summary_by_title()
 |
 v
Complete Summary
 |
 +--------------------+
 |                    |
 v                    v
Image Generation   Text-to-Speech
 |                    |
 v                    v
Artwork             Audio
 |
 v
Streamlit Interface
```

---

# Security

The OpenAI API key is stored in:

```text
.env
```

The `.env` file is excluded from Git using `.gitignore`.

API keys should never be committed to source control.

---

# Docker

The project runs inside a Docker container, which makes the environment reproducible and avoids dependencies on the local Python installation.

The container includes:

* Python
* pip
* Streamlit
* OpenAI SDK
* ChromaDB
* all project dependencies

ChromaDB data is persisted using the Docker volume:

```text
smart-librarian-chroma
```

---

# Summary

Smart Librarian demonstrates the integration of:

* Retrieval-Augmented Generation
* semantic vector search
* OpenAI embeddings
* ChromaDB
* conversational AI
* function/tool calling
* content moderation
* image generation
* text-to-speech
* speech-to-text
* Streamlit
* Docker

The result is an interactive AI reading assistant capable of understanding natural-language preferences and recommending relevant books from a curated collection.
