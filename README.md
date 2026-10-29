# Documind

Documind is an assistant tool that answers questions regarding company documents. We upload a document, ask a question in plain English and it finds the relevant part of the document.


## Current Status

Working:
1. Upload a PDF through the API
2. The text is split into chunks and saved in SQLite
3. Each chunk is converted into an embedding and stored in ChromaDB
4. Ask a question and get an answer written by an LLM, based only on the matching parts of the documents
5. The answer lists the file and chunk it came from
6. If the documents do not contain the answer, it says so
7. Every question and answer is saved in SQLite

Still to do:
1. React web page
2. Docker setup
3. Automated tests (pytest) and CI

## How it works

PDF -> text -> chunks (500 characters, 100 overlap) -> SQLite
Chunks -> embeddings (all-MiniLM-L6-v2) -> ChromaDB
Question -> embedding -> closest chunks in ChromaDB
Close enough chunks + question -> LLM (Groq) -> answer with sources
Question and answer -> saved in SQLite

If even the closest chunk is too far from the question, the LLM is not called and the answer is "Could not find an answer in the documents."

## Tech used
Python, FastAPI, SQLite, ChromaDB, sentence-transformers

## How to run
From the project folder:

```
python -m venv venv
venv\Scripts\activate
pip install -r backend\requirements.txt
```

Create a file called .env inside the backend folder with your Groq API key (free from console.groq.com):

```
GROQ_API_KEY=your-key-here
```

Then start the server:

```
cd backend
uvicorn app.main:app --reload
```

Then open http://127.0.0.1:8000/docs to try the endpoints.
The first run downloads the embedding model, so it takes a little longer.

## Endpoints

- GET /health : checks that the server is running
- POST /upload : upload a PDF
- GET /search?q=your question&n=3 : returns the n closest chunks

## Sample documents
The sample_docs folder has two made-up company PDFs for testing.