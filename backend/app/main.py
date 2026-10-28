import os
import shutil
from fastapi import FastAPI, UploadFile, File, HTTPException
from app.database import init_db, get_filename, save_query
from app.ingest import ingest_file
from app.vector_store import search
from app.rag import answer_question

app = FastAPI()
init_db()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/upload")
def upload_document(file: UploadFile = File(...)):
    filename = os.path.basename(file.filename)
    if not filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed.")
    path = os.path.join(UPLOAD_DIR, filename)
    with open(path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    doc_id = ingest_file(path)
    if doc_id is None:
        return {"message": "already uploaded", "filename": filename}
    return {"message": "uploaded", "filename": filename, "doc_id": doc_id}

@app.get("/search")
def search_documents(q : str, n : int = 3):
    results = search(q, n)

    matches = []
    for text, dist, meta in zip(results["documents"][0], results["distances"][0], results["metadatas"][0]):
        matches.append({
            "filename" : get_filename(meta["document_id"]),
            "chunk_index" : meta["chunk_index"],
            "distance" : dist,
            "text" : text
        })
    return{"question" : q, "matches" : matches}

@app.get("/query")
def query_documents(q : str, n : int = 3):
    result = answer_question(q, n)
    save_query(q, result["answer"])
    return result