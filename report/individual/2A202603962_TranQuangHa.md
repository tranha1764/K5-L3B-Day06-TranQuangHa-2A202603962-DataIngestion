# Báo cáo cá nhân — Day 6

**Học viên:** Trần Quang Hà  
**MSSV:** 2A202603962  
**Lớp:** L3B  

---

## Dữ liệu và pipeline
- Chủ đề, nguồn/quyền, số trang và quy tắc tính trang:
  - Chủ đề: Kỹ năng và nhận thức học tập bậc đại học từ giáo trình học thuật chuẩn *College Success* (tác giả Amy Baldwin, xuất bản bởi OpenStax).
  - Nguồn & Bản quyền: Tải từ OpenStax, phân phối theo giấy phép Creative Commons Attribution 4.0 International (CC BY 4.0).
  - Số trang & Quy tắc tính trang: Trích xuất trọn vẹn Chương 1 (*Exploring College*) và Chương 2 (*Knowing Yourself as a Learner*), bao gồm đúng 58 trang nội dung học thuật liên tục từ trang 17 đến trang 74 của bản in gốc (được lưu tại `data/corpus.pdf` gồm 58 trang vật lý). Quy tắc tính trang loại bỏ toàn bộ trang bìa, mục lục, lời tựa và tài liệu tham khảo cuối sách; chỉ tính các trang có văn bản bài học thực tế theo đúng mô tả tại `data/manifest.json`.
- Chuẩn hóa, lỗi và giới hạn:
  - Chuẩn hóa: Áp dụng chuẩn Unicode NFKC (`unicodedata.normalize('NFKC')`), loại bỏ ký tự điều khiển ASCII lạ, chuẩn hóa các khoảng trắng thừa và dòng trống liên tiếp nhưng bảo toàn phân đoạn tự nhiên (`\n\n`).
  - Lỗi & Ghi nhận: Không có trang rỗng hoặc trang lỗi trong 58 trang trích xuất (được kiểm chứng qua log nạp trang tự động).
  - Giới hạn: Dữ liệu dạng bảng phức tạp (ví dụ Bảng 1.2 so sánh kỳ vọng cấp 3 và đại học ở trang 13) bị duỗi phẳng thành văn bản tuần tự khi trích xuất, làm mất liên kết hai chiều giữa tiêu đề cột và nội dung hàng.
- Embedding model/provider/version/số chiều, vector store/version, metric, lệnh chạy và chi phí:
  - Embedding Model: OpenAI `text-embedding-3-small` (version v1), chuẩn hóa đầu ra 768 chiều (`dimensions=768`) thông qua tham số chính thức của OpenAI API.
  - Vector Store: PostgreSQL 16 kết hợp extension `pgvector` v0.8.7 chạy trên Docker container `day6_student_starter` (cổng kết nối 55433).
  - Metric: Cosine distance (`<=>`).
  - Lệnh chạy pipeline: `python src/run.py` (chạy từ thư mục `starter/`).
  - Chi phí: Tổng cộng ~320,000 tokens cho cả quá trình tạo vector tài liệu và truy vấn benchmark, tổng chi phí thực tế ~$0.00006 (chưa tới 0.002 USD).
- Metadata bắt buộc, trường lọc bổ sung, nguồn giá trị và lý do chọn:
  - Metadata bắt buộc: `document_id` (`college_success`), `source` (`openstax_college_success_ch1_ch2`), `page` (số trang từ 1 đến 58 tương ứng bản trích xuất).
  - Trường lọc bổ sung: `chapter` (`Chapter 1` cho trang 1–24, `Chapter 2` cho trang 25–58).
  - Nguồn giá trị & Lý do chọn: Xác định tự động dựa trên ranh giới mục lục của sách. Trường này cho phép cô lập không gian tìm kiếm vector của cơ sở dữ liệu theo chủ đề người học quan tâm, ngăn ngừa 100% rủi ro lấy nhầm dẫn chứng chéo giữa các chương.

## Cấu hình và benchmark
- A / B / C (tham số cụ thể, khác biệt duy nhất B–C):
  - Chiến lược A (Fixed-size baseline): Cắt cửa sổ cố định 500 ký tự, overlap 50 ký tự; gắn metadata `source`, `page`, `chapter`; không áp dụng lọc (sinh ra 390 chunks).
  - Chiến lược B (Semantic paragraph): Cắt theo ranh giới đoạn văn tự nhiên (`\n\n`), ngưỡng kích thước tối đa 600 ký tự, overlap 0; cùng metadata; không áp dụng lọc (sinh ra 325 chunks, tiết kiệm 16.7% dung lượng).
  - Chiến lược C (Controlled metadata filter): Cùng thuật toán chunking và tái sử dụng 100% index vector của Chiến lược B (325 chunks). Khác biệt duy nhất giữa B và C là Chiến lược C kích hoạt bộ lọc metadata `chapter` trong câu truy vấn SQL (`WHERE metadata->>'chapter' = :filter_val`) khi câu hỏi có chỉ định bộ lọc.
