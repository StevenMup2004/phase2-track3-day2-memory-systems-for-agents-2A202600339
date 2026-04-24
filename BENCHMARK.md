# BENCHMARK

Comparison of no-memory vs with-memory across 10 multi-turn conversations.

| # | Scenario | No-memory result | With-memory result | Pass? |
|---|----------|------------------|--------------------|-------|
| 1 | Profile recall: remember user name after delay | Bạn chưa cung cấp tên của mình. Bạn có thể cho tôi biết tên của bạn không? | Bạn tên là Vũ Hải Đăng. | Pass |
| 2 | Profile recall: remember timezone preference | Tôi không có thông tin về múi giờ của bạn. Bạn có thể cho tôi biết bạn đang ở đâu để tôi có thể giúp bạn xác định múi giờ? | Múi giờ của bạn là Asia/Ho_Chi_Minh. | Pass |
| 3 | Conflict update: allergy corrected | Tôi không có thông tin về dị ứng của bạn. Bạn có thể cung cấp thêm chi tiết về triệu chứng hoặc tình trạng của mình để tôi có thể giúp bạn tốt hơn. | Bạn dị ứng với đậu nành. | Pass |
| 4 | Conflict update: city overwritten | Tôi không có thông tin về nơi bạn đang sống. Bạn có thể chia sẻ thêm chi tiết nếu muốn! | Hiện tại, bạn đang sống ở Hà Nội. | Pass |
| 5 | Episodic recall: completed task outcome | Xin lỗi, nhưng tôi không có thông tin về việc bạn vừa hoàn tất. Bạn có thể chia sẻ thêm chi tiết không? | Bạn vừa hoàn tất việc sửa bug timeout cho API gateway. | Pass |
| 6 | Episodic recall: resolved issue tracking | Hiện tại, tôi không có thông tin về các vấn đề bạn đã giải quyết. Bạn có thể cung cấp thêm chi tiết để tôi có thể hỗ trợ bạn tốt hơn không? | Bạn vừa giải quyết vấn đề liên quan đến báo cáo nhập (import report). | Pass |
| 7 | Semantic retrieval: Windows encoding fix | Để tránh lỗi cp1252 decode crash khi đọc file source trên Windows, hãy sử dụng encoding 'utf-8' hoặc 'latin-1' khi mở file. | Để tránh lỗi cp1252 decode crash khi đọc file source trên Windows, hãy sử dụng encoding 'utf-8' hoặc 'utf-8-sig' khi mở file. | Pass |
| 8 | Semantic retrieval: FastAPI header deletion | Sử dụng object `response` để xóa header trong FastAPI middleware. Câu lệnh: `response.headers.pop('Header-Name', None)` | Sử dụng object `response` để xóa header trong FastAPI middleware. Câu lệnh: `response.headers.pop('Header-Name', None)` | Pass |
| 9 | Token budget trim under long context | Xin lỗi, tôi không biết tên bạn. | Tên bạn là Vũ Hải Đăng. | Pass |
| 10 | Combined profile + semantic in one response | Để kiểm tra git cho repo-scoped khi workspace có nhiều extension diffs, bạn có thể sử dụng lệnh sau: <br><br>```bash<br>git diff -- <tên_extension><br>``` | Chào Vũ Hải Đăng! Bạn có thể sử dụng lệnh sau để check git cho repo-scoped:<br><br>```bash<br>git diff -- <path-to-your-repo><br>``` | Pass |

Overall pass rate (with-memory expectation): 10/10

Notes:
- No-memory baseline disables memory retrieval and persistence.
- With-memory mode enables profile, episodic, semantic, and short-term retrieval.