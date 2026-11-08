from pathlib import Path
from app import database, rag
from app.rag import NOT_FOUND

HANDBOOK = Path(__file__).resolve().parent.parent.parent / "sample_docs" / "Meridian_Works_Employee_Policy_Handbook.pdf"


def upload_handbook(client):
    with open(HANDBOOK, "rb") as f:
        return client.post("/upload", files={"file": (HANDBOOK.name, f, "application/pdf")})


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_upload_rejects_non_pdf(client):
    response = client.post("/upload", files={"file": ("notes.txt", b"hello", "text/plain")})
    assert response.status_code == 400


def test_upload_pdf_then_duplicate(client):
    first = upload_handbook(client)
    assert first.status_code == 200
    assert first.json()["message"] == "uploaded"
    second = upload_handbook(client)
    assert second.json()["message"] == "already uploaded"


def test_search_finds_hotel_chunk(client):
    upload_handbook(client)
    response = client.get("/search", params={"q": "What is the hotel limit in metro cities?"})
    matches = response.json()["matches"]
    assert len(matches) == 3
    assert "4,500" in matches[0]["text"]


def test_query_gives_answer_with_sources(client):
    upload_handbook(client)
    response = client.get("/query", params={"q": "What is the hotel limit in metro cities?"})
    data = response.json()
    assert data["answer"] == "fake answer"
    assert len(data["sources"]) >= 1
    assert data["sources"][0]["filename"] == HANDBOOK.name


def test_query_not_found_skips_the_llm(client, monkeypatch):
    def fail(question, chunks):
        raise Exception("the LLM should not be called")
    monkeypatch.setattr(rag, "ask_llm", fail)

    upload_handbook(client)
    response = client.get("/query", params={"q": "What is the office dress code?"})
    data = response.json()
    assert data["answer"] == NOT_FOUND
    assert data["sources"] == []


def test_query_is_logged(client):
    upload_handbook(client)
    client.get("/query", params={"q": "What is the hotel limit in metro cities?"})
    conn = database.get_connection()
    rows = conn.execute("SELECT question, answer FROM queries").fetchall()
    conn.close()
    assert len(rows) == 1
    assert rows[0]["answer"] == "fake answer"