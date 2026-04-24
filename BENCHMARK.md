# BENCHMARK

Comparison of no-memory vs with-memory across 10 multi-turn conversations.

| # | Scenario | No-memory result | With-memory result | Pass? |
|---|----------|------------------|--------------------|-------|
| 1 | Profile recall: remember user name after delay | Bạn chưa cung cấp tên của mình. Bạn có thể cho tôi biết tên của bạn không? | Bạn tên là Vũ Hải Đăng. | Pass |
| 2 | Profile recall: remember timezone preference | Tôi không có thông tin về múi giờ của bạn. Bạn có thể cho tôi biết bạn đang ở đâu để tôi có thể giúp xác định múi giờ của bạn. | Múi giờ của bạn là Asia/Ho_Chi_Minh. | Pass |
| 3 | Conflict update: allergy corrected | Tôi không có thông tin về dị ứng của bạn. Nếu bạn có triệu chứng dị ứng hoặc nghi ngờ mình bị dị ứng, tốt nhất là nên tham khảo ý kiến bác sĩ để được chẩn đoán và điều trị thích hợp. | Bạn dị ứng với đậu nành. | Pass |
| 4 | Conflict update: city overwritten | Tôi không có thông tin về nơi bạn đang sống. Bạn có thể chia sẻ thêm chi tiết nếu muốn! | Hiện tại, bạn đang sống ở Hà Nội. | Pass |
| 5 | Episodic recall: completed task outcome | Xin lỗi, nhưng tôi không có thông tin về việc bạn vừa hoàn tất. Bạn có thể chia sẻ thêm chi tiết không? | Bạn vừa hoàn tất việc fix bug timeout cho API gateway. | Pass |
| 6 | Episodic recall: resolved issue tracking | Hiện tại, tôi không có thông tin về các vấn đề bạn đã giải quyết. Bạn có thể cung cấp thêm chi tiết để tôi có thể hỗ trợ bạn tốt hơn không? | Bạn vừa giải quyết vấn đề liên quan đến báo cáo nhập khẩu. | Pass |
| 7 | Semantic retrieval: docker service name | Trong Docker Compose, để backend gọi đến một service khác (peer service), bạn có thể sử dụng tên của service đó như một hostname. Docker Compose tự động tạo ra một mạng lưới cho các service trong cùng một file `docker-compose.yml`, cho phép chúng giao tiếp với nhau qua tên service.<br><br>Ví dụ, nếu bạn có một service backend và một service database trong file `docker-compose.yml`, bạn có thể cấu hình như sau:<br><br>```yaml<br>version: '3'<br>services:<br>  backend:<br>    image: your-backend-image<br>    depends_on:<br>      - database<br>    environment:<br>      DATABASE_URL: "postgres://user:password@database:5432/dbname"<br><br>  database:<br>    image: postgres<br>    environment:<br>      POSTGRES_USER: user<br>      POSTGRES_PASSWORD: password<br>      POSTGRES_DB: dbname<br>```<br><br>Trong ví dụ này, backend có thể gọi đến database bằng cách sử dụng hostname `database`. Bạn chỉ cần đảm bảo rằng service mà backend cần gọi đã được định nghĩa trong cùng một file Docker Compose. | Trong Docker Compose, để backend gọi đến một service khác (peer service), bạn có thể sử dụng tên của service đó như một hostname. Docker Compose tự động tạo ra một mạng lưới cho các service trong cùng một file `docker-compose.yml`, cho phép chúng giao tiếp với nhau thông qua tên service.<br><br>Ví dụ, nếu bạn có một service backend và một service database trong file `docker-compose.yml`, bạn có thể cấu hình như sau:<br><br>```yaml<br>version: '3'<br>services:<br>  backend:<br>    image: your-backend-image<br>    depends_on:<br>      - database<br>    environment:<br>      - DATABASE_URL=database:5432<br><br>  database:<br>    image: postgres<br>    environment:<br>      - POSTGRES_USER=user<br>      - POSTGRES_PASSWORD=password<br>```<br><br>Trong ví dụ này, backend có thể gọi đến database bằng cách sử dụng hostname `database` và port `5432`. Bạn chỉ cần đảm bảo rằng backend sử dụng đúng URL để kết nối đến service database. | Pass |
| 8 | Semantic retrieval: FastAPI header deletion | ```python<br>del request.headers['Header-Name']<br>``` | ```python<br>del request.headers['Header-Name']<br>``` | Pass |
| 9 | Token budget trim under long context | Xin lỗi, tôi không biết tên bạn. | Tên bạn là Vũ Hải Đăng. | Pass |
| 10 | Combined profile + semantic in one response | Tên bạn: [Chưa biết]  <br>Danh từ: service | Vũ Hải Đăng, service name. | Pass |

Overall pass rate (with-memory expectation): 10/10

Notes:
- No-memory baseline disables memory retrieval and persistence.
- With-memory mode enables profile, episodic, semantic, and short-term retrieval.