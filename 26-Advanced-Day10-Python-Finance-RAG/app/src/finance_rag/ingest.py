from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Chunk:
    source: str
    section: str
    text: str


def _normalize_text(text: str) -> str:
    return " ".join(text.split())


def _split_by_section(content: str) -> list[tuple[str, str]]:
    sections: list[tuple[str, str]] = []
    current_title = "Introduction"
    current_lines: list[str] = []

    for line in content.splitlines():
        if line.startswith("## "):
            if current_lines:
                sections.append((current_title, "\n".join(current_lines).strip()))
                current_lines = []
            current_title = line.removeprefix("## ").strip()
            continue
        if line.startswith("# "):
            continue
        current_lines.append(line)

    if current_lines:
        sections.append((current_title, "\n".join(current_lines).strip()))

    return [(title, text) for title, text in sections if text]


def _split_paragraphs(section_text: str, max_chars: int = 280) -> list[str]:
    chunks: list[str] = []
    paragraph = " ".join(line.strip() for line in section_text.splitlines() if line.strip())
    if not paragraph:
        return chunks

    while len(paragraph) > max_chars:
        split_point = paragraph.rfind(". ", 0, max_chars)
        if split_point == -1:
            split_point = paragraph.rfind(" ", 0, max_chars)
        if split_point == -1:
            split_point = max_chars
        piece = paragraph[: split_point + 1].strip()
        if piece:
            chunks.append(piece)
        paragraph = paragraph[split_point + 1 :].strip()

    if paragraph:
        chunks.append(paragraph)
    return chunks


def load_chunks(corpus_dir: Path) -> list[Chunk]:
    if not corpus_dir.exists() or not corpus_dir.is_dir():
        raise FileNotFoundError(f"Corpus directory not found: {corpus_dir}")

    all_chunks: list[Chunk] = []
    for file_path in sorted(corpus_dir.glob("*.md")):
        content = file_path.read_text(encoding="utf-8")
        for section, text in _split_by_section(content):
            for paragraph in _split_paragraphs(text):
                normalized = _normalize_text(paragraph)
                if normalized:
                    all_chunks.append(
                        Chunk(
                            source=file_path.name,
                            section=section,
                            text=normalized,
                        )
                    )
    if not all_chunks:
        raise ValueError("No chunks were created from corpus files.")
    return all_chunks
