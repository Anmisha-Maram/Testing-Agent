"""Minimal text ingestion helpers for the QA RAG Agent MVP."""

from pathlib import Path


def read_text_file(file_path: str) -> str:
    """Read UTF-8 text from a file and raise clear errors for invalid input."""
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Input file was not found: {file_path}")

    if not path.is_file():
        raise ValueError(f"Provided path is not a file: {file_path}")

    content = path.read_text(encoding="utf-8")
    if not content.strip():
        raise ValueError(f"Input file is empty: {file_path}")

    return content
