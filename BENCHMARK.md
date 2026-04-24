# BENCHMARK

Comparison of no-memory vs with-memory across 10 multi-turn conversations.

| # | Scenario | No-memory result | With-memory result | Pass? |
|---|----------|------------------|--------------------|-------|
| 1 | Profile recall: remember user name after daily planning | Hiện tại, tôi không có thông tin về tên của bạn. Bạn có thể cho tôi biết tên của bạn được không? | Tên bạn là Vũ Hải Đăng. | Pass |
| 2 | Profile recall: remember timezone preference | Múi giờ bạn sử dụng phụ thuộc vào vị trí địa lý của bạn. Bạn có thể cho tôi biết bạn đang ở đâu để tôi có thể giúp xác định múi giờ chính xác hơn. | Múi giờ bạn đang dùng là Asia/Ho_Chi_Minh. | Pass |
| 3 | Conflict update: allergy corrected | Mình không có thông tin về tình trạng dị ứng của bạn. Nếu bạn có triệu chứng dị ứng, tốt nhất là nên tham khảo ý kiến bác sĩ để được chẩn đoán và điều trị chính xác. | Bạn dị ứng với hải sản. | Pass |
| 4 | Conflict update: city overwritten | Hiện tại, mình không có thông tin về nơi bạn đang sống. Bạn có thể chia sẻ thêm để mình có thể giúp đỡ tốt hơn! | Hiện tại, bạn đang sống ở Hà Nội. | Pass |
| 5 | Episodic recall: completed administrative task | Xin lỗi, nhưng tôi không có thông tin về việc bạn vừa hoàn tất. Bạn có thể chia sẻ thêm chi tiết không? | Bạn vừa hoàn tất việc nộp hồ sơ hoàn phí trước bạ cho xe máy. | Pass |
| 6 | Episodic recall: resolved complaint ticket | Xin lỗi, nhưng mình không có thông tin về vụ việc bạn vừa giải quyết. Bạn có thể chia sẻ thêm chi tiết để mình có thể giúp đỡ tốt hơn không? | Bạn vừa giải quyết vụ khiếu nại mã KN-8841. | Pass |
| 7 | Semantic retrieval: complaint response SLA policy | Theo quy chế nội bộ QD-17, khiếu nại cấp 1 phải được phản hồi trong vòng 7 ngày làm việc. Cấp ưu tiên cho khiếu nại này thường là cao, vì nó liên quan đến quyền lợi và nghĩa vụ của cá nhân hoặc tổ chức. | Theo quy chế nội bộ QD-17, khiếu nại cấp 1 phải được phản hồi trong 36 giờ. Cấp ưu tiên: cao. | Pass |
| 8 | Semantic retrieval: KYC retention policy | Theo quy trình HT-22, hồ sơ KYC nhóm B phải được lưu trữ tối thiểu là 5 năm. | Theo quy trình HT-22, hồ sơ KYC nhóm B phải lưu tối thiểu 18 tháng. | Pass |
| 9 | Token budget trim under long context | Xin lỗi, nhưng tôi không biết tên của bạn. | Tên bạn là Vũ Hải Đăng. | Pass |
| 10 | Combined profile + semantic in one response | Chào bạn! Theo hướng dẫn BM-47, giao dịch treo phải hoàn tiền trong vòng 7 ngày làm việc. Nếu bạn cần thêm thông tin, hãy cho tôi biết! | Chào Vũ Hải Đăng! Theo hướng dẫn BM-47, giao dịch treo cần hoàn tiền trong 5 ngày làm việc. | Pass |

Overall pass rate (with-memory expectation): 10/10

Notes:
- No-memory baseline disables memory retrieval and persistence.
- With-memory mode enables profile, episodic, semantic, and short-term retrieval.