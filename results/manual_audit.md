# Bảng đánh giá và nhãn chấm thủ công (Manual Audit) — Day 06

**Họ tên:** Trần Quang Hà <br>
**MSSV:** 2A202603962 <br>
**Lớp:** L3B  
**Corpus:** OpenStax College Success (Chapters 1 & 2, 58 trang)

---

## 1. Đánh giá Chunk Coherence (Tính mạch lạc ngữ nghĩa)

- **Mẫu kiểm tra:** Chọn cố định đoạn mở đầu tại 10 trang đầu tiên (Trang 1 đến Trang 10 của `corpus.pdf`) trước khi xem điểm.
- **Thang điểm (theo GUIDE.md):**
  - `0`: Bị cắt giữa ý, thiếu chủ thể hoặc câu cụt làm người đọc không hiểu được.
  - `1`: Hiểu được một phần nội dung, nhưng thiếu ngữ cảnh hoặc bị cắt vế câu quan trọng.
  - `2`: Trọn vẹn ý tưởng, ngữ cảnh hoàn chỉnh, tự hiểu được độc lập.

| Vị trí | Trang nguồn | Chunk Strategy A (Fixed 500, overlap 50) | Điểm A | Chunk Strategy B (By-paragraph, max 600) | Điểm B | Nhận xét đối chiếu |
|:---:|:---:|---|:---:|---|:---:|---|
| 1 | Trang 1 | `college_success_p01_fix_00`: Bị cắt ngang ở cuối: *"because of the nature of the c"* | 1 | `college_success_p01_para_00`: Trọn vẹn đoạn giới thiệu nhập môn và thông tin mở đầu chương. | 2 | A bị cụt từ cuối câu; B giữ trọn đoạn văn. |
| 2 | Trang 2 | `college_success_p02_fix_00`: Cắt ngang câu chuyện sinh viên: *"after I navigated the c"* | 1 | `college_success_p02_para_00`: Giữ trọn câu chuyện của cựu sinh viên về việc tự bảo vệ quyền lợi. | 2 | A bị ngắt giữa chừng mạch tự sự; B hoàn chỉnh. |
| 3 | Trang 3 | `college_success_p03_fix_00`: Bắt đầu giữa chừng từ danh sách câu hỏi tự vấn, mất bối cảnh ban đầu. | 1 | `college_success_p03_para_00`: Toàn bộ đoạn mở đầu phần tự đánh giá bản thân (Self-Assessment). | 2 | B có câu mở đoạn định hướng rõ ràng cho bài tập. |
| 4 | Trang 4 | `college_success_p04_fix_00`: Cắt cụt danh sách 5 câu hỏi của phương pháp "Five Whys". | 1 | `college_success_p04_para_00`: Đoạn văn hoàn chỉnh giới thiệu kỹ thuật Five Whys và bối cảnh. | 2 | A cắt ngang giữa các bước hỏi; B giữ trọn vẹn ngữ cảnh. |
| 5 | Trang 5 | `college_success_p05_fix_00`: Cắt rời ví dụ minh họa về học ngành Speech Pathology. | 1 | `college_success_p05_para_01`: Đoạn ví dụ đầy đủ lời đối thoại và động lực học tập. | 2 | B giúp hiểu trọn vẹn lý do sinh viên chọn ngành. |
| 6 | Trang 6 | `college_success_p06_fix_00`: Giữ được ý chính định nghĩa mục tiêu ngắn hạn nhưng ngắt trước kết luận. | 1 | `college_success_p06_para_00`: Toàn bộ đoạn phân tích mục tiêu SMART và cách áp dụng. | 2 | A thiếu mệnh đề kết nối; B giữ nguyên logic. |
| 7 | Trang 7 | `college_success_p07_fix_00`: Đoạn văn ngắn nên vừa vặn trong 500 ký tự, trọn vẹn ý. | 2 | `college_success_p07_para_00`: Đoạn văn phân tích tầm quan trọng của việc lập kế hoạch học tập. | 2 | Cả hai cấu hình đều đạt tính toàn vẹn do đoạn gốc ngắn. |
| 8 | Trang 8 | `college_success_p08_fix_00`: Cắt giữa chừng câu danh ngôn của Nelson Mandela. | 1 | `college_success_p08_para_00`: Trọn vẹn câu danh ngôn và đoạn phân tích bình luận đi kèm. | 2 | A làm cụt danh ngôn; B giữ nguyên vẹn cảm xúc và ngữ cảnh. |
| 9 | Trang 9 | `college_success_p09_fix_00`: Vừa vặn trong 500 ký tự giới thiệu mục 1.2 "Understanding the Value of College". | 2 | `college_success_p09_para_00`: Đoạn mở đầu hoàn chỉnh của mục 1.2. | 2 | Cả hai đều đạt điểm tối đa. |
| 10 | Trang 10 | `college_success_p10_fix_00`: Vừa vặn trong 500 ký tự phân tích dữ liệu việc làm sinh viên. | 2 | `college_success_p10_para_00`: Đoạn văn phân tích thống kê thị trường lao động. | 2 | Cả hai đều mạch lạc. |

