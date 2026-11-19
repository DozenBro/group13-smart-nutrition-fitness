# Sprint 2 Kế hoạch tập và streak

**Bản nháp 0.1 · 19/11/2026 · Trạng thái chưa triển khai**

Đọc [spec tổng](../PROJECT_SPEC.md) và các phần auth/quyền sở hữu của [Sprint 1](SPRINT_1.md). Nội dung dưới đây chi tiết hóa WBS 2.1–2.8 để nhóm refinement. Chủ việc, reviewer và thuật toán là đề xuất cần nhóm xác nhận.

## Mục tiêu và phụ thuộc

**Luồng demo** — Member chọn mục tiêu → nhận lịch tập đã lưu → xem chi tiết buổi tập → ghi nhận hoàn thành → xem streak đúng quy tắc.

Luồng tích hợp dùng tài khoản và quyền sở hữu từ Sprint 1. Trong lúc auth đang hoàn thiện, có thể chuẩn bị dữ liệu bài tập, prototype, template và unit test thuật toán riêng.

| Thông tin | Giá trị |
| --- | --- |
| Ngày bắt đầu / review | Chưa điền |
| Người tổng hợp | Chưa điền |
| Commit demo / kết quả review | Chưa có |
| Đầu vào từ Sprint 1 | Auth, quyền sở hữu, migrations và CI |

## User story và điều kiện nghiệm thu

### US-AD02 Quản lý danh mục bài tập

**Là Admin, tôi muốn quản lý bài tập và loại bài để hệ thống có dữ liệu lập kế hoạch.** Phụ trách D, phối hợp C, review B. Trạng thái Chưa làm. WBS 2.3.

- **AC1** Admin tạo, xem, sửa và xóa hoặc lưu trữ bài tập/loại bài theo chính sách đã chốt.
- **AC2** Tên, loại, dụng cụ, độ khó, hướng dẫn, đơn vị thực hiện và nguồn được kiểm tra theo mẫu dữ liệu.
- **AC3** Member gọi API quản trị bị từ chối. Sửa bài tập không làm mất nội dung của kế hoạch và log đã có.
- **AC4** Nhập được bộ seed đã review. Mốc tạm dùng là 40 bài, cần xác nhận S2-D04.

### US-W01 Nhận và xem kế hoạch theo mục tiêu

**Là Member, tôi muốn có lịch tập phù hợp với mục tiêu để biết mình cần tập gì theo ngày.** Phụ trách D, phối hợp C, review A. Trạng thái Chưa làm. WBS 2.4–2.5.

- **AC1** Ba mục tiêu giảm cân, tăng cơ và duy trì đều tạo được kế hoạch hợp lệ khi có đủ dữ liệu.
- **AC2** Kế hoạch ghi rõ ngày/buổi, bài tập, số hiệp và số lần hoặc thời lượng theo template đã chốt.
- **AC3** Mục tiêu thiếu hoặc sai bị từ chối. Thiếu bài tập phù hợp trả thông báo rõ ràng.
- **AC4** Kế hoạch được lưu, đọc lại sau refresh, chỉ chủ sở hữu truy cập được.
- **AC5** Có thể giải thích bài tập được chọn theo rule/template nào. Cách thay đổi kế hoạch hiện tại tuân theo S2-D01.

### US-W04 Ghi nhận hoàn thành buổi tập

**Là Member, tôi muốn đánh dấu buổi tập đã hoàn thành để lưu lại hoạt động của mình.** Phụ trách D, phối hợp C, review B. Trạng thái Chưa làm. WBS 2.6.

- **AC1** Chỉ chủ sở hữu ghi nhận được buổi tập đúng ngày được phép.
- **AC2** Refresh vẫn thấy trạng thái hoàn thành đã lưu.
- **AC3** Bấm hai lần, gửi lại request hoặc hai request đồng thời đều chỉ tạo một lần hoàn thành cho cùng buổi.
- **AC4** Lỗi lưu không tạo trạng thái thành công giả trên UI. Log và dữ liệu activity nhất quán khi thao tác thất bại.
- **AC5** Ngày hoạt động được xác định theo rule đã chốt để Sprint 3 tái sử dụng.

### US-S01 Xem streak hoạt động

