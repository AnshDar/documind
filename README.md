# Documind
![Tests](https://github.com/AnshDar/documind/actions/workflows/tests.yml/badge.svg)
Documind is an assistant tool that answers questions regarding company documents. We upload a document, ask a question in plain English and it finds the relevant part of the document.


## Current status

Working:
- Upload a PDF through the web page or the API
- The text is split into chunks and saved in SQLite
- Each chunk is converted into an embedding and stored in ChromaDB
- Ask a question on the web page and get an answer written by an LLM, based only on the matching parts of the documents
- The answer lists the file and chunk it came from
- If the documents do not contain the answer, it says so
- Every question and answer is saved in SQLite
- 11 automated tests (pytest)

## How it works

PDF -> text -> chunks (500 characters, 100 overlap) -> SQLite
Chunks -> embeddings (all-MiniLM-L6-v2) -> ChromaDB
Question -> embedding -> closest chunks in ChromaDB
Close enough chunks + question -> LLM (Groq) -> answer with sources
Question and answer -> saved in SQLite

If even the closest chunk is too far from the question, the LLM is not called and the answer is "Could not find an answer in the documents."

## Tech used
Python, FastAPI, SQLite, ChromaDB, sentence-transformers, Groq (LLM), React (Vite), pytest

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

Then start the backend:

```
cd backend
uvicorn app.main:app --reload
```

In a second terminal, start the web page:

```
cd frontend
npm install
npm run dev
```

Open http://localhost:5173 to use the app. The API pages are at http://127.0.0.1:8000/docs.
The first run downloads the embedding model, so it takes a little longer.

## Running with Docker

The project has a Dockerfile for the backend, a Dockerfile for the frontend, and a `docker-compose.yml` that starts both. On a machine with Docker:

1. Create `backend/.env` with your `GROQ_API_KEY`.
2. From the project folder, run `docker compose up --build`.
3. Open http://localhost:5173 for the page. The API is at http://localhost:8000.

Notes:

- The containers are built and started on every push by the GitHub Actions workflow, which checks that the backend and the page both respond. They have not been run on my own laptop, because Docker is not installed there.
- The frontend container runs the Vite development server. It is meant for demos, not for production.
- The database, search index and uploaded files live inside the backend container, so they are lost when the container is removed.

## Endpoints

- GET /health : checks that the server is running
- POST /upload : upload a PDF
- GET /search?q=your question&n=3 : returns the n closest chunks
- GET /query?q=your question&n=3 : returns an answer from the LLM, with the sources it used

## Sample documents
The sample_docs folder has two made-up company PDFs for testing.

## Testing
Automated tests (run from the backend folder):

```
python -m pytest
```

These use a temporary database and a fake LLM, so they need no API key and do not touch your real data.

To check answer quality on real documents, upload both PDFs from sample_docs and run:

```
python test_questions.py
```

It asks 20 questions (17 the documents can answer, 3 they cannot) and prints PASS or FAIL for each. This one calls the real LLM.

## Known limits

- Only text PDFs work. Scanned PDFs need OCR, which is not included.
- Tables in a PDF are read as plain lines of text, so a question about a table can come out less exact.
- Documents are cut into fixed 500-character chunks, so a sentence is sometimes split. The overlap between chunks makes up for most of this.
- The distance cut-offs (1.35 to answer, 1.1 to cite) were chosen using two small sample documents. Run `python test_questions.py` again after adding new documents.
- Every question sends the matching passages to the Groq service, so only documents that are allowed to leave the machine should be used.
- There are no user accounts. Anyone who can reach the app sees all uploaded documents.