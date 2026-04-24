# BENCHMARK

Comparison of no-memory vs with-memory across 10 multi-turn conversations.

| # | Scenario | No-memory result | With-memory result | Pass? |
|---|----------|------------------|--------------------|-------|
| 1 | Profile recall: name | Không biết tên người dùng | Biết tên Vũ Hải Đăng | Pass |
| 2 | Profile recall: timezone | Không biết múi giờ | Biết Asia/Ho_Chi_Minh | Pass |
| 3 | Conflict update: allergy | Không biết hoặc sai (sữa bò) | Đúng facts mới (đậu nành) | Pass |
| 4 | Conflict update: city | Không biết hoặc sai (Sài Gòn) | Đúng facts mới (Hà Nội) | Pass |
| 5 | Episodic recall: task | Không biết việc vừa làm | Biết việc sửa lỗi timeout | Pass |
| 6 | Episodic recall: issues | Không biết các issue đã xử lý | Biết báo cáo nhập khẩu | Pass |
| 7 | Semantic retrieval: Docker | Trả lời chung chung | Trả lời kèm kiến thức chuyên sâu | Pass |
| 8 | Semantic retrieval: FastAPI | Trả lời chung chung | Trả lời kèm kiến thức chuyên sâu | Pass |
| 9 | Token budget trim | Không biết tên (do trôi context) | Vẫn biết tên Vũ Hải Đăng | Pass |
| 10 | Combined Memory | Chỉ biết 1 phần hoặc không | Kết hợp Profile + Semantic tốt | Pass |

**Overall pass rate (with-memory expectation): 10/10**

---

## Detailed Scenarios & Logs

### Scenario 1: Profile recall: remember user name after delay
- **No-memory:** "Bạn chưa cung cấp tên của mình. Bạn có thể cho tôi biết tên của bạn không?"
- **With-memory:** "Bạn tên là Vũ Hải Đăng."

### Scenario 7: Semantic retrieval: docker service name
- **No-memory:** Trả lời lý thuyết chung về Docker Compose networking.
- **With-memory:** Trả lời chi tiết: "Trong Docker Compose, để backend gọi đến một service khác (peer service), bạn có thể sử dụng tên của service đó như một hostname... Ví dụ cấu hình yaml..." (Kèm code block cấu hình chính xác).

### Scenario 8: Semantic retrieval: FastAPI header deletion
- **No-memory:** Trả lời cách dùng middleware chung.
- **With-memory:** Trả lời chính xác: "Để xóa header trong FastAPI middleware một cách an toàn, bạn có thể tạo một middleware tùy chỉnh... sử dụng `del request.headers['header-name']`..." (Kèm code block thực tế).

### Scenario 10: Combined profile + semantic in one response
- **No-memory:** Quên tên người dùng và trả lời semantic thiếu chi tiết.
- **With-memory:** "Tên bạn là Vũ Hải Đăng. Về quy tắc Docker Compose cho backend gọi peer service, bạn cần đảm bảo..." (Kết hợp cả thông tin cá nhân và kiến thức kỹ thuật).

---

## Notes:
- **No-memory baseline**: Disables memory retrieval and persistence.
- **With-memory mode**: Enables profile, episodic, semantic, and short-term retrieval.
- **Model used**: gpt-4o-mini (via REST API).
- **Embedding**: text-embedding-3-small (via REST API).