**Là Member, tôi muốn xem chuỗi ngày hoạt động liên tiếp để theo dõi thói quen.** Phụ trách D, review F. Trạng thái Chưa làm. WBS 2.6, mở rộng ở 3.4.

- **AC1** Hoàn thành nhiều buổi trong cùng ngày chỉ đóng góp một ngày hoạt động.
- **AC2** Các ngày liên tiếp nối dài streak, bỏ lỡ một ngày đầy đủ thì chuỗi mới bắt đầu từ lần hoạt động tiếp theo.
- **AC3** Trước khi có hoạt động hôm nay, hiển thị đúng trạng thái theo S2-D03, tránh coi hôm nay là ngày đã bỏ lỡ.
- **AC4** Có test ngày đầu, trùng ngày, ngày liên tiếp, bỏ ngày, qua nửa đêm và request đồng thời.
- **AC5** Streak có thể đối chiếu lại với log, chỉ chủ tài khoản xem được dữ liệu cá nhân.

## Quy tắc và quyết định

| Mã | Nội dung đề xuất | Trạng thái / người theo dõi |
| --- | --- | --- |
| S2-D01 | Dùng template được review cho ba mục tiêu. Chốt lịch, cách chọn bài, đơn vị, nghỉ giữa buổi, cách tạo lại/thay kế hoạch | Chờ D + A chốt |
| S2-D02 | Chốt dữ liệu danh mục, cách xóa/lưu trữ và giữ nội dung lịch sử khi danh mục thay đổi | Chờ D + B chốt |
| S2-D03 | Chốt múi giờ cùng D-05, ngày được phép hoàn thành và cách undo/backdate. Đề xuất dùng ngày server, mỗi ngày tính một lần | Chờ D + A chốt |
| S2-D04 | Xác nhận ký hiệu bị lỗi trong CSV trước số 40. Dùng 40 bài làm mục tiêu seed tạm thời | Chờ A xác nhận |

**Cách tính streak đề xuất** — Lấy các ngày có hoạt động hợp lệ, loại trùng. Nếu hôm nay có hoạt động, đếm chuỗi kết thúc hôm nay. Nếu chưa có hôm nay nhưng có hôm qua, giữ chuỗi kết thúc hôm qua. Các trường hợp còn lại trả 0. Hoạt động mới sau một ngày bỏ lỡ bắt đầu chuỗi 1.

Nhóm chốt S2-D03 trước khi dùng cách tính này làm điều kiện test. Test dùng đồng hồ cố định. Khi bổ sung bữa ăn, Sprint 3 tham chiếu lại rule này.

## Thiết kế và contract dự kiến

| Thành phần | Thiết kế cần giao |
| --- | --- |
| UI | Figma chọn mục tiêu, lịch tuần, chi tiết buổi, trạng thái hoàn thành và lỗi |
| Database | exercises/categories, workout_plans, workout_sessions, plan_items, workout_logs và cách lưu/đọc activity |
| Integrity | Khóa ngoại, chủ sở hữu, quy tắc lịch sử, duy nhất một completion cho user/buổi |
| API | Contract quản trị bài tập, tạo/đọc kế hoạch, hoàn thành buổi và lấy streak |
| Sequence diagram | Trình tự hoàn thành buổi, kiểm tra quyền, ghi log và tính/cập nhật activity |

Các nhóm API trên là phạm vi thiết kế. Người thực hiện ghi method/path, request/response, lỗi và ví dụ vào issue thiết kế trước khi frontend/backend tích hợp. API dùng auth của Sprint 1. Migration phải giữ được dữ liệu tài khoản và số đo đã có.

### Mẫu dữ liệu bài tập

`id`, `name`, `category`, `equipment`, `difficulty`, `instructions`, `goal_tags`, `source`, `review_status`. Liều lượng tập như sets/reps/duration thuộc template hoặc plan item khi phù hợp. Mỗi batch có người nhập và người review khác nhau.

## Task và phân công

