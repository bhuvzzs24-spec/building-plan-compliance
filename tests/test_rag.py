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
def test_end_to_end_pdf_index_retrieval_and_citation(tmp_path):
    from pathlib import Path
    from pypdf import PdfWriter
    from pypdf.generic import (
        DictionaryObject,
        DecodedStreamObject,
        NameObject,
    )
    from agents.rag.indexer import index_pdf
    from agents.rag.retriever import retrieve_clauses

    pdf_path = tmp_path / "synthetic_test.pdf"
    db_path = str(tmp_path / "chroma_db")

    writer = PdfWriter()
    page = writer.add_blank_page(width=612, height=792)

    font = DictionaryObject()
    font.update({
        NameObject("/Type"): NameObject("/Font"),
        NameObject("/Subtype"): NameObject("/Type1"),
        NameObject("/BaseFont"): NameObject("/Helvetica"),
    })
    fonts = DictionaryObject()
    fonts[NameObject("/F1")] = writer._add_object(font)
    resources = DictionaryObject()
    resources[NameObject("/Font")] = fonts
    page[NameObject("/Resources")] = resources

    stream = DecodedStreamObject()
    stream.set_data(
        b"BT /F1 12 Tf 72 720 Td "
        b"(Synthetic test passage about setbacks and road width.) Tj ET"
    )
    page[NameObject("/Contents")] = writer._add_object(stream)

    with pdf_path.open("wb") as file:
        writer.write(file)

    indexed = index_pdf(str(pdf_path), db_path)
    assert indexed["pages_extracted"] == 1
    assert indexed["chunks_created"] == 1

    results = retrieve_clauses(
        "setbacks and road width",
        db_path,
        3,
    )

    assert results
    assert "Synthetic test passage" in results[0]["text"]
    assert results[0]["source"] == "synthetic_test.pdf"
    assert results[0]["page"] == 1
