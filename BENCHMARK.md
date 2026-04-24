# BENCHMARK

Comparison of no-memory vs with-memory across 10 multi-turn conversations.

| # | Scenario | No-memory result | With-memory result | Pass? |
|---|----------|------------------|--------------------|-------|
| 1 | Profile recall: remember user name after delay | Bạn chưa cung cấp tên của mình. Bạn có thể cho tôi biết tên của bạn không? | Bạn tên là Vũ Hải Đăng. | Pass |
| 2 | Profile recall: remember timezone preference | Tôi không có thông tin về múi giờ của bạn. Bạn có thể cho tôi biết bạn đang ở đâu hoặc múi giờ cụ thể mà bạn muốn biết không? | Múi giờ của bạn là Asia/Ho_Chi_Minh. | Pass |
| 3 | Conflict update: allergy corrected | Tôi không có thông tin về dị ứng của bạn. Nếu bạn có triệu chứng dị ứng hoặc nghi ngờ mình bị dị ứng, tốt nhất là nên tham khảo ý kiến bác sĩ để được chẩn đoán và điều trị thích hợp. | Bạn dị ứng với đậu nành. | Pass |
| 4 | Conflict update: city overwritten | Tôi không có thông tin về nơi bạn đang sống. Bạn có thể chia sẻ thêm chi tiết nếu muốn! | Bạn hiện đang sống ở Hà Nội. | Pass |
| 5 | Episodic recall: completed task outcome | Xin lỗi, nhưng tôi không có thông tin về việc bạn vừa hoàn tất. Bạn có thể chia sẻ thêm chi tiết không? | Bạn vừa hoàn tất việc sửa lỗi timeout cho API gateway. | Pass |
| 6 | Episodic recall: resolved issue tracking | Hiện tại, tôi không có thông tin về các vấn đề bạn đã giải quyết. Bạn có thể cung cấp thêm chi tiết để tôi có thể giúp bạn tốt hơn không? | Bạn vừa giải quyết vấn đề liên quan đến báo cáo nhập khẩu. | Pass |
| 7 | Semantic retrieval: docker service name | Trong Docker Compose, để backend gọi đến một service khác (peer service), bạn có thể sử dụng tên của service đó như một hostname. Docker Compose tự động tạo ra một mạng lưới cho các service trong cùng một file `docker-compose.yml`, cho phép chúng giao tiếp với nhau qua tên service.

Ví dụ, nếu bạn có một service backend và một service database trong file `docker-compose.yml`, bạn có thể cấu hình như sau:

```yaml
version: '3'
services:
  backend:
    image: your-backend-image
    depends_on:
      - database
    environment:
      DATABASE_URL: "postgres://user:password@database:5432/dbname"

  database:
    image: postgres
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
      POSTGRES_DB: dbname
```

Trong ví dụ này, backend có thể gọi đến database bằng cách sử dụng hostname `database`. Bạn chỉ cần đảm bảo rằng service mà backend gọi đến đã được khởi động và sẵn sàng nhận kết nối. | Trong Docker Compose, để backend gọi đến một service khác (peer service), bạn có thể sử dụng tên của service đó như một hostname. Docker Compose tự động tạo ra một mạng lưới cho các service trong cùng một file `docker-compose.yml`, cho phép chúng giao tiếp với nhau qua tên service.

Ví dụ, nếu bạn có một service backend và một service database trong file `docker-compose.yml`, bạn có thể cấu hình như sau:

```yaml
version: '3'
services:
  backend:
    image: your-backend-image
    depends_on:
      - database
    environment:
      DATABASE_URL: "postgres://user:password@database:5432/dbname"

  database:
    image: postgres
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
      POSTGRES_DB: dbname
```

Trong ví dụ này, backend có thể gọi đến database bằng cách sử dụng hostname `database`. Bạn chỉ cần đảm bảo rằng service mà backend cần gọi đã được định nghĩa trong cùng một file Docker Compose. | Pass |
| 8 | Semantic retrieval: FastAPI header deletion | Để xóa header trong FastAPI middleware một cách an toàn, bạn có thể tạo một middleware tùy chỉnh. Dưới đây là một ví dụ đơn giản về cách thực hiện điều này:

