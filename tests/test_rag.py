
from agents.rag.text_chunker import chunk_pages
from agents.rag.retriever import retrieve_clauses


def test_chunker_preserves_source_and_page():
    pages = [{
        "source": "sample_test.pdf",
        "page": 3,
        "text": "Synthetic text for testing source citations."
    }]

    chunks = chunk_pages(pages)

    assert chunks
    assert chunks[0]["source"] == "sample_test.pdf"
    assert chunks[0]["page"] == 3


def test_retriever_rejects_blank_question():
    try:
        retrieve_clauses(
            "   ",
            "data/chroma_validation_test",
            1
        )
    except ValueError as exc:
        assert "Question cannot be empty" in str(exc)
    else:
        raise AssertionError("Blank question should be rejected")


def test_retriever_rejects_zero_top_k():
    try:
        retrieve_clauses(
            "sample query",
            "data/chroma_validation_test",
            0
        )
    except ValueError as exc:
        assert "top_k must be at least 1" in str(exc)
    else:
        raise AssertionError("top_k=0 should be rejected")
