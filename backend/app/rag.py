from app.vector_store import search
from app.llm import ask_llm
from app.database import get_filename

CUTOFF = 1.35
SOURCE_CUTOFF = 1.1
NOT_FOUND = "Could not find an answer in the documents"

def answer_question(q, n=3):
    results = search(q, n)
    distances = results["distances"][0]
    best = distances[0]

    if best > CUTOFF:
        return{"question" : q, "answer" : NOT_FOUND, "sources" : [], "best_distance" : best}

    chunks = []
    sources = []
    for text, dist, meta in zip(results["documents"][0], distances, results["metadatas"][0]):
        if dist > SOURCE_CUTOFF and len(chunks) > 0:
            continue
        chunks.append(text)
        sources.append({
            "filename" : get_filename(meta["document_id"]),
            "chunk_index" : meta["chunk_index"],
            "distance" : dist
        })

    answer = ask_llm(q, chunks)
    return {"question" : q, "answer" : answer, "sources" : sources, "best_distance" : best}
