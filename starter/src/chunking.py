"""Implement fixed-size and structure-aware chunking."""
from .models import Chunk, DocumentPage


def fixed_size(page: DocumentPage, size: int = 500, overlap: int = 50) -> list[Chunk]:
    """Split text into overlapping windows and retain page metadata."""
    text = page.text
    if not text:
        return []

    chunks: list[Chunk] = []
    start = 0
    step = max(1, size - overlap)
    idx = 0

    while start < len(text):
        end = min(len(text), start + size)
        chunk_text = text[start:end].strip()
        if chunk_text:
            chunk_id = f"{page.document_id}_p{page.page:02d}_fix_{idx:02d}"
            chunks.append(Chunk(
                chunk_id=chunk_id,
                document_id=page.document_id,
                source=page.source,
                page=page.page,
                text=chunk_text,
                metadata=dict(page.metadata)
            ))
            idx += 1
        if end >= len(text):
            break
        start += step

    return chunks

def by_paragraph(page: DocumentPage, max_size: int = 600) -> list[Chunk]:
    """Group paragraphs, split oversized paragraphs and retain metadata."""
    raw_paras = page.text.split("\n\n")
    paragraphs = [p.strip() for p in raw_paras if p.strip()]

    if not paragraphs:
        return []

    chunks: list[Chunk] = []
    current_para = ""
    idx = 0

    for p in paragraphs:
        if len(p) > max_size:
            if current_para:
                chunks.append(Chunk(
                    chunk_id=f"{page.document_id}_p{page.page:02d}_para_{idx:02d}",
                    document_id=page.document_id,
                    source=page.source,
                    page=page.page,
                    text=current_para.strip(),
                    metadata=dict(page.metadata)
                ))
                idx += 1
                current_para = ""

            p_start = 0
            while p_start < len(p):
                p_end = min(len(p), p_start + max_size)
                chunk_piece = p[p_start:p_end].strip()
                if chunk_piece:
                    chunks.append(Chunk(
                        chunk_id=f"{page.document_id}_p{page.page:02d}_para_{idx:02d}",
                        document_id=page.document_id,
                        source=page.source,
                        page=page.page,
                        text=chunk_piece,
                        metadata=dict(page.metadata)
                    ))
                    idx += 1
                if p_end >= len(p):
                    break
                p_start += (max_size - 50)
        elif len(current_para) + len(p) + 2 <= max_size:
            current_para = f"{current_para}\n\n{p}".strip() if current_para else p
        else:
            chunks.append(Chunk(
                chunk_id=f"{page.document_id}_p{page.page:02d}_para_{idx:02d}",
                document_id=page.document_id,
                source=page.source,
                page=page.page,
                text=current_para.strip(),
                metadata=dict(page.metadata)
            ))
            idx += 1
            current_para = p

    if current_para:
        chunks.append(Chunk(
            chunk_id=f"{page.document_id}_p{page.page:02d}_para_{idx:02d}",
            document_id=page.document_id,
            source=page.source,
            page=page.page,
            text=current_para.strip(),
            metadata=dict(page.metadata)
        ))

    return chunks
