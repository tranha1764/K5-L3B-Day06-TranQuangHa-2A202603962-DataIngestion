"""
Script trích xuất Chapter 1 & Chapter 2 từ OpenStax College Success
và tự động tạo file manifest.json đạt chuẩn GUIDE.md và RUBRIC.md.
Xuất file duy nhất vào thư mục data/ ở cấp root theo cấu trúc SUBMISSION.md.
"""
from pathlib import Path
import json
from pypdf import PdfReader, PdfWriter


def prepare_corpus():
    root_dir = Path(__file__).resolve().parents[2]
    starter_dir = Path(__file__).resolve().parents[1]
    
    input_pdf = starter_dir / "data" / "college-success.pdf"
    if not input_pdf.exists():
        input_pdf = root_dir / "data" / "college-success.pdf"

    output_pdf = root_dir / "data" / "corpus.pdf"
    manifest_path = root_dir / "data" / "manifest.json"

    if not input_pdf.exists():
        print(f"Lỗi: Không tìm thấy file {input_pdf}")
        return

    reader = PdfReader(str(input_pdf))
    total_pages = len(reader.pages)
    print(f"Tổng số trang sách gốc: {total_pages}")

    # Phạm vi Chapter 1 & 2: Trang vật lý 17 (index 16) đến trang vật lý 74 (index 73)
    start_idx = 16  # Trang vật lý 17 (Chapter 1 Exploring College)
    end_idx = 74    # Trang vật lý 74 (kết thúc Chapter 2 The Truth About Learning Styles)

    writer = PdfWriter()
    page_records = []

    for idx in range(start_idx, end_idx):
        page = reader.pages[idx]
        text = page.extract_text() or ""
        char_count = len(text.strip())
        physical_page = idx + 1
        
        # Metadata theo chương
        chapter = "Chapter 1" if physical_page <= 40 else "Chapter 2"
        section_title = "Exploring College" if chapter == "Chapter 1" else "Knowing Yourself as a Learner"

        writer.add_page(page)
        corpus_page_index = len(writer.pages)  # 1..58

        page_records.append({
            "corpus_page": corpus_page_index,
            "original_pdf_page": physical_page,
            "chapter": chapter,
            "section_title": section_title,
            "char_count": char_count
        })

    # Lưu corpus.pdf duy nhất vào root data/
    with open(output_pdf, "wb") as f:
        writer.write(f)

    # Lập manifest.json theo quy chuẩn GUIDE.md và SUBMISSION.md
    manifest = {
        "source_id": "openstax_college_success_ch1_ch2",
        "title": "College Success - Chapters 1 & 2",
        "author": "Amy Baldwin et al.",
        "publisher": "OpenStax, Rice University",
        "source_path_or_url": "https://openstax.org/details/books/college-success",
        "license_or_permission": "Creative Commons Attribution 4.0 International (CC BY 4.0)",
        "accessed_at": "2026-11-14",
        "total_content_pages": len(writer.pages),
        "page_selection_rule": "Physical pages 17 to 74 covering Chapter 1 (Exploring College) and Chapter 2 (Knowing Yourself as a Learner). Covers, table of contents, and preface excluded.",
        "filter_fields": {
            "chapter": ["Chapter 1", "Chapter 2"]
        },
        "pages": page_records
    }

    # Ghi manifest duy nhất vào root data/
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    print(f"-> Đã tạo {output_pdf} thành công với {len(writer.pages)} trang nội dung hữu ích.")
    print(f"-> Đã tạo {manifest_path} ghi nhận đầy đủ bản quyền và số trang.")


if __name__ == "__main__":
    prepare_corpus()
