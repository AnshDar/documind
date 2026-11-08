from app.ingest import chunk_text

def test_short_text_is_one_chunk():
    chunks = chunk_text("hello world")
    assert chunks == ["hello world"]

def test_empty_text_gives_no_chunks():
    assert chunk_text("") == []

def test_long_text_is_split_into_chunks():
    chunks = chunk_text("a" * 1200)
    assert len(chunks) == 3
    assert len(chunks[0]) == 500
    assert len(chunks[2]) == 400

def test_chunks_overlap():
    text = "".join(str(i % 10) for i in range(1200))
    chunks = chunk_text(text)
    assert chunks[1][:100] == chunks[0][-100:]