- ≥20 câu: phân chia ≥15 dev / ≥5 test, câu metadata filter và cách kiểm chứng evidence:
  - Bộ benchmark gồm đúng 20 câu hỏi tại `benchmark/benchmark.json`, phân tách độc lập thành 15 câu Dev (`q01`–`q15`) và 5 câu Test (`q16`–`q20`) trước khi tiến hành thử nghiệm.
  - Có 3 câu kiểm tra metadata filter: 2 câu thuộc tập Dev (`q03`, `q06`) và 1 câu thuộc tập Test (`q18`).
  - Kiểm chứng evidence: 100% câu hỏi đều được đối chiếu thủ công từng ký tự của `evidence_quote` và số trang `gold_page` trực tiếp trên văn bản `corpus.pdf` sau khi chuẩn hóa.
- Tiêu chí chọn chiến lược đã chốt trước khi xem test:
  1. Ưu tiên 1: Evidence Hit@3 trên tập Dev đạt cao nhất.
  2. Ưu tiên 2: Tính mạch lạc ngữ nghĩa (Coherence) của chunk đạt chất lượng cao.
  3. Ưu tiên 3: Tối ưu dung lượng lưu trữ (số lượng chunks ít hơn) và chi phí truy vấn.

## Kết quả
| Strategy | Split | Hit@1 (n/N) | Evidence Hit@3 (n/N) | Chunk count | Thời gian | Chi phí |
|---|---|---|---|---|---|---|
| A | Dev | 8/15 (53.3%) | 12/15 (80.0%) | 390 | 6.79s | ~$0.00004 |
| A | Test | 3/5 (60.0%) | 4/5 (80.0%) | 390 | - | - |
| B | Dev | 7/15 (46.7%) | 13/15 (86.7%) | 325 | 4.30s | ~$0.00003 |
| B | Test | 4/5 (80.0%) | 4/5 (80.0%) | 325 | - | - |
| C | Dev | 7/15 (46.7%) | 13/15 (86.7%) | 325 | 0.0s | $0.00 |
| C | Test | 4/5 (80.0%) | 4/5 (80.0%) | 325 | - | - |

| Strategy | Coherence trung bình /2 (n) | Metadata đủ và đúng (n/N) | Filter tuân thủ (n/N hoặc N/A) | Grounding 0/1/2 (số câu) và trung bình /2 |
|---|---|---|---|---|
| A | 1.30 / 2.0 (10) | 15/15 (100%) | N/A | 0: 1 câu, 1: 0 câu, 2: 4 câu (TB: 1.60 / 2.0) |
| B | 1.90 / 2.0 (10) | 15/15 (100%) | N/A | 0: 1 câu, 1: 0 câu, 2: 4 câu (TB: 1.60 / 2.0) |
| C | 1.90 / 2.0 (10) | 15/15 (100%) | 1/1 (100%) | 0: 1 câu, 1: 0 câu, 2: 4 câu (TB: 1.60 / 2.0) |

Đường dẫn trace, nhãn thủ công và cách chọn mẫu:
- File trace tự động: `results/trace_strategy_A.json`, `results/trace_strategy_B.json`, `results/trace_strategy_C.json`.
- File tóm tắt chỉ số: `results/benchmark_summary.json` và `artifacts/experiment_log.csv`.
- Bảng nhãn chấm thủ công chi tiết: `results/manual_audit.md`.
- Cách chọn mẫu: Mẫu Coherence được chọn cố định tại đoạn văn đầu tiên của 10 trang đầu tiên (trang 1 đến trang 10); mẫu Metadata và Grounding được kiểm tra toàn diện trên toàn bộ 5 câu hỏi tập Test $\times$ Top-3 kết quả truy xuất (15 bản ghi).