- **Điểm trung bình Coherence:**
  - **Chiến lược A:** $(1 + 1 + 1 + 1 + 1 + 1 + 2 + 1 + 2 + 2) / 10 = \mathbf{1.30 / 2.0}$ (Phân bổ: 0 câu mức 0, 7 câu mức 1, 3 câu mức 2).
  - **Chiến lược B:** $(2 + 2 + 2 + 2 + 2 + 2 + 2 + 2 + 2 + 2) / 10 = \mathbf{1.90 / 2.0}$ (Phân bổ: 0 câu mức 0, 1 câu mức 1, 9 câu mức 2).
- **Kết luận:** Chiến lược B vượt trội hoàn toàn về tính mạch lạc do không bao giờ cắt xẻ câu chữ lưng chừng, giúp embedding vector đại diện chuẩn xác cho toàn bộ ý niệm.

---

## 2. Đánh giá Metadata Usefulness (Độ hữu dụng của siêu dữ liệu)

- **Mẫu kiểm tra:** 5 câu hỏi tập Test $\times$ Top-3 kết quả truy xuất = **15 bản ghi**.
- **Tiêu chuẩn kiểm tra:** Mỗi bản ghi phải có đủ `source`, `page` chính xác khớp với số trang vật lý của sách, và trường bổ sung `chapter` khớp chính xác với chương nội dung.

