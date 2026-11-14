"""Pipeline runner executing Strategies A, B, and C with full benchmarking."""
import json
import os
import sys
import time
from pathlib import Path
from dotenv import load_dotenv

# Thêm thư mục starter vào sys.path để Python nhận diện trọn vẹn package src
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.ingestion import load_pdf
from src.chunking import fixed_size, by_paragraph
from src.embeddings import MyEmbedder
from src.store import PgVectorStore
from src.evaluation import evaluate_query, summarize


def main() -> None:
    # 1. Khởi tạo đường dẫn và môi trường
    env_path = Path(__file__).resolve().parents[1] / ".env"
    load_dotenv(env_path)
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise ValueError("DATABASE_URL not found in .env")

    root_dir = Path(__file__).resolve().parents[2]
    corpus_pdf = root_dir / "data" / "corpus.pdf"
    benchmark_file = root_dir / "benchmark" / "benchmark.json"
    results_dir = root_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    print("====================================================")
    print("   BẮT ĐẦU CHẠY PIPELINE BENCHMARK (DAY 06)         ")
    print("====================================================")

    # 2. Nạp Corpus và Benchmark
    pages = load_pdf(corpus_pdf, document_id="college_success", source="openstax_college_success_ch1_ch2")
    print(f"-> Đã nạp thành công {len(pages)} trang từ {corpus_pdf}")

    with open(benchmark_file, "r", encoding="utf-8") as f:
        benchmark_queries = json.load(f)
    print(f"-> Đã nạp {len(benchmark_queries)} câu hỏi benchmark (15 dev / 5 test)")

    # 3. Khởi tạo Embedder và Vector Store
    embedder = MyEmbedder()
    store = PgVectorStore(database_url=database_url, dimensions=embedder.dimensions)
    store.create_schema()
    print("-> Đã khởi tạo schema pgvector trong database thành công.")

    # 4. Định nghĩa 3 chiến lược
    chunks_a = []
    for p in pages:
        chunks_a.extend(fixed_size(p, size=500, overlap=50))

    chunks_b = []
    for p in pages:
        chunks_b.extend(by_paragraph(p, max_size=600))
    
    # Chiến lược C dùng chung chunk với B để so sánh có kiểm soát (chỉ khác lọc metadata)
    chunks_c = chunks_b

    strategies = [
        {"name": "A", "chunks": chunks_a, "use_filter": False, "desc": "Fixed-size (500, overlap 50)"},
        {"name": "B", "chunks": chunks_b, "use_filter": False, "desc": "By-paragraph (max 600, no filter)"},
        {"name": "C", "chunks": chunks_c, "use_filter": True, "desc": "By-paragraph (max 600 + metadata filter)"}
    ]

    all_summaries = {}

    for strat in strategies:
        s_name = strat["name"]
        print(f"\n--- Đang xử lý Chiến lược {s_name}: {strat['desc']} ---")
        
        start_time = time.time()
        # Chiến lược A và B cần tạo embedding và nạp vào DB
        # Chiến lược C tái sử dụng vector store của B vì cùng chunking
        if s_name in ("A", "B"):
            print(f"-> Đang tạo embedding ({embedder.model_name}) cho {len(strat['chunks'])} chunks của Chiến lược {s_name}...")
            texts = [c.text for c in strat["chunks"]]
            vectors = embedder.embed_documents(texts)
            print(f"-> Đang lưu {len(vectors)} vectors vào PostgreSQL...")
            store.upsert(strategy=s_name, chunks=strat["chunks"], vectors=vectors)
        elif s_name == "C":
            print("-> Chiến lược C tái sử dụng index của B, kích hoạt metadata filter.")

        ingest_duration = round(time.time() - start_time, 2)

        # Chạy benchmark truy xuất 20 câu hỏi
        print("-> Đang truy xuất top-3 cho 20 câu hỏi...")
        traces = []
        target_store_strategy = "B" if s_name == "C" else s_name

        for q in benchmark_queries:
            q_vec = embedder.embed_query(q["question"])
            filter_to_apply = q.get("filter") if strat["use_filter"] else None
            hits = store.search(strategy=target_store_strategy, query_vector=q_vec, top_k=3, filters=filter_to_apply)
            trace = evaluate_query(q, hits)
            traces.append(trace)

        # Lưu trace chi tiết vào results/ ở cấp root
        trace_file = results_dir / f"trace_strategy_{s_name}.json"
        with open(trace_file, "w", encoding="utf-8") as f:
            json.dump(traces, f, indent=2, ensure_ascii=False)

        summary = summarize(traces)
        summary["chunk_count"] = len(strat["chunks"])
        summary["duration_seconds"] = ingest_duration
        all_summaries[s_name] = summary

        print(f"Chiến lược {s_name} hoàn tất trong {ingest_duration}s:")
        print(f"  [Dev 15 câu]  - Hit@1: {summary['dev']['hit1']} ({summary['dev']['hit1_pct']}%) | Hit@3: {summary['dev']['hit3']} ({summary['dev']['hit3_pct']}%)")
        print(f"  [Test 5 câu]  - Hit@1: {summary['test']['hit1']} ({summary['test']['hit1_pct']}%) | Hit@3: {summary['test']['hit3']} ({summary['test']['hit3_pct']}%)")
        if strat["use_filter"]:
            print(f"  [Tuân thủ Filter] - Dev: {summary['dev']['filter_compliance']} | Test: {summary['test']['filter_compliance']}")

    # 5. Xuất tóm tắt kết quả
    summary_file = results_dir / "benchmark_summary.json"
    with open(summary_file, "w", encoding="utf-8") as f:
        json.dump(all_summaries, f, indent=2, ensure_ascii=False)

    print("\n====================================================")
    print("   HOÀN TẤT CHẠY BENCHMARK TOÀN BỘ 3 CHIẾN LƯỢC!   ")
    print(f"-> Đã lưu các file trace tại: {results_dir}")
    print("====================================================")


if __name__ == "__main__":
    main()
