# Lab #17: Build Multi-Memory Agent với LangGraph

**Sinh viên:** Vũ Hải Đăng  
**MSSV:** 2A202600339

## 📌 Giới thiệu bài Lab
Dự án này tập trung vào việc xây dựng một AI Agent có khả năng ghi nhớ đa tầng (Multi-Memory Stack) sử dụng framework LangGraph. Agent không chỉ trả lời câu hỏi mà còn có khả năng học hỏi, ghi nhớ thông tin người dùng và tra cứu kiến thức chuyên sâu.

## 🧠 Hệ thống bộ nhớ (Memory Stack)
Hệ thống bao gồm 4 tầng bộ nhớ riêng biệt:
1.  **Short-term Memory (Bộ nhớ ngắn hạn):** Lưu trữ ngữ cảnh hội thoại hiện tại (sliding window).
2.  **Long-term Profile Memory (Hồ sơ người dùng):** Lưu trữ các sự thật (facts) cố định về người dùng (tên, sở thích, dị ứng...) vào file `profile.json`.
3.  **Episodic Memory (Bộ nhớ sự kiện):** Lưu trữ kết quả của các tác vụ đã hoàn thành vào file `episodes.json`.
4.  **Semantic Memory (Bộ nhớ ngữ nghĩa):** Sử dụng **ChromaDB** thực tế để lưu trữ và truy vấn kiến thức chuyên môn (Docker, FastAPI, Windows encoding...) thông qua embedding `text-embedding-3-small`.

## 🛠 Công nghệ sử dụng
-   **LangGraph:** Quản lý luồng suy nghĩ và trạng thái (state) của Agent.
-   **ChromaDB:** Vector Database để lưu trữ Semantic Memory.
-   **OpenAI REST API:** Gọi API trực tiếp thông qua `requests` để bypass các giới hạn môi trường (AppLocker/DLL block).
-   **Python:** Ngôn ngữ lập trình chính.

## 📁 Cấu trúc thư mục
-   `src/agent.py`: Định nghĩa Agent và luồng LangGraph.
-   `src/memory/`: Chứa các module xử lý 4 loại bộ nhớ.
-   `src/prompts.py`: Quản lý prompt injection và tối ưu hóa token budget.
-   `data/`: Lưu trữ cơ sở dữ liệu ChromaDB và các file JSON memory.
-   `BENCHMARK.md`: Kết quả kiểm thử so sánh giữa Agent có và không có bộ nhớ.
-   `REFLECTION.md`: Phân tích về quyền riêng tư và hạn chế kỹ thuật.

## 🚀 Cách chạy dự án
1.  Cài đặt thư viện: `pip install -r requirements.txt`
2.  Cấu hình file `.env` với `OPENAI_API_KEY`.
3.  Chạy benchmark: `python benchmark_runner.py`
4.  Chạy file test nhanh: `python scratch_test.py`

---
*Dự án được thực hiện trong khuôn khổ Lab #17 - Memory Systems for Agents.*