| Query ID | Rank | Chunk ID | Source | Trang ghi nhận | Trang thực tế | Chapter ghi nhận | Chapter thực tế | Kết quả kiểm tra |
|:---:|:---:|:---|:---|:---:|:---:|:---:|:---:|:---:|
| `q16` | 1 | `college_success_p15_para_04` | openstax_college_success_ch1_ch2 | 15 | 15 | Chapter 1 | Chapter 1 | Đúng & Đủ |
| `q16` | 2 | `college_success_p17_para_02` | openstax_college_success_ch1_ch2 | 17 | 17 | Chapter 1 | Chapter 1 | Đúng & Đủ |
| `q16` | 3 | `college_success_p16_para_02` | openstax_college_success_ch1_ch2 | 16 | 16 | Chapter 1 | Chapter 1 | Đúng & Đủ |
| `q17` | 1 | `college_success_p15_para_00` | openstax_college_success_ch1_ch2 | 15 | 15 | Chapter 1 | Chapter 1 | Đúng & Đủ |
| `q17` | 2 | `college_success_p14_para_04` | openstax_college_success_ch1_ch2 | 14 | 14 | Chapter 1 | Chapter 1 | Đúng & Đủ |
| `q17` | 3 | `college_success_p14_para_03` | openstax_college_success_ch1_ch2 | 14 | 14 | Chapter 1 | Chapter 1 | Đúng & Đủ |
| `q18` | 1 | `college_success_p49_para_00` | openstax_college_success_ch1_ch2 | 49 | 49 | Chapter 2 | Chapter 2 | Đúng & Đủ |
| `q18` | 2 | `college_success_p49_para_01` | openstax_college_success_ch1_ch2 | 49 | 49 | Chapter 2 | Chapter 2 | Đúng & Đủ |
| `q18` | 3 | `college_success_p50_para_03` | openstax_college_success_ch1_ch2 | 50 | 50 | Chapter 2 | Chapter 2 | Đúng & Đủ |
| `q19` | 1 | `college_success_p26_para_00` | openstax_college_success_ch1_ch2 | 26 | 26 | Chapter 2 | Chapter 2 | Đúng & Đủ |
| `q19` | 2 | `college_success_p26_para_01` | openstax_college_success_ch1_ch2 | 26 | 26 | Chapter 2 | Chapter 2 | Đúng & Đủ |
| `q19` | 3 | `college_success_p39_para_01` | openstax_college_success_ch1_ch2 | 39 | 39 | Chapter 2 | Chapter 2 | Đúng & Đủ |
| `q20` | 1 | `college_success_p27_para_00` | openstax_college_success_ch1_ch2 | 27 | 27 | Chapter 2 | Chapter 2 | Đúng & Đủ |
| `q20` | 2 | `college_success_p27_para_01` | openstax_college_success_ch1_ch2 | 27 | 27 | Chapter 2 | Chapter 2 | Đúng & Đủ |
| `q20` | 3 | `college_success_p27_para_02` | openstax_college_success_ch1_ch2 | 27 | 27 | Chapter 2 | Chapter 2 | Đúng & Đủ |

- **Tỷ lệ Metadata đủ và đúng:** **15 / 15 (100.0%)**.
- **Tuân thủ bộ lọc (Filter Compliance):** Câu `q18` có filter `{"chapter": "Chapter 2"}`: cả 3 chunk ở top-3 của Chiến lược C đều mang `chapter = Chapter 2` $\rightarrow$ **1 / 1 (100.0%)**.
- **Phân tích vai trò và hạn chế:**
  - *Vai trò thực tế:* Metadata `chapter` đóng vai trò là tiền bộ lọc cứng trong SQL (`WHERE metadata->>'chapter' = :filter_val`), giúp cắt giảm hoàn toàn 50% không gian vector không liên quan, tăng tốc độ tính khoảng cách cosine và loại bỏ tuyệt đối rủi ro nhiễu chéo chương.
  - *Hạn chế:* Nếu người dùng đặt các câu hỏi tổng hợp liên chương (ví dụ so sánh phương pháp học ở Chapter 1 với lý thuyết nhận thức ở Chapter 2) hoặc hệ thống trích xuất filter bị sai, bộ lọc cứng sẽ vô tình loại bỏ luôn các bằng chứng quý giá ở chương còn lại.

---

## 3. Đánh giá Grounding Quality (Chất lượng bằng chứng truy xuất)

- **Mẫu kiểm tra:** 5 câu hỏi tập Test (`q16` đến `q20`).
- **Thang điểm (theo GUIDE.md):**
  - `0`: Không có bằng chứng hỗ trợ trả lời câu hỏi.
  - `1`: Có bằng chứng liên quan nhưng thiếu điều kiện hoặc ngữ cảnh cần thiết để trả lời đầy đủ.
  - `2`: Bằng chứng đầy đủ, chính xác, cho phép trả lời trọn vẹn và truy xuất nguồn tin cậy.

