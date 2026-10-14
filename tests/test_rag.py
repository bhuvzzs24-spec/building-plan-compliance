import pytest
from agents.rag.vector_store import build_vector_store
from agents.rag.pdf_loader import load_pdf

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




def test_loader_rejects_missing_pdf(tmp_path):
    missing_pdf = tmp_path / "missing.pdf"

    with pytest.raises(FileNotFoundError):
        load_pdf(str(missing_pdf))


def test_loader_rejects_non_pdf_file(tmp_path):
    text_file = tmp_path / "rules.txt"
    text_file.write_text("Synthetic test content", encoding="utf-8")

    with pytest.raises(ValueError, match="must be a PDF"):
        load_pdf(str(text_file))




def test_vector_store_upserts_chunks_without_duplicates(tmp_path):
    db_path = str(tmp_path / "chroma_db")
    chunks = [
        {
            "source": "synthetic_test.pdf",
            "page": 1,
            "text": "Synthetic passage about setbacks and road width."
        }
    ]

    first_count = build_vector_store(chunks, db_path)
    second_count = build_vector_store(chunks, db_path)

    assert first_count == 1
    assert second_count == 1
