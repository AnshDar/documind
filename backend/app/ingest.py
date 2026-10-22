from pypdf import PdfReader
from datetime import datetime
from app.database import get_connection
import os
from app.vector_store import embed_document

def read_pdf(path):
    reader = PdfReader(path)
    text = ""
    for page in reader.pages: 
        text += page.extract_text() + "\n"
    return text

def chunk_text(text, chunk_size = 500, overlap = 100):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        if end >= len(text):
            break
        start = end - overlap
    return chunks

def save_document(filename, chunks):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("INSERT INTO documents (filename, uploaded_at) VALUES (?, ?)", (filename, datetime.now().isoformat()))
    doc_id = cursor.lastrowid

    for i, chunk in enumerate(chunks):
        cursor.execute("INSERT INTO chunks (document_id, content, chunk_index) VALUES (?, ?, ?)", (doc_id, chunk, i))

    conn.commit()
    conn.close()
    return doc_id

def already_saved(filename):
    conn = get_connection()
    row = conn.execute("SELECT id FROM documents WHERE filename = ?", (filename,)).fetchone()
    conn.close()
    return row is not None

def ingest_file(path):
    filename = os.path.basename(path)
    if already_saved(filename):
        return None

    text = read_pdf(path)
    chunks = chunk_text(text)
    doc_id = save_document(filename, chunks)
    embed_document(doc_id)
    return doc_id         


# if __name__ == "__main__":
#      text = read_pdf("../sample_docs/Meridian_Works_Employee_Policy_Handbook.pdf")
#      chunks = chunk_text(text)
    #  print("Length of chunks :", len(chunks))
    #  print(chunks[0])
    #  print("-------")
    #  print(chunks[1]) 
    #  doc_id = save_document("Meridian_Works_Employee_Policy_Handbook.pdf", chunks)
    #  print("saved_document", doc_id, "with", len(chunks), "chunks")

if __name__ == "__main__":
    doc_id = ingest_file("../sample_docs/Meridian_Works_Employee_Policy_Handbook.pdf")
    print("doc id:", doc_id)