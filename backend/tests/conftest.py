import os
os.environ.setdefault("GROQ_API_KEY", "test-key")

import uuid
import chromadb
import pytest
from fastapi.testclient import TestClient
from app import database, vector_store, rag, main


@pytest.fixture
def client(tmp_path, monkeypatch):
    monkeypatch.setattr(database, "DB_PATH", str(tmp_path / "test.db"))
    database.init_db()

    chroma = chromadb.EphemeralClient()
    monkeypatch.setattr(vector_store, "collection", chroma.create_collection(str(uuid.uuid4())))

    monkeypatch.setattr(main, "UPLOAD_DIR", str(tmp_path))
    monkeypatch.setattr(rag, "ask_llm", lambda question, chunks: "fake answer")

    return TestClient(main.app)
