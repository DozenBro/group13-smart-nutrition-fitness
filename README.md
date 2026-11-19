Đọc [đặc tả dự án và bảng theo dõi công việc](docs/PROJECT_SPEC.md) để xem user story, điều kiện nghiệm thu, phân công và mẫu nhật ký làm việc với AI.

## Chạy trên máy đang làm việc

1. Mở thư mục `smart-fitness` và chạy `START.cmd`.
2. Giữ cửa sổ đó mở. Truy cập `http://127.0.0.1:8013`.
3. Nhập **70 kg**, **175 cm**, bấm **Lưu số đo**. Kết quả BMI mong đợi là **22.86**.
4. Tải lại trang. Bản ghi vẫn hiện trong lịch sử.
5. Nhập **70 kg**, **0 cm**. Trang phải báo lỗi và lịch sử giữ nguyên.

Chạy API trực tiếp tại `http://127.0.0.1:8013/docs`. Chọn `POST /api/measurements`, bấm **Try it out**, rồi gửi ví dụ sau.

```json
{"weight_kg": 70, "height_cm": 175}
```

Để dừng website, bấm `Ctrl+C` ở cửa sổ chạy. PostgreSQL riêng của dự án tiếp tục chạy. Dừng nó bằng lệnh sau trong thư mục `smart-fitness`.

```powershell
.\.venv\Scripts\python.exe manage.py stop-db
```

## Cách chạy trên máy của thành viên khác

Cài Python 3.12 trở lên, Node.js 22.12 trở lên và PostgreSQL 18 trên Windows. Các bản cài trong nhóm nên cùng phiên bản để dễ hỗ trợ nhau. Sau khi nhận code, chạy các lệnh sau trong thư mục `smart-fitness`.

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
cd frontend
npm install
npm run build
cd ..
.\.venv\Scripts\python.exe manage.py run
```

Script tìm PostgreSQL trong PATH hoặc thư mục cài mặc định trên Windows. Nếu cài ở nơi khác, đặt biến `POSTGRES_BIN` tới thư mục `bin` của PostgreSQL trước khi chạy. Script tạo cụm dữ liệu riêng trong `.local/postgres`, dùng cổng `55432`, tài khoản `fitness` và mật khẩu ngẫu nhiên lưu trong `.local/database.json`. Thư mục `.local` được bỏ qua khi dùng Git. Website chỉ lắng nghe trên máy hiện tại.

Máy dựng bản đầu đã chạy bằng Python 3.14, Node.js 24 và PostgreSQL 18. Các thư viện Python đã được ghi phiên bản trong `requirements.txt`. Khi chia sẻ, gửi code và hướng dẫn, bỏ qua `.venv`, `.local` và `frontend/node_modules`.

## Đọc code theo thứ tự này

| File | Bạn cần hiểu gì? |
| --- | --- |
| `frontend/src/main.jsx` | Form lấy dữ liệu, gọi API bằng `fetch`, hiển thị kết quả và lỗi |
| `backend/main.py` | FastAPI nhận request, kiểm tra dữ liệu và gọi thao tác lưu/đọc |
| `backend/models.py` | Bản ghi số đo có những cột nào và giới hạn ở database |
| `backend/database.py` | SQLAlchemy tạo kết nối và phiên làm việc với PostgreSQL |
| `backend/health.py` | Chuyển chiều cao sang mét và tính BMI |
| `migrations/versions/001_measurements.py` | Alembic tạo bảng có phiên bản để các máy thống nhất schema |
| `tests/test_measurements.py` | Kiểm tra lưu/đọc, thứ tự lịch sử, ví dụ BMI và dữ liệu sai |

Luồng khi bấm Lưu là **form → POST /api/measurements → kiểm tra dữ liệu → INSERT trong PostgreSQL → trả bản ghi về form**. Khi tải lại trang, frontend gửi `GET /api/measurements` để lấy 30 bản ghi gần nhất.

## Quy tắc tạm dùng để nhóm thảo luận

- Cân nặng lớn hơn 0 và tối đa 500 kg.
- Chiều cao từ 50 đến 250 cm.
- Hai số có tối đa 2 chữ số thập phân.
- BMI = cân nặng kg / (chiều cao mét)², làm tròn kết quả hiển thị tới 2 số thập phân.
- Thời gian ghi nhận do server tạo, frontend hiển thị theo giờ máy người xem.

Đây là giới hạn kỹ thuật ban đầu cho dữ liệu giả lập. Nhóm cần chốt lại giới hạn và đối tượng người dùng trong rule sheet. Bản ghi hiện dùng chung trong bản học thử. Mốc tiếp theo là thêm tài khoản và gắn mỗi bản ghi với người sở hữu.

## Việc 

| Người | Việc đầu tiên | Bằng chứng cần mang lại |
| --- | --- | --- |
| A | Đọc công thức và giới hạn đầu vào, đề xuất quy tắc đã thống nhất | Một ví dụ hợp lệ, một ví dụ sai và kết quả mong đợi |
| B | Chạy API trên Swagger, đọc model và migration | Giải thích bản ghi lưu ở đâu và API đọc lại thế nào |
| C | Chạy form và thử thu nhỏ màn hình | Chỉ ra code gửi request và code hiện thông báo lỗi |
| D | Chạy thử luồng lưu và đề xuất các ca cần kiểm tra thêm | Một lỗi thực tế hoặc một trường hợp biên cần xử lý |
| E | Bắt đầu thu thập ba món ăn theo mẫu trong kế hoạch | Khẩu phần, kcal, giá VND, nguồn và ngày thu thập |
| F | Chạy trên máy thứ hai, chạy test và ghi lại trở ngại | Kết quả chạy, phiên bản công cụ, bước cài còn thiếu |

## Chạy kiểm thử

```powershell
.\.venv\Scripts\python.exe manage.py test
```

Lệnh này tạo hoặc dùng database **fitness_test**, áp dụng migration và chạy pytest. Các thay đổi của từng bài test được rollback. Database demo và database test có tên riêng.

Kết quả kiểm tra ban đầu gồm **12 bài test API đạt**, build React thành công và kiểm tra bằng trình duyệt cho thao tác lưu, tải lại, từ chối chiều cao bằng 0 và màn hình hẹp. Một bản ghi giả lập 70 kg, 175 cm được lưu trong database demo khi kiểm tra.

File `.github/workflows/ci.yml` đã chuẩn bị lệnh build và test cho GitHub Actions. Khi nhóm tạo repo và push code, mở mục Actions để xem kết quả thực tế của lần chạy đầu.

## Sau bản đầu tiên

1. Ghi nhận phản hồi khi cả nhóm chạy thử và chốt quy tắc đầu vào.
2. Tạo kho GitHub chung, đưa các việc còn lại thành issue và dùng pull request để review.
3. Thêm đăng ký, đăng nhập, phiên đăng nhập, phân quyền và chủ sở hữu số đo.
4. Thêm hồ sơ đủ dữ liệu cho TDEE, test công thức rồi thêm biểu đồ lịch sử.
5. Thêm admin khóa/mở khóa, kiểm thử tích hợp và chuẩn bị review Sprint 1.

Hãy dùng dữ liệu giả lập ở mốc này. Việc đăng nhập, TDEE, biểu đồ, admin, Docker Compose và triển khai staging sẽ được xây tiếp theo các issue của Sprint 1.

Tài liệu công cụ cho thành viên muốn tìm hiểu thêm được cung cấp bởi [FastAPI](https://fastapi.tiangolo.com/tutorial/sql-databases/), [Vite](https://vite.dev/guide/) và [PostgreSQL](https://www.postgresql.org/download/windows/).
