# Đặc tả và theo dõi dự án Group 13

**Smart Nutrition and Fitness System · Phiên bản 0.1 · Ngày 19/11/2026**

**Trạng thái tài liệu — Bản nháp để nhóm thống nhất.** Tên thành viên, thời hạn Sprint 1 và các quyết định còn mở cần được nhóm điền. Quy trình review và ghi nhận AI bên dưới là đề xuất cho nhóm sử dụng.

**Mốc code được đối chiếu** — `a2e3eea6447aa2a62492a7c9d36ce01ec9af3166` trên nhánh `main`. Khi code thay đổi, cập nhật mốc và kết quả kiểm tra trong mục 10.

**Đọc nhanh** · [Bắt đầu](#1-cách-sử-dụng) · [Phạm vi](#2-phạm-vi-và-tiến-độ) · [Thành viên](#3-phân-công-sáu-thành-viên) · [User story](#4-user-story-sprint-1) · [Quy tắc](#5-quy-tắc-và-quyết-định) · [Kỹ thuật](#6-đặc-tả-kỹ-thuật) · [Công việc](#7-bảng-công-việc) · [AI](#8-quy-trình-làm-việc-với-ai) · [Nghiệm thu](#9-kiểm-thử-và-điều-kiện-hoàn-thành) · [Nhật ký](#10-nhật-ký-và-bằng-chứng)

## 1. Cách sử dụng

File này ghi những gì phần mềm phải làm, người phụ trách, điều kiện nghiệm thu và bằng chứng công việc. Mỗi thành viên gửi cho AI của mình phần liên quan trước khi bắt đầu task.

**Ở buổi họp đầu**, nhóm làm bốn việc.

- [ ] Điền tên vào vai trò A–F, xác nhận ai nhận từng task và người review.
- [ ] Điền ngày review Sprint 1 và hạn hoàn thành từng task trong mục 7.
- [ ] Chốt các quyết định đang mở trong mục 5, hoặc chỉ định người tìm câu trả lời.
- [ ] Mỗi người chạy bản demo, đọc story mình nhận và thử một trường hợp sai.

**Mỗi lần làm việc**, cập nhật task, ghi lại phần AI hỗ trợ và kết quả thực tế. Khi thay đổi yêu cầu, sửa mục tương ứng và ghi lý do vào lịch sử quyết định. Khi báo cáo, dùng các liên kết issue, commit, pull request và CI để mở bằng chứng.

| Thông tin cần nhóm bổ sung | Giá trị |
| --- | --- |
| Ngày bắt đầu Sprint 1 thực tế | Chưa điền |
| Ngày review Sprint 1 | Chưa điền |
| Người tổng hợp tiến độ | Chưa điền |
| Người trao đổi yêu cầu với giảng viên | Chưa điền |
| Mẫu hoặc định dạng giảng viên yêu cầu thêm | Chưa xác nhận |

## 2. Phạm vi và tiến độ

Sản phẩm cuối giúp thành viên quản lý hồ sơ sức khỏe, số đo, kế hoạch tập, gợi ý món Việt và hoạt động đã hoàn thành. Admin quản lý tài khoản và dữ liệu danh mục. Hệ thống dùng quy tắc rõ ràng để tính chỉ số và gợi ý kế hoạch.

**Mục tiêu Sprint 1** — Thành viên đăng ký, đăng nhập, lưu hồ sơ và số đo của mình, xem BMI/TDEE và lịch sử bằng biểu đồ. Admin xem và khóa/mở khóa tài khoản. Nhóm có thiết kế, API, migration, kiểm thử và bản demo tích hợp.

| Hạng mục | Tình trạng ở mốc đối chiếu | Bằng chứng hoặc phần còn lại |
| --- | --- | --- |
| React gửi request tới FastAPI | Có bản demo | [Giao diện](../frontend/src/main.jsx), [API](../backend/main.py) |
| Lưu và đọc số đo trong PostgreSQL | Có bản demo dùng dữ liệu chung | Cần bổ sung tài khoản và chủ sở hữu bản ghi |
| Kiểm tra đầu vào và tính BMI | Có code và kiểm thử | Cần áp dụng trong luồng riêng của Member và được nhóm review |
| Lịch sử số đo | Có bảng số đo gần nhất | Cần lọc theo tài khoản và thêm biểu đồ |
| Đăng ký, đăng nhập, phân quyền | Chưa triển khai | US-A01, US-A02, US-AD01 |
| Hồ sơ và TDEE | Chưa triển khai | US-H01, US-H04, quyết định D-02 |
| ERD user/profile/measurement | Chưa có thiết kế đầy đủ | Hiện mới có bảng `measurements` |
| GitHub và CI | Đã có lần chạy thành công | EV-01 trong mục 10 |
| Review, nghiệm thu của nhóm | Chờ thực hiện | Điền người kiểm tra và kết quả sau khi thực hiện |

**Sprint 2** dự kiến làm danh mục bài tập, kế hoạch tập và streak. **Sprint 3** dự kiến làm dữ liệu món Việt, gợi ý bữa ăn và ghi nhận bữa ăn. Challenge chờ xác nhận phạm vi. Kế hoạch thời gian cần điều chỉnh theo hạn nộp thực tế.

Các tích hợp Maps, đặt đồ ăn, thanh toán, thiết bị đeo và cảnh báo chẩn đoán được giữ ngoài đợt triển khai hiện tại theo phạm vi nhóm đang sử dụng.

## 3. Phân công sáu thành viên

Đây là phân công đề xuất. Người được giao xác nhận nhận việc trên issue. Mọi người kiểm thử phần mình làm và có người khác review thay đổi trước khi ghi hoàn thành.

| Vai trò | Tên | Trách nhiệm | Việc hỗ trợ trong Sprint 1 |
| --- | --- | --- | --- |
| A | Chưa điền | Yêu cầu, hồ sơ, BMI/TDEE | Chốt AC, công thức và ví dụ tính tay |
| B | Chưa điền | Backend, database, auth | Thiết kế user/profile/session, migration và quyền sở hữu |
| C | Chưa điền | Giao diện và tích hợp | Figma, form, màn hình đăng nhập, dashboard và biểu đồ |
| D | Chưa điền | Module tập luyện của Sprint 2 | Review ca biên và kiểm thử API, kiểm tra truy cập chéo tài khoản |
| E | Chưa điền | Module bữa ăn của Sprint 3 | Review đầu vào hồ sơ, thử luồng người dùng, chuẩn bị dữ liệu có nguồn |
| F | Chưa điền | Cách chạy, CI, triển khai và kiểm thử trình duyệt | Chạy máy thứ hai, giữ liên kết CI và tổng hợp kịch bản demo |

AI là công cụ hỗ trợ cho người nhận task. Mỗi task vẫn có thành viên chịu trách nhiệm giải thích và kiểm tra kết quả. Code khởi tạo đã có hỗ trợ AI, và chưa được ghi nhận là đóng góp triển khai riêng của một thành viên A–F.

## 4. User story Sprint 1

**AC** là điều kiện nghiệm thu có thể kiểm tra. Một story chỉ được chuyển sang Done sau khi đáp ứng toàn bộ AC và điều kiện trong mục 9. Mỗi story giữ mã ổn định để liên kết code, test và nhật ký.

### US-A01 Đăng ký tài khoản

**Là người mới, tôi muốn tạo tài khoản để có thể sử dụng các chức năng dành cho thành viên.** Phụ trách đề xuất B, phối hợp C, review D. Trạng thái Chưa làm. Liên quan WBS 1.6.

- **AC1** Dữ liệu đăng ký hợp lệ tạo được tài khoản Member và người dùng có thể đăng nhập.
- **AC2** Email đã tồn tại bị từ chối, kể cả trường hợp khác chữ hoa/thường theo quy tắc đã chốt.
- **AC3** Mật khẩu được lưu bằng thuật toán hash của thư viện được chọn. API và log ứng dụng không trả mật khẩu hoặc hash.
- **AC4** Người đăng ký không thể tự cấp quyền Admin qua dữ liệu gửi lên.

### US-A02 Đăng nhập và đăng xuất

**Là thành viên, tôi muốn đăng nhập và đăng xuất để truy cập dữ liệu của mình và kết thúc phiên khi dùng xong.** Phụ trách B, phối hợp C, review D. Trạng thái Chưa làm. WBS 1.6. Phụ thuộc US-A01.

- **AC1** Đúng thông tin đăng nhập tạo phiên hợp lệ, tải lại trang vẫn nhận diện được người dùng trong thời hạn phiên.
- **AC2** Sai thông tin bị từ chối với thông báo thống nhất.
- **AC3** Đăng xuất làm phiên hết hiệu lực ở backend. Gọi lại API bằng phiên cũ bị từ chối.
- **AC4** Request chưa đăng nhập tới chức năng được bảo vệ nhận HTTP 401.
- **AC5** Quyền Admin được kiểm tra tại backend khi gọi trực tiếp API.

### US-H01 Cập nhật hồ sơ

**Là thành viên, tôi muốn lưu thông tin hồ sơ để hệ thống có đủ đầu vào tính các chỉ số đã thống nhất.** Phụ trách A, phối hợp B/C, review E. Trạng thái Chưa làm. WBS 1.7. Phụ thuộc US-A02 và D-02.

- **AC1** Các trường, đơn vị, giá trị hợp lệ và trường bắt buộc được mô tả trước khi làm form.
- **AC2** Lưu hồ sơ thành công, tải lại vẫn thấy đúng dữ liệu của tài khoản đó.
- **AC3** Input sai trả thông báo phù hợp, bản hồ sơ đã lưu giữ nguyên.
- **AC4** Thành viên khác không đọc hoặc sửa được hồ sơ bằng cách đổi ID trong request.

### US-H02 Ghi nhận số đo

**Là thành viên, tôi muốn lưu cân nặng và chiều cao để theo dõi thay đổi của mình theo thời gian.** Phụ trách B/C, A chốt quy tắc, review D. Trạng thái Một phần. WBS 1.7. Phụ thuộc US-A02.

- **AC1** Số đo hợp lệ được lưu cùng người sở hữu và thời điểm do server tạo.
- **AC2** Bản ghi vẫn đọc lại được sau khi tải lại trang và khởi động lại ứng dụng.
- **AC3** Chiều cao bằng 0 và input ngoài giới hạn bị từ chối, không tạo bản ghi.
- **AC4** Backend lấy người sở hữu từ phiên đăng nhập. Gửi `user_id` của người khác không cho phép ghi thay họ.
- **AC5** Khi lưu thất bại, giao diện báo lỗi và không hiện bản ghi như đã lưu thành công.

**Bằng chứng hiện có** — Tạo/đọc số đo và từ chối input sai có test. Chủ sở hữu và auth cần bổ sung. Test hiện tại mới đối chiếu một phần AC1–AC3.

### US-H03 Xem BMI

**Là thành viên, tôi muốn xem BMI từ số đo của mình để biết kết quả tính toán theo công thức hệ thống sử dụng.** Phụ trách A/C, review E. Trạng thái Một phần. WBS 1.7. Phụ thuộc US-H02.

- **AC1** 70 kg và 175 cm cho kết quả hiển thị 22.86.
- **AC2** Backend chuyển cm sang mét, dùng công thức và cách làm tròn đã ghi trong S1-R02.
- **AC3** Kết quả gắn với số đo của chính người đang đăng nhập. Khi chưa có số đo, màn hình hướng dẫn nhập dữ liệu.
- **AC4** Có kiểm thử ví dụ đã tính độc lập và các giới hạn đầu vào được nhóm chấp nhận.

### US-H04 Xem TDEE

**Là thành viên, tôi muốn xem ước tính năng lượng tiêu hao mỗi ngày từ hồ sơ và số đo để sử dụng cho các chức năng lập kế hoạch sau này.** Phụ trách A, phối hợp B/C, review E. Trạng thái Chờ quyết định D-02. WBS 1.7.

- **AC1** Nhóm ghi rõ công thức, nguồn, đầu vào, hệ số hoạt động, phạm vi sử dụng và cách làm tròn.
- **AC2** Tối thiểu hai ví dụ tính độc lập được đối chiếu bằng unit test trước khi tích hợp.
- **AC3** Thiếu đầu vào bắt buộc thì chỉ rõ trường cần bổ sung, kết quả chưa sẵn sàng.
- **AC4** UI ghi đơn vị kcal/ngày và thể hiện đây là giá trị ước tính.

### US-H05 Xem lịch sử và biểu đồ

**Là thành viên, tôi muốn xem lịch sử và biểu đồ số đo của mình để theo dõi các lần ghi nhận.** Phụ trách C, phối hợp B, review F. Trạng thái Một phần. WBS 1.7. Phụ thuộc US-H02.

- **AC1** Bảng và biểu đồ chỉ dùng số đo thuộc tài khoản hiện tại.
- **AC2** Bảng mặc định hiển thị mới nhất trước. Biểu đồ dùng trình tự thời gian tăng dần và ghi rõ đơn vị.
- **AC3** Lưu số đo mới rồi tải lại thì bảng và biểu đồ cùng cập nhật từ dữ liệu đã lưu.
- **AC4** Trạng thái chưa có dữ liệu, đang tải và lỗi API đều được xử lý rõ ràng.

**Bằng chứng hiện có** — Có bảng lịch sử dùng dữ liệu chung. Cần bổ sung bộ lọc chủ sở hữu và biểu đồ.

### US-AD01 Quản lý trạng thái tài khoản

**Là Admin, tôi muốn xem danh sách và khóa/mở khóa tài khoản để quản lý quyền sử dụng hệ thống.** Phụ trách B/C, review D. Trạng thái Chưa làm. WBS 1.8. Phụ thuộc US-A02.

- **AC1** Admin xem được danh sách cùng trạng thái tài khoản và thực hiện khóa/mở khóa.
- **AC2** Member gọi trực tiếp API quản trị bị từ chối bằng HTTP 403.
- **AC3** Sau khi bị khóa, tài khoản không đăng nhập mới và không dùng tiếp phiên cũ để truy cập API được bảo vệ.
- **AC4** Sau khi mở khóa, tài khoản có thể đăng nhập lại, dữ liệu cũ còn nguyên.
- **AC5** Mật khẩu và hash được loại khỏi phản hồi danh sách tài khoản.

## 5. Quy tắc và quyết định

### Quy tắc Sprint 1

| Mã | Quy tắc | Tình trạng |
| --- | --- | --- |
| S1-R01 | Cân nặng lớn hơn 0 và tối đa 500 kg. Chiều cao từ 50 đến 250 cm. Tối đa 2 số thập phân. | Đã dùng trong bản demo, nhóm cần xác nhận giới hạn |
| S1-R02 | BMI = kg / (cm / 100)². Backend làm tròn kết quả hiển thị tới 2 số thập phân bằng ROUND_HALF_UP. | Có code và test ví dụ |
| S1-R03 | Thời điểm ghi nhận do server tạo, lưu kiểu timezone-aware. Hiện UI dùng giờ máy người xem. | Có trong demo, cách hiển thị cuối chờ D-05 |
| S1-R04 | Member đọc/ghi dữ liệu riêng qua danh tính đã xác thực ở backend. | Yêu cầu mục tiêu, chưa triển khai |
| S1-R05 | Admin quản lý trạng thái tài khoản, tài khoản khóa bị từ chối truy cập cả với phiên cũ. | Yêu cầu mục tiêu, chưa triển khai |
| S1-R06 | Dữ liệu sai trả HTTP 422 và thông tin lỗi. Request chưa đăng nhập trả 401, thiếu quyền trả 403. | 422 có sẵn, 401/403 cần triển khai |
| S1-R07 | Database thử nghiệm là `fitness_test`, tách khỏi `fitness_demo`. | Có trong lệnh test |

### Các quyết định cần theo dõi

| Mã | Câu hỏi và đề xuất | Người theo dõi | Trạng thái | Kết luận và ngày chốt |
| --- | --- | --- | --- | --- |
| D-01 | Xác nhận phạm vi và ngày review Sprint 1 với giảng viên | A | Chờ xác nhận | Chưa điền |
| D-02 | Chọn công thức TDEE, nguồn và hệ số hoạt động. Kế hoạch gợi ý Mifflin–St Jeor. | A | Chờ tìm nguồn và nhóm chốt | Chưa điền |
| D-03 | Xác định email/mật khẩu hợp lệ, thư viện hash, thời hạn phiên, cookie/CSRF và cách cấp Admin ban đầu. Định hướng server session theo Excel. | B | Chờ thiết kế | Chưa điền |
| D-04 | Challenge có bắt buộc không? Mô tả dự án và CSV đang khác nhau. | A | Chờ hỏi giảng viên | Chưa điền |
| D-05 | Chốt múi giờ hiển thị và dữ liệu nào được sửa sau khi lưu | A + C | Chờ nhóm chốt | Chưa điền |
| D-06 | Chọn nơi staging, điều kiện PostgreSQL và cách chạy trên máy khác | F | Chờ kiểm tra quyền truy cập | Chưa điền |
| D-07 | Điền tên thật cho A–F, xác nhận chủ task và người review | Cả nhóm | Chờ họp | Chưa điền |

Khi sửa quy tắc, ghi mã quyết định, lý do, story/API/schema/test bị ảnh hưởng, người chốt và ngày. Cập nhật spec cùng pull request thực hiện thay đổi đó.

## 6. Đặc tả kỹ thuật

### Công cụ nhóm đang dùng

| Phần | Công cụ | Bằng chứng hoặc mục đích |
| --- | --- | --- |
| Frontend | React + Vite, JavaScript và CSS | Form và bảng lịch sử |
| Backend và API | Python + FastAPI, REST/JSON, Swagger UI | Kiểm tra dữ liệu và xử lý request |
| Database | PostgreSQL | Lưu số đo |
| Truy cập và thay đổi database | SQLAlchemy + Alembic | Model và migration có phiên bản |
| Kiểm thử | pytest + FastAPI TestClient | Kiểm tra API với PostgreSQL test |
| Quản lý code và CI | Git + GitHub + GitHub Actions | Commit, pull request và build/test |
| Bổ sung theo giai đoạn | Figma, diagrams.net, Playwright, Docker Compose | Nhóm ghi bằng chứng khi bắt đầu sử dụng từng công cụ |

### API hiện có

| Method và đường dẫn | Đầu vào | Thành công | Trường hợp lỗi |
| --- | --- | --- | --- |
| `POST /api/measurements` | JSON gồm `weight_kg`, `height_cm` theo S1-R01 | 201 với bản ghi và BMI | 422 input sai, 503 lỗi database |
| `GET /api/measurements` | `limit` từ 1 đến 100, mặc định 30 | 200 với danh sách, mới nhất trước | 422 limit sai, 503 lỗi database |
| `GET /docs` | Mở trên trình duyệt | Swagger UI | Cần backend đang chạy |

Ví dụ request và response thành công dưới đây dùng dữ liệu minh họa. `id` và thời điểm thực tế do hệ thống tạo.

```json
{"weight_kg": 70, "height_cm": 175}
```

```json
{
  "id": 1,
  "weight_kg": 70.0,
  "height_cm": 175.0,
  "bmi": 22.86,
  "created_at": "2026-11-19T04:00:00Z"
}
```

**Thay đổi cần có cho auth** — Giữ hành vi lưu/đọc hợp lệ, thêm kiểm tra phiên và lọc chủ sở hữu cho hai endpoint. B và C ghi trước contract của register/login/logout/current-user/profile/admin vào spec khi chốt D-03, rồi cùng dùng contract đó để code và test.

### Dữ liệu

Hiện `measurements` có `id`, `weight_kg`, `height_cm`, `created_at`. Có ràng buộc giới hạn cân nặng và chiều cao ở database. BMI được tính khi trả kết quả.

| Thành phần cần bổ sung | Yêu cầu thiết kế |
| --- | --- |
| `users` | Khóa chính, email chuẩn hóa duy nhất, hash mật khẩu, role và trạng thái khóa |
| `profiles` | Mỗi user một hồ sơ, trường và giới hạn theo D-02 |
| `sessions` | Gắn user, có thời hạn và thu hồi được khi logout hoặc khóa tài khoản |
| `measurements.user_id` | Khóa ngoại tới users, dùng để kiểm tra quyền sở hữu |

Các bản ghi giả lập cũ đang thiếu chủ sở hữu. Trước migration auth, nhóm cần quyết định cách gán vào tài khoản demo hoặc xử lý chúng với sự đồng ý của người giữ dữ liệu. Ghi cách chuyển đổi và kiểm tra bảo toàn dữ liệu trong task S1-03.

## 7. Bảng công việc

Trạng thái sử dụng gồm **Chưa làm → Đang làm → Chờ review → Hoàn thành**. Dùng **Bị chặn** kèm lý do và người cần hỗ trợ. Các task dưới đây là kế hoạch đề xuất, tên và hạn chưa được thành viên xác nhận.

| Task | Kết quả cần giao | Chủ việc / review đề xuất | Phụ thuộc | Hạn | Trạng thái | Issue hoặc PR |
| --- | --- | --- | --- | --- | --- | --- |
| S1-01 | Chốt AC, giới hạn và D-01/D-02/D-07 | A / E | Họp nhóm | Chưa điền | Chưa làm | Chưa tạo |
| S1-02 | Figma auth/profile/dashboard/admin, trạng thái lỗi | C / A | S1-01 cho phần liên quan | Chưa điền | Chưa làm | Chưa tạo |
| S1-03 | ERD user/profile/session/measurement và migration | B / D | D-03, thiết kế hồ sơ | Chưa điền | Chưa làm | Chưa tạo |
| S1-04 | Contract và backend register/login/logout/current-user | B / D | D-03, S1-03 | Chưa điền | Chưa làm | Chưa tạo |
| S1-05 | Giao diện auth và profile | C + A / E | Contract S1-04, S1-02 | Chưa điền | Chưa làm | Chưa tạo |
| S1-06 | Lọc chủ sở hữu khi lưu/đọc số đo, test truy cập chéo | B + D / A | S1-03, S1-04 | Chưa điền | Chưa làm | Chưa tạo |
| S1-07 | TDEE với nguồn, ví dụ độc lập và unit test | A / E | D-02 | Chưa điền | Chưa làm | Chưa tạo |
| S1-08 | Dashboard BMI/TDEE và biểu đồ lịch sử | C / F | S1-06, S1-07 | Chưa điền | Chưa làm | Chưa tạo |
| S1-09 | Admin khóa/mở khóa và test phiên của user bị khóa | B + C / D | S1-04 | Chưa điền | Chưa làm | Chưa tạo |
| S1-10 | Chạy máy thứ hai, kiểm thử trình duyệt và staging | F / C | D-06, luồng tích hợp | Chưa điền | Chưa làm | Chưa tạo |
| S1-11 | Review Sprint 1, phản hồi và việc cải thiện | A + F / cả nhóm | Kết quả nghiệm thu | Chưa điền | Chưa làm | Chưa tạo |

Người nhận việc có thể chia task lớn thành các issue nhỏ, giữ liên kết về task và story gốc. Mọi thành viên ghi đóng góp cụ thể để nhìn được ai đã phân tích, code, test và review phần nào.

## 8. Quy trình làm việc với AI

### Trước khi bắt đầu

1. Đọc story, AC, rule và code liên quan. Kiểm tra task đã có người nhận chưa.
2. Tạo nhánh cho task, ví dụ `feature/S1-06-measurement-owner`.
3. Gửi AI mã task, mục tiêu, AC, quy tắc đã chốt, file liên quan và kết quả hiện tại.
4. Yêu cầu kế hoạch ngắn, chọn một bước có thể chạy và kiểm tra.

### Khi thực hiện và bàn giao

- Làm từng bước nhỏ. Chạy thử theo AC và giữ kết quả thực tế.
- AI ghi rõ file đã sửa, giả định, câu hỏi còn mở và phần kiểm tra đã thực hiện.
- Nếu thay đổi ảnh hưởng người khác, cập nhật contract/spec và báo vào issue chung.
- Trước khi mở PR, người nhận task giải thích được đoạn code, cách kiểm tra và giới hạn còn lại.
- PR liên kết story, task, nhật ký AI và kết quả test. Người review kiểm tra AC và ghi nhận xét.

Đây là quy trình nhóm đề xuất. Các quyết định phạm vi, công thức và nghiệm thu cần có tên thành viên hoặc giảng viên đã chốt. Kết quả AI tạo được ghi đúng nguồn hỗ trợ trong nhật ký. Dùng dữ liệu giả lập trong prompt và bỏ mật khẩu/token khỏi nội dung chia sẻ.

### Prompt chung cho từng AI

```text
Bạn hỗ trợ dự án Smart Nutrition and Fitness của Group 13.
Hãy đọc docs/PROJECT_SPEC.md phiên bản [phiên bản], mốc code [commit].

Thành viên phụ trách: [tên, vai trò A–F]
Task và story: [mã, link issue nếu có]
Mục tiêu của lần làm này: [một kết quả]
AC cần đáp ứng: [các AC cụ thể]
Quy tắc và quyết định đã chốt: [mã và nội dung]
File liên quan: [đường dẫn tương đối và nội dung cần thiết]
Kết quả trước đó hoặc lỗi hiện tại: [lệnh, output]

Hãy giải thích ngắn rồi đề xuất từng bước nhỏ có cách kiểm tra.
Chỉ rõ giả định và quyết định còn thiếu nếu chúng ảnh hưởng task.
Khi sửa xong, liệt kê file thay đổi, lệnh đã chạy và kết quả thực tế.
Phân biệt kiểm tra đã chạy với kiểm tra cần chạy tiếp.
Tạo đoạn bàn giao theo mẫu mục 10 để thành viên xác minh và đưa vào PR.
```

Nếu AI mới không truy cập được repo, thành viên gửi spec và file liên quan trực tiếp. Khi thay đổi AI hoặc chuyển việc cho người khác, gửi lại mã task, commit, phần đã làm, test đã chạy và blocker để tiếp tục từ đúng trạng thái.

## 9. Kiểm thử và điều kiện hoàn thành

### Đối chiếu yêu cầu với bằng chứng

| Story hoặc nền tảng | Bằng chứng hiện có | Cần bổ sung để nghiệm thu |
| --- | --- | --- |
| Nền tảng lưu số đo | `test_save_then_read` | Khởi động lại app/database rồi đối chiếu bản ghi, ghi người kiểm tra |
| US-H02 | `test_invalid_input_does_not_save` với 9 input sai | Auth, quyền sở hữu và lỗi khi lưu |
| US-H03 | `test_bmi_known_example`, `test_save_then_read` | Luồng riêng của Member và các ca biên theo rule đã chốt |
| US-H05 | `test_newest_first_and_limit` | Lọc theo tài khoản, biểu đồ và giao diện lỗi/empty/loading |
| US-A01, US-A02 | Chưa có | Đăng ký trùng email, login sai, logout, phiên hết hạn và quyền Admin |
| US-H01, US-H04 | Chưa có | Hồ sơ hợp lệ/sai, truy cập chéo, TDEE theo ví dụ độc lập |
| US-AD01 | Chưa có | Member bị từ chối, khóa phiên cũ, mở khóa và bảo toàn dữ liệu |
| CI | EV-01 | Giữ CI thành công ở commit đem trình bày |

Các test hiện có nằm trong [tests/test_measurements.py](../tests/test_measurements.py). Chạy tại thư mục gốc repo trên Windows bằng lệnh sau.

```powershell
.\.venv\Scripts\python.exe manage.py test
```

**Điều kiện Done đề xuất**

- [ ] AC của story hoặc task đã được kiểm tra đầy đủ.
- [ ] Test liên quan đạt và ghi rõ commit, lệnh, kết quả hoặc CI run.
- [ ] Người khác đã review và ghi tên/kết luận trong PR hoặc nhật ký.
- [ ] UI, API và database hoạt động cùng nhau cho luồng liên quan.
- [ ] Spec, API/migration và hướng dẫn được cập nhật khi có thay đổi.
- [ ] Đóng góp của thành viên và AI được ghi đúng mức đã thực hiện.

Review Sprint 1 gồm demo Member, Admin, trường hợp lỗi, thiết kế và test theo các story. Ghi AC còn thiếu, lỗi chưa sửa và kế hoạch xử lý vào biên bản thực tế của buổi review.

## 10. Nhật ký và bằng chứng

### Bằng chứng đã xác định

| Mã | Ngày | Sự kiện | Nguồn kiểm tra | Giới hạn kết luận |
| --- | --- | --- | --- | --- |
| EV-01 | 19/11/2026 | Workflow Build and test hoàn thành success tại commit `a2e3eea` | [GitHub Actions run 44459130985](https://github.com/DozenBro/group13-smart-nutrition-fitness/actions/runs/44459130985) | Có build frontend, migration và test backend. Cần bằng chứng riêng cho review và nghiệm thu story |
| EV-02 | 19/11/2026 | Code khởi tạo số đo/BMI được tạo với hỗ trợ AI theo yêu cầu người dùng | Commit `cb29921`, các file backend/frontend/test/migration trong repo | Nhóm chưa xác nhận phân bổ đóng góp cho A–F |

Lần kiểm tra trước đã ghi nhận 12 bài test đạt trên PostgreSQL và kiểm tra trình duyệt cho lưu/refresh/input sai/màn hình hẹp. Thành viên cần chạy lại trên máy của mình, ghi tên và kết quả khi xác nhận nhận bàn giao.

### Nhật ký thao tác của thành viên và AI

Thêm một mục cho mỗi phiên làm việc tạo ra kết quả cần bàn giao, chẳng hạn chốt quy tắc, sửa code, chạy test hoặc review. Liên kết log chi tiết trong issue/PR khi nội dung dài. Hiện chưa có phiên làm việc nào được xác nhận dưới tên thành viên A–F.

Sao chép mẫu sau, thay phần trong ngoặc và thêm dưới bảng nhật ký.

```text
Mã nhật ký: LOG-[số tăng dần]
Ngày giờ và múi giờ: [thời điểm thực tế]
Thành viên chịu trách nhiệm: [tên và vai trò]
Task / story / issue: [mã và liên kết]
Commit hoặc nhánh bắt đầu: [giá trị thực tế]
Mục tiêu: [kết quả muốn tạo]
AI hỗ trợ: [công cụ, model nếu biết, hoặc không dùng]
Nội dung yêu cầu AI: [tóm tắt hoặc link, bỏ thông tin bí mật]
Phần AI tạo hoặc đề xuất: [cụ thể]
Phần thành viên đã kiểm tra hoặc chỉnh lại: [cụ thể]
File thay đổi: [đường dẫn tương đối]
Lệnh hoặc thao tác kiểm tra: [đã chạy thực tế]
Kết quả và bằng chứng: [pass/fail/chưa chạy, link hoặc output ngắn]
Người review và kết luận: [tên, kết luận, hoặc chờ review]
Commit / PR bàn giao: [liên kết thực tế, hoặc chưa có]
Blocker và bước tiếp theo: [nếu có]
```

| Nhật ký | Thành viên | Task | Kết quả ngắn | Bằng chứng | Trạng thái review |
| --- | --- | --- | --- | --- | --- |
| Chưa có mục thành viên xác nhận | Chưa điền | Chưa điền | Chưa điền | Chưa điền | Chờ điền |

### Lịch sử sửa spec

| Phiên bản | Ngày | Nội dung | Người chốt |
| --- | --- | --- | --- |
| 0.1 | 19/11/2026 | Tạo spec Sprint 1, story/AC, phân công đề xuất, task, quy trình AI và mẫu nhật ký. Đối chiếu code `a2e3eea`. | Soạn với AI theo yêu cầu người dùng, chờ nhóm xác nhận |

## 11. Nguồn đối chiếu

- Kế hoạch nhóm `Sprint_Agile_Group13 1(Agile Project Plan).csv`, WBS 1.1–1.9 cho Sprint 1.
- `Project Description.docx` cho phạm vi sản phẩm và kiến trúc.
- `PROJECT_EXECUTION_GUIDE.md` và bảng công cụ nhóm cho vai trò A–F và hướng triển khai.
- Code tại mốc đã nêu và EV-01 cho bằng chứng thực hiện.

Nhóm đính kèm các tài liệu môn học cần nộp cùng spec theo yêu cầu giảng viên. Khi có mẫu đặc tả chính thức, cập nhật cấu trúc và ghi thay đổi trong lịch sử phiên bản.
