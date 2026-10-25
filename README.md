# Documind

Documind is an assistant tool that answers questions regarding company documents. We upload a document, ask a question in plain English and it finds the relevant part of the document.


## Current Status

Working:
1. Upload a pdf through API
2. The text is split into chunks and saved in SQLite
3. Each chunk is conerted into embedding and stored in Chroma DB
4. A search endpoint returns the chunks closest to the questin that we asked

Still to do:
1. Generate a written answer using LLm, with citations
2. React web page
3. Docker setup, tests and CI

## How it works

PDF -> text -> chunks (500 characters, 100 overlap) -> SQLite
Chunks -> embeddings (all-MiniLM-L6-v2) -> ChromaDB
Question -> embedding -> closest chunks in ChromaDB

##Tech used
Python, FastAPI, SQLite, ChromaDB, sentence-transformers

## How to run

```
python -m venv venv
venv\Scripts\activate
pip install -r backend\requirements.txt
cd backend
uvicorn app.main:app --reload
```

Then open http://127.0.0.1:8000/docs to try the endpoints.
The first run downloads the embedding model, so it takes a little longer

## Endpoints

- GET /health : checks that the server is running
- POST /upload : upload a PDF
- GET /search?q=your question&n=3 : returns the n closest chunks

## Sample documents
The sample_docs folder has two made-up company PDFs for testing.