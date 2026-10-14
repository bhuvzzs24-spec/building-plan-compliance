
from pathlib import Path

import chromadb


def build_vector_store(
    chunks: list[dict],
    persist_dir: str = "data/chroma_db",
) -> int:
    """Store text chunks and their source/page metadata in Chroma."""
    if not chunks:
        raise ValueError("No text chunks provided to index.")

    db_path = Path(persist_dir)
    db_path.mkdir(parents=True, exist_ok=True)

    client = chromadb.PersistentClient(path=str(db_path))
    collection = client.get_or_create_collection(
        name="building_bye_laws"
    )

    ids = []
    documents = []
    metadatas = []

    for i, chunk in enumerate(chunks):
        text = chunk.get("text", "").strip()
        if not text:
            continue

        source = str(chunk.get("source", "unknown"))
        page = chunk.get("page")
        chunk_id = f"{source}-page-{page}-chunk-{i}"

        ids.append(chunk_id)
        documents.append(text)
        metadatas.append({
            "source": source,
            "page": int(page) if page is not None else 0,
        })

    if not documents:
        raise ValueError("All supplied chunks were empty.")

    # Remove old chunks for these sources before inserting the current
    # version. This prevents obsolete chunks remaining after re-indexing.
    sources = sorted({metadata["source"] for metadata in metadatas})
    for source in sources:
        collection.delete(where={"source": source})

    collection.upsert(
        ids=ids,
        documents=documents,
        metadatas=metadatas,
    )

    return collection.count()
