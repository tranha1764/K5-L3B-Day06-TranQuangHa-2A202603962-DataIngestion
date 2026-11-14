"""Read and normalize source data. TODO: implement functions."""
from pathlib import Path
import unicodedata
import re
from pypdf import PdfReader
from .models import DocumentPage

def load_pdf(path: Path, document_id: str, source: str) -> list[DocumentPage]:
    """Extract each physical page; keep its page number, source, and chapter metadata."""
    if not path.exists():
        raise FileNotFoundError(f"PDF not found: {path}")

    reader = PdfReader(str(path))
    pages: list[DocumentPage] = []
    empty_pages: list[int] = []

    for idx, page_obj in enumerate(reader.pages):
        page_num = idx + 1
        raw_text = page_obj.extract_text() or ""
        normalized = normalize_text(raw_text)

        if len(normalized) < 50:
            empty_pages.append(page_num)

        # Chapter 1: trang 1-24, Chapter 2: trang 25-58
        chapter = "Chapter 1" if page_num <= 24 else "Chapter 2"
        metadata = {
            "chapter": chapter,
            "char_count": len(normalized)
        }

        pages.append(DocumentPage(
            document_id=document_id,
            source=source,
            page=page_num,
            text=normalized,
            metadata=metadata
        ))

    if empty_pages:
        print(f"Log cảnh báo: các trang ít/không có text: {empty_pages}")
    else:
        print(f"Log: Đã nạp thành công {len(pages)} trang từ {path.name} (không có trang rỗng).")

    return pages

def normalize_text(text: str) -> str:
    """Normalize Unicode and whitespace without discarding useful structure."""
    if not text:
        return ""
    text = unicodedata.normalize("NFKC", text)
    text = re.sub(r'[\r\f\v]', '\n', text)
    lines = [re.sub(r'[ \t]+', ' ', line).strip() for line in text.split('\n')]
    cleaned = '\n'.join(lines)
    cleaned = re.sub(r'\n{3,}', '\n\n', cleaned)
    return cleaned.strip()