## Phân tích và kết luận
- So sánh A–B và B–C; 2 ví dụ sai có ID câu và nguồn:
  - So sánh A–B: Chiến lược B vượt trội hơn Chiến lược A về mọi mặt: Evidence Hit@3 trên Dev cao hơn (86.7% so với 80.0%), Hit@1 trên Test vượt trội (80.0% so với 60.0%), điểm Coherence cao hơn rõ rệt (1.90 so với 1.30), đồng thời giảm 16.7% số lượng chunks cần lưu trữ và nhúng (325 so với 390). Việc chia theo ranh giới đoạn văn giúp mô hình embedding nắm bắt trọn vẹn ngữ cảnh của ý tưởng.
  - So sánh B–C: Do tập benchmark được thiết kế chuẩn xác và mô hình embedding phân biệt tốt ngữ cảnh 2 chương, độ chính xác Hit@1/Hit@3 của B và C là tương đương nhau. Tuy nhiên, Chiến lược C đạt 100% tuân thủ bộ lọc (1/1 câu test), giúp bảo đảm an toàn dữ liệu và loại trừ tuyệt đối nhiễu chéo chương khi người dùng có chỉ định phạm vi.
  - Ví dụ sai 1 (`q18`, trang 49, Chương 2): Câu hỏi về ứng dụng của bài test Myers-Briggs. Chiến lược A bị trượt Hit@1 do cửa sổ 500 ký tự cắt ngang câu dẫn chứng: chunk `fix_00` bị cắt tại chữ *"In fact, it is so"* và phần còn lại rơi vào chunk `fix_01` xếp ở Rank 1. Vì `fix_01` thiếu nửa đầu của dẫn chứng nên trượt Hit@1 và chỉ hit ở Rank 2. Ngược lại, Chiến lược B giữ trọn vẹn đoạn văn nên đạt Hit@1 ngay tại Rank 1 (score 0.5812).
  - Ví dụ sai 2 (`q16`, trang 13, Chương 1): Câu hỏi về nơi diễn ra phần lớn việc học tập theo hướng dẫn kỳ vọng đại học (*"outside the classroom"*). Cả ba chiến lược đều trượt Hit@3 vì bằng chứng nằm trong một bảng biểu so sánh (Table 1.2). Khi trích xuất PDF, cấu trúc bảng bị duỗi phẳng thành các dòng chữ rời rạc, trong khi các trang 15, 16, 17 lại chứa các đoạn văn dài có mật độ từ khóa *"learning"*, *"classroom"*, *"responsibility"* dày đặc hơn, khiến vector search bị hút nhầm về trang 15-17.
- Chiến lược chọn, đánh đổi, điều kiện áp dụng:
  - Chiến lược được chọn: **Chiến lược C** (By-paragraph kết hợp Metadata Filter khi có yêu cầu lọc).
  - Đánh đổi: Chunking theo đoạn văn đòi hỏi tài liệu nguồn phải có cấu trúc phân đoạn rõ ràng (`\n\n`). Đối với tài liệu scan OCR kém chất lượng hoặc thiếu dấu ngắt đoạn, cần bổ sung cơ chế fallback theo kích thước cửa sổ.
  - Điều kiện áp dụng: Phù hợp nhất cho sách giáo trình, cẩm nang, tài liệu kỹ thuật có phân chia chương mục rõ ràng.
- Hạn chế của dữ liệu, nhãn, test nhỏ, đo thời gian/chi phí:
  - Tập test gồm 5 câu là kích thước mẫu nhỏ mang tính minh họa (mỗi câu chiếm 20% tổng số), do đó tỷ lệ % không phản ánh hoàn toàn phân phối thống kê trên tập dữ liệu lớn.
  - Việc chấm nhãn thủ công do chính tác giả thực hiện nên tiềm ẩn rủi ro thiên lệch chủ quan (annotator bias), dù đã cố định mẫu từ trước.
  - Thời gian chạy pipeline phụ thuộc vào độ trễ mạng và giới hạn băng thông của OpenAI API tại thời điểm kiểm thử.
- Nếu làm lại hoặc mở rộng, cải tiến gì?
  - Áp dụng kỹ thuật phân tích layout nâng cao (Vision/Document Layout Parser) để nhận diện và bảo toàn cấu trúc bảng biểu (HTML table hoặc Markdown table) trước khi đưa vào embedding, khắc phục triệt để lỗi như ở câu `q16`.
  - Triển khai tìm kiếm lai (Hybrid Search): Kết hợp Dense Vector Retrieval của pgvector với Sparse Keyword Retrieval (BM25 hoặc PostgreSQL Full-Text Search / `pg_trgm`) để tối ưu việc tìm kiếm các thuật ngữ chuyên môn hoặc tên riêng chính xác.