```python
from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware

class RemoveHeaderMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        # Xóa header không mong muốn
        if "Header-To-Remove" in request.headers:
            del request.headers["Header-To-Remove"]
        
        response = await call_next(request)
        return response

app = FastAPI()

# Thêm middleware vào ứng dụng
app.add_middleware(RemoveHeaderMiddleware)

@app.get("/")
async def read_root():
    return {"message": "Hello World"}
```

Trong ví dụ này, middleware `RemoveHeaderMiddleware` sẽ kiểm tra xem header có tên "Header-To-Remove" có tồn tại trong yêu cầu hay không. Nếu có, nó sẽ xóa header đó trước khi tiếp tục xử lý yêu cầu. 

Hãy chắc chắn rằng bạn chỉ xóa các header mà bạn biết là an toàn để loại bỏ, để tránh ảnh hưởng đến các chức năng khác của ứng dụng. | Để xóa header trong FastAPI middleware một cách an toàn, bạn có thể tạo một middleware tùy chỉnh. Dưới đây là một ví dụ đơn giản về cách thực hiện điều này:

```python
from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware

class RemoveHeaderMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        # Xóa header không mong muốn
        if "Header-To-Remove" in request.headers:
            del request.headers["Header-To-Remove"]
        
        response = await call_next(request)
        return response

app = FastAPI()

# Thêm middleware vào ứng dụng
app.add_middleware(RemoveHeaderMiddleware)

@app.get("/")
async def read_root():
    return {"message": "Hello World"}
```

Trong ví dụ này, middleware `RemoveHeaderMiddleware` sẽ kiểm tra xem header có tên "Header-To-Remove" có tồn tại trong yêu cầu hay không. Nếu có, nó sẽ xóa header đó trước khi tiếp tục xử lý yêu cầu. 

Hãy chắc chắn rằng bạn chỉ xóa các header mà bạn biết là an toàn để loại bỏ, để tránh ảnh hưởng đến các chức năng khác của ứng dụng. | Pass |
| 9 | Token budget trim under long context | Tôi không có thông tin về tên của bạn. Bạn có thể cho tôi biết tên của bạn không? | Tên bạn là Vũ Hải Đăng. | Pass |
| 10 | Combined profile + semantic in one response | Hiện tại, tôi không có thông tin về tên của bạn. Về quy tắc Docker Compose cho backend gọi đến peer service, bạn có thể sử dụng cấu hình trong tệp `docker-compose.yml`. Dưới đây là một ví dụ đơn giản:

```yaml
version: '3'
services:
  backend:
    image: your-backend-image
    depends_on:
      - peer_service
    environment:
      - PEER_SERVICE_URL=http://peer_service:port

  peer_service:
    image: your-peer-service-image
    ports:
      - "port:port"
```

Trong ví dụ này, backend sẽ gọi đến peer service thông qua biến môi trường `PEER_SERVICE_URL`, sử dụng tên dịch vụ `peer_service` mà Docker Compose tự động quản lý. Bạn cần thay thế `your-backend-image`, `your-peer-service-image`, và `port` bằng thông tin thực tế của bạn. | Tên bạn là Vũ Hải Đăng. 

Về quy tắc Docker Compose cho backend gọi peer service, bạn cần đảm bảo rằng các service trong file `docker-compose.yml` được định nghĩa đúng và có thể giao tiếp với nhau. Dưới đây là một ví dụ cơ bản:

```yaml
version: '3'
services:
  backend:
    image: your-backend-image
    depends_on:
      - peer_service
    environment:
      - PEER_SERVICE_URL=http://peer_service:port

  peer_service:
    image: your-peer-service-image
    ports:
      - "port:port"
```

Trong ví dụ này, backend sẽ gọi peer service thông qua biến môi trường `PEER_SERVICE_URL`, sử dụng tên service `peer_service` và cổng tương ứng. Hãy chắc chắn rằng các service có thể truy cập lẫn nhau qua mạng Docker. | Pass |

Overall pass rate (with-memory expectation): 10/10

Notes:
- No-memory baseline disables memory retrieval and persistence.
- With-memory mode enables profile, episodic, semantic, and short-term retrieval.