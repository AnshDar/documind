import chromadb
from sentence_transformers import SentenceTransformer
from app.database import get_connection

model = SentenceTransformer('all-MiniLM-L6-v2')
client = chromadb.PersistentClient(path="chroma_data")
collection = client.get_or_create_collection("chunks")

def embed_document(doc_id):
    conn = get_connection()
    rows = conn.execute(
        "SELECT id, content, chunk_index FROM chunks WHERE document_id = ?", (doc_id,)
    ).fetchall()
    conn.close()

    ids = [str(row["id"]) for row in rows]
    texts = [row["content"] for row in rows]
    metas = [{"document_id": doc_id, "chunk_index" : row["chunk_index"]} for row in rows]
    vectors = model.encode(texts).tolist()

    collection.upsert(ids = ids, documents = texts, metadatas = metas, embeddings = vectors)

def search(question, n_results=3):
    question_vector = model.encode([question]).tolist()
    results = collection.query(query_embeddings=question_vector, n_results=n_results)
    return results

if __name__ == "__main__":
    results = search("What is the dress code?")
    for text, dist in zip(results["documents"][0], results["distances"][0]):
        print(dist)
        print(text)
        print("-----")