| Task | Kết quả cần giao | Chủ việc / review đề xuất | Phụ thuộc | Hạn | Trạng thái | Issue/PR |
| --- | --- | --- | --- | --- | --- | --- |
| S2-01 | Prototype và refinement story, rule workout/streak | C + D / A | Phản hồi Sprint 1 | Chưa điền | Chưa làm | Chưa tạo |
| S2-02 | ERD v2, migration, contract và sequence diagram | D + B / F | S2-D01–S2-D03 | Chưa điền | Chưa làm | Chưa tạo |
| S2-03 | Admin danh mục và bộ seed được review | D + C / E | S2-02, S2-D04 | Chưa điền | Chưa làm | Chưa tạo |
| S2-04 | Sinh kế hoạch và test ba mục tiêu/thiếu dữ liệu | D / A | S2-02, dữ liệu thử | Chưa điền | Chưa làm | Chưa tạo |
| S2-05 | Lịch tuần và chi tiết kế hoạch từ API | C / D | Contract S2-02, S2-04 | Chưa điền | Chưa làm | Chưa tạo |
| S2-06 | Completion và streak, test trùng/ngày/quyền | D / B + F | S2-04, S2-D03 | Chưa điền | Chưa làm | Chưa tạo |
| S2-07 | Test tích hợp, regression Sprint 1, migration bảo toàn dữ liệu | F + A / B | Luồng tích hợp | Chưa điền | Chưa làm | Chưa tạo |
| S2-08 | Review, phản hồi, quyết định challenge và kế hoạch Sprint 3 | A + F / cả nhóm | S2-07, D-04 | Chưa điền | Chưa làm | Chưa tạo |

## Kiểm thử và review

| Story | Kiểm tra cần có | Bằng chứng hiện tại |
| --- | --- | --- |
| US-AD02 | Admin CRUD, Member bị từ chối, seed nhập lại, lịch sử khi sửa/xóa | Chưa có |
| US-W01 | Ba mục tiêu, goal sai/rỗng, thiếu bài, refresh, đọc kế hoạch của người khác | Chưa có |
| US-W04 | Thành công, trùng request, đồng thời, ngày sai, thất bại transaction | Chưa có |
| US-S01 | Trùng ngày, liên tiếp, bỏ ngày, nửa đêm, hôm nay chưa hoạt động | Chưa có |
| Regression | Auth/health còn đạt, migration giữ dữ liệu cũ | Chưa có |

- [ ] Áp dụng [điều kiện Done chung](../PROJECT_SPEC.md#điều-kiện-hoàn-thành) cho từng task/story.
- [ ] Demo goal → kế hoạch → completion → streak, rồi thử trùng request và input sai.
- [ ] Mở rule, sequence diagram, test và CI của commit demo để giải thích.
- [ ] Ghi quyết định D-04 trước khi đưa challenge vào Sprint 3.
- [ ] Ghi phản hồi thật và một cải thiện cho sprint sau.

## Nhật ký và bàn giao AI

Dùng [prompt chung](../PROJECT_SPEC.md#prompt-dùng-chung). Hiện chưa có phiên thực hiện Sprint 2 được xác nhận.

| Nhật ký | Ngày / thành viên | Task | Kết quả | Commit/PR/test | Reviewer và kết luận |
| --- | --- | --- | --- | --- | --- |
| Chưa có | Chưa điền | Chưa điền | Chưa điền | Chưa điền | Chưa điền |

```text
Nhật ký: S2-LOG-[số]
Ngày giờ và múi giờ: [thực tế]
Thành viên / task / story / issue: [tên và mã]
Commit bắt đầu: [commit]
Mục tiêu và AC: [một kết quả và điều kiện kiểm tra]
AI đã hỗ trợ: [công cụ/model, yêu cầu, đề xuất hoặc code]
Thành viên đã kiểm tra/chỉnh lại: [cụ thể]
File thay đổi: [đường dẫn tương đối]
Lệnh/kiểm tra đã chạy và kết quả: [thực tế hoặc chưa chạy]
Bằng chứng / PR: [link hoặc chưa có]
Reviewer và kết luận: [tên/kết luận hoặc chờ review]
Blocker / bước tiếp theo: [nội dung]
```

## Lịch sử tài liệu

| Phiên bản | Ngày | Thay đổi | Xác nhận |
| --- | --- | --- | --- |
| 0.1 | 19/11/2026 | Chi tiết hóa WBS 2.1–2.8, giữ mã story từ hướng dẫn dự án | Bản nháp soạn với AI, chờ nhóm chốt |
