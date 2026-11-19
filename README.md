# Smart Nutrition & Fitness

[![Build and test](https://github.com/DozenBro/group13-smart-nutrition-fitness/actions/workflows/ci.yml/badge.svg)](https://github.com/DozenBro/group13-smart-nutrition-fitness/actions/workflows/ci.yml)

Ứng dụng web hỗ trợ theo dõi số đo cơ thể, lập kế hoạch tập luyện và gợi ý bữa ăn Việt Nam. Dự án được phát triển bởi **Group 13** trong môn Công nghệ phần mềm.

Phiên bản hiện tại cung cấp luồng ghi nhận cân nặng, chiều cao, tính BMI và lưu lịch sử trên PostgreSQL. Các chức năng tài khoản, TDEE, tập luyện và bữa ăn đang được phát triển theo kế hoạch sprint.

## Tính năng

- Ghi nhận cân nặng và chiều cao với kiểm tra đầu vào ở backend.
- Tính BMI và hiển thị kết quả với hai chữ số thập phân.
- Xem bảng 30 số đo gần nhất, mới nhất ở trên.
- Lưu dữ liệu trong PostgreSQL và tải lại lịch sử qua API.
- Thử API trực tiếp bằng Swagger UI.
- Kiểm thử tự động và build frontend qua GitHub Actions.

> Bản hiện tại sử dụng dữ liệu giả lập và lịch sử dùng chung. Chức năng đăng nhập và quyền sở hữu dữ liệu được triển khai ở mốc tiếp theo của Sprint 1.

## Công nghệ

| Thành phần | Công cụ |
| --- | --- |
| Frontend | React, Vite, JavaScript, CSS |
| Backend | Python, FastAPI, Pydantic |
| Database | PostgreSQL |
| ORM và migration | SQLAlchemy, Alembic |
| Kiểm thử | pytest, FastAPI TestClient |
| CI | GitHub Actions |

Giao diện gửi request JSON tới FastAPI. Backend kiểm tra dữ liệu, thực hiện tính toán và đọc/ghi PostgreSQL thông qua SQLAlchemy. Alembic quản lý phiên bản schema.

## Yêu cầu môi trường

Hướng dẫn chạy local dưới đây dành cho **Windows và PowerShell**, sử dụng các phiên bản đã kiểm tra trong dự án.

- Python **3.14**
- Node.js **24** kèm npm
- PostgreSQL **18**, gồm `initdb` và `pg_ctl`
- Git

Script `manage.py` quản lý PostgreSQL local trên Windows. CI sử dụng PostgreSQL service riêng trên Ubuntu.

## Cài đặt

### 1. Lấy mã nguồn

```powershell
git clone https://github.com/DozenBro/group13-smart-nutrition-fitness.git
cd group13-smart-nutrition-fitness
```

Repo riêng tư yêu cầu tài khoản GitHub đã được cấp quyền truy cập.

### 2. Cài thư viện Python

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

### 3. Cài và build frontend

```powershell
cd frontend
npm install
npm run build
cd ..
```

## Chạy ứng dụng

Chạy từ thư mục gốc repo.

```powershell
.\.venv\Scripts\python.exe manage.py run
```

Hoặc mở `START.cmd` sau khi hoàn tất cài đặt và build.

| Địa chỉ | Nội dung |
| --- | --- |
| `http://127.0.0.1:8013` | Giao diện ứng dụng |
| `http://127.0.0.1:8013/docs` | Swagger UI |

Lần đầu chạy, script khởi tạo vùng dữ liệu PostgreSQL riêng tại `.local/postgres`, tạo database, áp dụng migration và khởi động FastAPI. Mật khẩu được sinh ngẫu nhiên và lưu tại `.local/database.json` trên từng máy.

| Cấu hình local | Giá trị |
| --- | --- |
| Địa chỉ PostgreSQL | `127.0.0.1:55432` |
| Database ứng dụng | `fitness_demo` |
| Database kiểm thử | `fitness_test` |
| Tài khoản PostgreSQL | `fitness` |

Script tìm PostgreSQL trong PATH hoặc thư mục cài mặc định trên Windows. Nếu PostgreSQL được cài ở vị trí khác, đặt `POSTGRES_BIN` tới thư mục `bin` trước khi chạy. Ví dụ với vị trí cài mặc định của PostgreSQL 18:

```powershell
$env:POSTGRES_BIN = "C:\Program Files\PostgreSQL\18\bin"
.\.venv\Scripts\python.exe manage.py run
```

Dừng FastAPI bằng `Ctrl+C`. Để dừng PostgreSQL riêng của dự án, chạy:

```powershell
.\.venv\Scripts\python.exe manage.py stop-db
```

Các thư mục `.local`, `.venv`, `frontend/node_modules` và `frontend/dist` được bỏ qua khi commit bằng Git.

## Phát triển giao diện

Giữ backend chạy bằng `manage.py run`. Trong terminal thứ hai, mở thư mục `frontend` và chạy Vite:

```powershell
cd frontend
npm run dev
```

Truy cập địa chỉ local Vite in ra trong terminal, mặc định là `http://127.0.0.1:5173`. Request `/api` được chuyển tới FastAPI ở cổng `8013`.

Vite cập nhật giao diện khi sửa code. Khi dùng giao diện do FastAPI phục vụ ở cổng `8013`, chạy lại `npm run build` sau khi sửa frontend. Khởi động lại backend sau khi sửa code Python.

## API

| Method | Endpoint | Chức năng |
| --- | --- | --- |
| `POST` | `/api/measurements` | Lưu số đo và trả kết quả BMI |
| `GET` | `/api/measurements` | Đọc lịch sử số đo |

Ví dụ body cho `POST /api/measurements`:

```json
{
  "weight_kg": 70,
  "height_cm": 175
}
```

Request hợp lệ trả HTTP `201` với bản ghi đã lưu và BMI `22.86`. Dữ liệu sai trả HTTP `422`. Với endpoint đọc lịch sử, `limit` mặc định là `30`, hỗ trợ từ `1` đến `100`.

Các trường, giới hạn và điều kiện nghiệm thu được mô tả trong [đặc tả dự án](docs/PROJECT_SPEC.md).

## Kiểm thử

```powershell
.\.venv\Scripts\python.exe manage.py test
```

Lệnh sử dụng database `fitness_test`, áp dụng migration rồi chạy pytest. Bộ test hiện có 12 trường hợp, kiểm tra công thức BMI, lưu/đọc, dữ liệu sai, thứ tự lịch sử và giới hạn truy vấn.

Workflow [Build and test](https://github.com/DozenBro/group13-smart-nutrition-fitness/actions/workflows/ci.yml) chạy khi push hoặc mở pull request. Pipeline khởi tạo PostgreSQL, áp dụng migration, chạy test backend và build frontend.

## Cấu trúc dự án

```text
.
├── backend/                 # API, model, kết nối database và tính BMI
├── frontend/
│   ├── src/                 # Giao diện React và CSS
│   ├── package.json
│   └── vite.config.js
├── migrations/              # Lịch sử thay đổi schema
├── tests/                   # Kiểm thử backend
├── docs/
│   ├── PROJECT_SPEC.md      # Phạm vi, kiến trúc và quy trình chung
│   └── sprints/
│       ├── SPRINT_1.md      # Health tracking và tài khoản
│       ├── SPRINT_2.md      # Workout và streak
│       └── SPRINT_3.md      # Meals, tích hợp và phát hành
├── .github/workflows/ci.yml # Pipeline build và test
├── alembic.ini
├── manage.py                # Quản lý database local, migration, chạy app và test
├── requirements.txt
└── START.cmd
```

## Đóng góp

1. Nhận task và thống nhất điều kiện nghiệm thu trong issue.
2. Tạo nhánh theo công việc, ví dụ `feature/S1-06-measurement-owner`.
3. Thực hiện thay đổi và chạy kiểm thử liên quan.
4. Mở pull request, liên kết task, mô tả thay đổi và kết quả kiểm tra.
5. Nhờ một thành viên khác review trước khi merge.

Đọc [spec tổng](docs/PROJECT_SPEC.md) và spec của sprint đang làm trước khi nhận task. Mỗi sprint giữ user story, điều kiện nghiệm thu, bảng việc, kết quả kiểm tra và nhật ký AI riêng.

## Lộ trình

| Giai đoạn | Nội dung |
| --- | --- |
| [Sprint 1](docs/sprints/SPRINT_1.md) | Tài khoản, phân quyền, hồ sơ, BMI/TDEE, biểu đồ và quản lý tài khoản |
| [Sprint 2](docs/sprints/SPRINT_2.md) | Danh mục bài tập, kế hoạch tập, ghi nhận hoàn thành và streak |
| [Sprint 3](docs/sprints/SPRINT_3.md) | Dữ liệu món Việt, gợi ý bữa ăn, ghi nhận bữa ăn và hoàn thiện bản phát hành |

Trạng thái chi tiết và các quyết định chờ xác nhận được cập nhật trong [đặc tả dự án](docs/PROJECT_SPEC.md).
