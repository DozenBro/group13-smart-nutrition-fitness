# Sprint 1 Nền tảng và theo dõi sức khỏe

**Bản nháp 0.2 · 19/11/2026 · Trạng thái đang thực hiện một phần**

Đọc [spec tổng](../PROJECT_SPEC.md) trước khi nhận việc. Mốc code đối chiếu là `7e0f064`. Ngày bắt đầu, ngày review và tên thành viên cần nhóm xác nhận. Phạm vi dựa trên WBS 1.1–1.9 của kế hoạch nhóm.

## Mục tiêu và mốc hiện tại

**Luồng cần nghiệm thu** — Member đăng ký, đăng nhập, cập nhật hồ sơ, lưu số đo của mình và xem BMI/TDEE, lịch sử và biểu đồ. Admin xem danh sách, khóa/mở khóa tài khoản.

**Đã có** — Demo số đo/BMI dùng dữ liệu chung, PostgreSQL và migration, API có kiểm tra đầu vào, 12 trường hợp test và CI thành công. **Cần hoàn thiện** — Tài khoản, quyền sở hữu, hồ sơ/TDEE, biểu đồ, admin và nghiệm thu của nhóm.

**Ưu tiên triển khai** — Chốt D-03 → thiết kế và migration auth → register/login/logout → bảo vệ số đo theo user → hồ sơ/TDEE → biểu đồ và admin → test tích hợp và review. Có thể thực hiện thiết kế UI và tìm nguồn công thức song song.

| Mốc nhóm cần điền | Giá trị |
| --- | --- |
| Ngày bắt đầu | Chưa điền |
| Ngày review | Chưa điền |
| Commit dùng để demo | Chưa điền khi nghiệm thu |
| Người tổng hợp | Chưa điền |

## User story và điều kiện nghiệm thu

**AC** là điều kiện nghiệm thu có thể kiểm tra. Một story chỉ được chuyển sang Done sau khi đáp ứng toàn bộ AC và điều kiện Done chung. Mỗi story giữ mã ổn định để liên kết code, test và nhật ký.

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

## Quy tắc của Sprint 1

### Quy tắc Sprint 1


| Mã    | Quy tắc                                                                                                      | Tình trạng                                                 |
| ------ | ------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------ |
| S1-R01 | Cân nặng lớn hơn 0 và tối đa 500 kg. Chiều cao từ 50 đến 250 cm. Tối đa 2 số thập phân.       | Đã dùng trong bản demo, nhóm cần xác nhận giới hạn |
| S1-R02 | BMI = kg / (cm / 100)². Backend làm tròn kết quả hiển thị tới 2 số thập phân bằng ROUND_HALF_UP.  | Có code và test ví dụ                                    |
| S1-R03 | Thời điểm ghi nhận do server tạo, lưu kiểu timezone-aware. Hiện UI dùng giờ máy người xem.       | Có trong demo, cách hiển thị cuối chờ D-05             |
| S1-R04 | Member đọc/ghi dữ liệu riêng qua danh tính đã xác thực ở backend.                                  | Yêu cầu mục tiêu, chưa triển khai                      |
| S1-R05 | Admin quản lý trạng thái tài khoản, tài khoản khóa bị từ chối truy cập cả với phiên cũ.      | Yêu cầu mục tiêu, chưa triển khai                      |
| S1-R06 | Dữ liệu sai trả HTTP 422 và thông tin lỗi. Request chưa đăng nhập trả 401, thiếu quyền trả 403. | 422 có sẵn, 401/403 cần triển khai                       |
| S1-R07 | Database thử nghiệm là`fitness_test`, tách khỏi `fitness_demo`.                                          | Có trong lệnh test                                         |

