
from pathlib import Path

from agents.rag.indexer import index_pdf


PDF_DIR = Path("data/bye_laws")
DB_DIR = "data/chroma_db"


def main():
    pdf_files = sorted(PDF_DIR.glob("*.pdf"))

    if not pdf_files:
        print(f"No PDF files found in {PDF_DIR.resolve()}")
        print("Add an official building bye-laws PDF, then run again.")
        return

    for pdf_path in pdf_files:
        try:
            result = index_pdf(str(pdf_path), DB_DIR)
            print(result)
        except Exception as exc:
            print(f"Failed to index {pdf_path.name}: {exc}")


if __name__ == "__main__":
    main()