| Query ID | Câu hỏi | Gold Evidence Quote & Trang | Kết quả truy xuất Top-1 (Strategy B/C) | Điểm Grounding | Lý do chấm điểm chi tiết |
|:---:|---|---|---|:---:|---|
| `q16` | Where does most learning take place according to the college expectations guide? | *"In college, most learning happens outside the classroom."* (Trang 13) | `college_success_p15_para_04` (Trang 15): Bàn về việc tự theo dõi tiến độ học tập và luyện tập phương pháp học hiệu quả. | **0** | Top-3 rơi vào trang 15, 17, 16. Bằng chứng nằm ở Bảng 1.2 trang 13 không xuất hiện trong top-3, không đủ dữ liệu để trả lời. |
| `q17` | How do relationships typically change and expand for students during college? | *"relationships will expand to peer networks—not friends, but near-age peers or situational peers"* (Trang 15) | `college_success_p15_para_00` (Trang 15): Chứa trọn vẹn câu: *"your relationships will expand to peer networks—not friends, but near-age peers or situational peers..."* | **2** | Chứa chính xác và trọn vẹn dẫn chứng cùng ngữ cảnh mở rộng mạng lưới quan hệ hỗ trợ nghề nghiệp. |
| `q18` | In Chapter 2, how is the Myers-Briggs assessment described in terms of its application? | *"The Myers-Briggs system is one of the most popular personality tests... It has seen a great deal of use in the business world with testing seminars and presentations on group dynamics."* (Trang 49) | `college_success_p49_para_00` (Trang 49): Chứa trọn vẹn đoạn văn giới thiệu bài test Myers-Briggs và ứng dụng trong giới doanh nghiệp. | **2** | Bằng chứng đầy đủ 100%, trả lời chính xác cả tính phổ biến lẫn ứng dụng hội thảo nhóm. |
| `q19` | What did the former STEM student discover when switching to studying Russian? | *"Since I am now a humanities student studying Russian, I learned the hard way that you cannot study for everything the same way."* (Trang 26) | `college_success_p26_para_00` (Trang 26): Chứa đầy đủ lời tự sự của sinh viên Gabby Kennedy về sự khác biệt giữa học STEM và tiếng Nga. | **2** | Bằng chứng rõ ràng, trích xuất chính xác kết luận về việc không thể áp dụng cùng một cách học cho mọi môn. |
| `q20` | What ancient philosophical obsession led to modern learning theories? | *"We humans have been obsessed with how we learn and understand things since ancient times."* (Trang 27) | `college_success_p27_para_00` (Trang 27): Chứa nguyên văn câu mở đầu chương 2 về sự ám ảnh từ thời cổ đại đối với việc tiếp thu tri thức. | **2** | Cung cấp đầy đủ bối cảnh triết học cổ đại dẫn tới các lý thuyết học tập hiện đại. |

- **Phân bổ mức điểm Grounding:**
  - Mức `0`: 1 câu (`q16`).
  - Mức `1`: 0 câu.
  - Mức `2`: 4 câu (`q17`, `q18`, `q19`, `q20`).
- **Điểm trung bình Grounding:** $(0 + 2 + 2 + 2 + 2) / 5 = \mathbf{1.60 / 2.0}$ (Tương đương 80.0%).

---

## 4. Kết luận

- **Rủi ro thiên lệch (Annotator Bias):** Do người chấm cũng là người thiết kế câu hỏi benchmark và pipeline, có thể tồn tại thiên lệch chủ quan trong việc đánh giá mức độ tương đương ngữ nghĩa của bằng chứng.
- **Biện pháp giảm thiểu:**
  - Cố định danh sách 10 vị trí kiểm tra Coherence từ trước theo số thứ tự trang vật lý (Trang 1 đến Trang 10).
  - Đối chiếu nguyên văn từng ký tự của `gold_quote` đối với các câu kiểm tra Grounding thay vì đánh giá cảm tính.
  - Mọi kết quả chấm đều đính kèm trích dẫn văn bản trực tiếp và ID chunk trong DB để người chấm thi có thể tái lập và xác minh độc lập 100%.
