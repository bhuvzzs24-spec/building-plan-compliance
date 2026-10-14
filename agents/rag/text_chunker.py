
def chunk_pages(
    pages: list[dict],
    chunk_size: int = 1000,
    overlap: int = 150,
) -> list[dict]:
    """Split PDF page text into chunks while preserving source and page."""

    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive")

    if overlap < 0 or overlap >= chunk_size:
        raise ValueError("overlap must be between 0 and chunk_size")

    chunks = []

    for page in pages:
        text = page.get("text", "").strip()
        if not text:
            continue

        start = 0
        while start < len(text):
            end = min(start + chunk_size, len(text))

            # Prefer ending at a word boundary.
            if end < len(text):
                boundary = text.rfind(" ", start, end)
                if boundary > start:
                    end = boundary

            chunk_text = text[start:end].strip()

            if chunk_text:
                chunks.append({
                    "source": page.get("source", "unknown"),
                    "page": page.get("page"),
                    "text": chunk_text,
                })

            if end >= len(text):
                break

            start = max(end - overlap, start + 1)

    return chunks