Các quyết định D-01–D-07 được cập nhật tại [bảng quyết định chung](../PROJECT_SPEC.md#quyết-định-cần-chốt). Sửa quy tắc tại file sprint này và ghi lịch sử thay đổi ở cuối file.

## API và dữ liệu

| Method và đường dẫn | Đầu vào                                    | Thành công                            | Trường hợp lỗi               |
| ------------------------ | --------------------------------------------- | --------------------------------------- | -------------------------------- |
| `POST /api/measurements` | JSON gồm`weight_kg`, `height_cm` theo S1-R01 | 201 với bản ghi và BMI               | 422 input sai, 503 lỗi database |
| `GET /api/measurements`  | `limit` từ 1 đến 100, mặc định 30       | 200 với danh sách, mới nhất trước | 422 limit sai, 503 lỗi database |
| `GET /docs`              | Mở trên trình duyệt                       | Swagger UI                              | Cần backend đang chạy         |

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


| Thành phần cần bổ sung | Yêu cầu thiết kế                                                                    |
| -------------------------- | --------------------------------------------------------------------------------------- |
| `users`                    | Khóa chính, email chuẩn hóa duy nhất, hash mật khẩu, role và trạng thái khóa |
| `profiles`                 | Mỗi user một hồ sơ, trường và giới hạn theo D-02                               |
| `sessions`                 | Gắn user, có thời hạn và thu hồi được khi logout hoặc khóa tài khoản       |
| `measurements.user_id`     | Khóa ngoại tới users, dùng để kiểm tra quyền sở hữu                           |

Các bản ghi giả lập cũ đang thiếu chủ sở hữu. Trước migration auth, nhóm cần quyết định cách gán vào tài khoản demo hoặc xử lý chúng với sự đồng ý của người giữ dữ liệu. Ghi cách chuyển đổi và kiểm tra bảo toàn dữ liệu trong task S1-03.

## Công việc và phân công

Trạng thái sử dụng gồm **Chưa làm → Đang làm → Chờ review → Hoàn thành**. Dùng **Bị chặn** kèm lý do và người cần hỗ trợ. Các task dưới đây là kế hoạch đề xuất, tên và hạn chưa được thành viên xác nhận.


| Task  | Kết quả cần giao                                             | Chủ việc / review đề xuất | Phụ thuộc                | Hạn         | Trạng thái | Issue hoặc PR |
| ----- | --------------------------------------------------------------- | ------------------------------ | -------------------------- | ------------ | ------------ | -------------- |
| S1-01 | Chốt AC, giới hạn và D-01/D-02/D-07                         | A / E                          | Họp nhóm                 | Chưa điền | Chưa làm   | Chưa tạo     |
| S1-02 | Figma auth/profile/dashboard/admin, trạng thái lỗi           | C / A                          | S1-01 cho phần liên quan | Chưa điền | Chưa làm   | Chưa tạo     |
| S1-03 | ERD user/profile/session/measurement và migration              | B / D                          | D-03, thiết kế hồ sơ   | Chưa điền | Chưa làm   | Chưa tạo     |
| S1-04 | Contract và backend register/login/logout/current-user         | B / D                          | D-03, S1-03                | Chưa điền | Chưa làm   | Chưa tạo     |
| S1-05 | Giao diện auth và profile                                     | C + A / E                      | Contract S1-04, S1-02      | Chưa điền | Chưa làm   | Chưa tạo     |
| S1-06 | Lọc chủ sở hữu khi lưu/đọc số đo, test truy cập chéo | B + D / A                      | S1-03, S1-04               | Chưa điền | Chưa làm   | Chưa tạo     |
| S1-07 | TDEE với nguồn, ví dụ độc lập và unit test              | A / E                          | D-02                       | Chưa điền | Chưa làm   | Chưa tạo     |
| S1-08 | Dashboard BMI/TDEE và biểu đồ lịch sử                     | C / F                          | S1-06, S1-07               | Chưa điền | Chưa làm   | Chưa tạo     |
| S1-09 | Admin khóa/mở khóa và test phiên của user bị khóa       | B + C / D                      | S1-04                      | Chưa điền | Chưa làm   | Chưa tạo     |
| S1-10 | Chạy máy thứ hai, kiểm thử trình duyệt và staging       | F / C                          | D-06, luồng tích hợp    | Chưa điền | Chưa làm   | Chưa tạo     |
| S1-11 | Review Sprint 1, phản hồi và việc cải thiện               | A + F / cả nhóm              | Kết quả nghiệm thu      | Chưa điền | Chưa làm   | Chưa tạo     |

Người nhận việc có thể chia task lớn thành các issue nhỏ, giữ liên kết về task và story gốc. Mọi thành viên ghi đóng góp cụ thể để nhìn được ai đã phân tích, code, test và review phần nào.

## Kiểm thử và nghiệm thu

### Đối chiếu yêu cầu với bằng chứng


| Story hoặc nền tảng  | Bằng chứng hiện có                              | Cần bổ sung để nghiệm thu                                                   |
| ----------------------- | --------------------------------------------------- | -------------------------------------------------------------------------------- |
| Nền tảng lưu số đo | `test_save_then_read`                               | Khởi động lại app/database rồi đối chiếu bản ghi, ghi người kiểm tra |
| US-H02                  | `test_invalid_input_does_not_save` với 9 input sai | Auth, quyền sở hữu và lỗi khi lưu                                          |
| US-H03                  | `test_bmi_known_example`, `test_save_then_read`     | Luồng riêng của Member và các ca biên theo rule đã chốt                 |
| US-H05                  | `test_newest_first_and_limit`                       | Lọc theo tài khoản, biểu đồ và giao diện lỗi/empty/loading              |
| US-A01, US-A02          | Chưa có                                           | Đăng ký trùng email, login sai, logout, phiên hết hạn và quyền Admin    |
| US-H01, US-H04          | Chưa có                                           | Hồ sơ hợp lệ/sai, truy cập chéo, TDEE theo ví dụ độc lập              |
| US-AD01                 | Chưa có                                           | Member bị từ chối, khóa phiên cũ, mở khóa và bảo toàn dữ liệu       |
| CI                      | EV-01                                               | Giữ CI thành công ở commit đem trình bày                                  |

Các test hiện có nằm trong [tests/test_measurements.py](../../tests/test_measurements.py). Chạy tại thư mục gốc repo trên Windows bằng lệnh sau.

```powershell
.\.venv\Scripts\python.exe manage.py test
```

Áp dụng [điều kiện Done chung](../PROJECT_SPEC.md#điều-kiện-hoàn-thành). Một story có auth và dữ liệu riêng cần đạt các AC đó trước khi ghi hoàn thành.

### Kịch bản review

- [ ] Mở backlog và chỉ ra story đã đạt, một phần hoặc chưa đạt.
- [ ] Demo đăng ký/login, lưu số đo hợp lệ và xem lại sau refresh.
- [ ] Demo input sai, truy cập chéo tài khoản bị từ chối và logout vô hiệu phiên cũ.
- [ ] Đối chiếu BMI/TDEE với ví dụ độc lập, mở biểu đồ lịch sử.
- [ ] Demo Member bị từ chối API admin, Admin khóa/mở khóa và kiểm tra phiên cũ.
- [ ] Mở ERD, API contract, migration và kết quả test/CI của commit demo.
- [ ] Ghi phản hồi, lỗi còn mở và hành động cải thiện cho Sprint 2.

## Nhật ký và bằng chứng

### Bằng chứng đã xác định


| Mã   | Ngày      | Sự kiện                                                                              | Nguồn kiểm tra                                                                                                       | Giới hạn kết luận                                                                                     |
| ----- | ---------- | -------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------- |
| EV-01 | 19/11/2026 | Workflow Build and test hoàn thành success tại commit`a2e3eea`                      | [GitHub Actions run 44459130985](https://github.com/DozenBro/group13-smart-nutrition-fitness/actions/runs/44459130985) | Có build frontend, migration và test backend. Cần bằng chứng riêng cho review và nghiệm thu story |
| EV-02 | 19/11/2026 | Code khởi tạo số đo/BMI được tạo với hỗ trợ AI theo yêu cầu người dùng | Commit`cb29921`, các file backend/frontend/test/migration trong repo                                                  | Nhóm chưa xác nhận phân bổ đóng góp cho A–F                                                     |

Lần kiểm tra trước đã ghi nhận 12 bài test đạt trên PostgreSQL và kiểm tra trình duyệt cho lưu/refresh/input sai/màn hình hẹp. Thành viên cần chạy lại trên máy của mình, ghi tên và kết quả khi xác nhận nhận bàn giao.

### Nhật ký thao tác của thành viên và AI

Thêm một mục cho mỗi phiên làm việc tạo ra kết quả cần bàn giao, chẳng hạn chốt quy tắc, sửa code, chạy test hoặc review. Liên kết log chi tiết trong issue/PR khi nội dung dài. Hiện chưa có phiên làm việc nào được xác nhận dưới tên thành viên A–F.

Điền mẫu dưới đây hoặc liên kết bản bàn giao trong issue/PR. Mã log cho sprint này dùng tiền tố S1-LOG.

```text
Mã nhật ký: S1-LOG-[số tăng dần]
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


| Nhật ký                              | Thành viên | Task         | Kết quả ngắn | Bằng chứng | Trạng thái review |
| -------------------------------------- | ------------ | ------------ | --------------- | ------------ | ------------------- |
| Chưa có mục thành viên xác nhận | Chưa điền | Chưa điền | Chưa điền    | Chưa điền | Chờ điền         |

## Lịch sử tài liệu

| Phiên bản | Ngày | Nội dung | Người xác nhận |
| --- | --- | --- | --- |
| 0.1 | 19/11/2026 | Story, AC và bảng việc ban đầu nằm trong PROJECT_SPEC.md, đối chiếu code a2e3eea | Soạn với AI, chờ nhóm xác nhận |
| 0.2 | 19/11/2026 | Tách Sprint 1, giữ story/AC/task và bằng chứng đã có, thêm kịch bản review | Soạn với AI, chờ nhóm xác nhận |
