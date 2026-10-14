
from pathlib import Path
from pypdf import PdfReader


def load_pdf(pdf_path: str) -> list[dict]:
    """
    Extract text from a building bye-laws PDF.
    Returns text page by page so page references can be preserved.
    """
    path = Path(pdf_path)

    if not path.exists():
        raise FileNotFoundError(f"PDF not found: {path}")

    if path.suffix.lower() != ".pdf":
        raise ValueError("The input file must be a PDF.")

    reader = PdfReader(str(path))
    pages = []

    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""

        if text.strip():
            pages.append(
                {
                    "source": path.name,
                    "page": page_number,
                    "text": text.strip(),
                }
            )

    return pages
