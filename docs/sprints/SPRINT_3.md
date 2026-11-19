# Sprint 3 Bữa ăn Việt Nam và phát hành

**Bản nháp 0.1 · 19/11/2026 · Trạng thái chưa triển khai**

Đọc [spec tổng](../PROJECT_SPEC.md), TDEE/quyền sở hữu ở [Sprint 1](SPRINT_1.md) và streak/completion ở [Sprint 2](SPRINT_2.md). Phạm vi dựa trên WBS 3.1–3.7. Checklist nghiệm thu cuối tham chiếu WBS 4.1–4.2.

## Mục tiêu và phụ thuộc

**Luồng demo** — Member có hồ sơ và target năng lượng → nhập sở thích/ngân sách → nhận kế hoạch bữa ăn → ghi nhận hoàn thành → activity/streak cập nhật. Toàn bộ health → workout → meal chạy được trên staging.

Dùng auth và dữ liệu hồ sơ từ Sprint 1, tái sử dụng rule ngày/streak từ Sprint 2. Có thể thu thập dữ liệu và thử thuật toán meal độc lập từ sớm. Trạng thái task, tên và lịch bên dưới đang chờ nhóm xác nhận.

| Thông tin | Giá trị |
| --- | --- |
| Ngày bắt đầu / review | Chưa điền |
| Hạn đóng băng tính năng / nghiệm thu cuối | Chưa điền |
| URL staging / commit phát hành | Chưa có |
| Người tổng hợp / người nghiệm thu | Chưa điền |

## User story và điều kiện nghiệm thu

### US-AD03 Quản lý món ăn Việt Nam

**Là Admin, tôi muốn quản lý món ăn và thông tin dinh dưỡng để có dữ liệu đáng tin cậy cho gợi ý bữa ăn.** Phụ trách E, phối hợp C, review A. Trạng thái Chưa làm. WBS 3.2.

- **AC1** Admin tạo, đọc, sửa và xóa/lưu trữ món theo chính sách giữ lịch sử đã chốt.
- **AC2** Mỗi món có khẩu phần, kcal, protein/carb/fat và giá VND cùng một cơ sở khẩu phần, có nguồn dinh dưỡng và bối cảnh giá.
- **AC3** Dữ liệu thiếu đơn vị hoặc không hợp lệ bị từ chối. Member gọi API quản trị bị từ chối.
- **AC4** Có bộ seed được review, mốc tạm 60 món cần xác nhận S3-D03. Nhập lại cùng seed không tạo bản ghi trùng.
- **AC5** Sửa/xóa món không làm thay đổi thông tin của kế hoạch đã lưu trước đó.

### US-M01 Nhận và xem gợi ý bữa ăn

**Là Member, tôi muốn nhận gợi ý món Việt theo target năng lượng, sở thích và ngân sách để có kế hoạch phù hợp với các lựa chọn của mình.** Phụ trách E, phối hợp C, review D. Trạng thái Chưa làm. WBS 3.3.

- **AC1** Input hợp lệ và có đủ dữ liệu tạo được kế hoạch trong giới hạn kcal, sở thích và ngân sách đã chốt.
- **AC2** Thiếu target/hồ sơ thì chỉ rõ thông tin cần bổ sung. Ngân sách hoặc sở thích sai bị từ chối.
- **AC3** Không có tổ hợp thỏa tất cả điều kiện thì trả no-match với hướng dẫn điều chỉnh lựa chọn.
- **AC4** Kế hoạch hiển thị món, lượng/khẩu phần, tổng kcal và giá. Dữ liệu đủ để giải thích vì sao tổ hợp được chọn.
- **AC5** Kế hoạch được lưu và đọc lại sau refresh, chỉ người sở hữu xem được. Lưu đầu vào/rule và giá trị món cần thiết để giữ lịch sử.

### US-M02 Ghi nhận bữa ăn và cập nhật hoạt động

**Là Member, tôi muốn đánh dấu bữa ăn đã hoàn thành để ghi nhận thói quen cùng với tập luyện.** Phụ trách E + D, phối hợp C, review B. Trạng thái Chưa làm. WBS 3.4.

- **AC1** Thành viên chỉ hoàn thành bữa ăn thuộc kế hoạch của mình, theo ngày được phép.
- **AC2** Gửi lại request hoặc request đồng thời chỉ ghi nhận một completion cho cùng bữa.
- **AC3** Workout và meal cùng ngày chỉ đóng góp một ngày cho streak chung theo rule đã chốt.
- **AC4** Refresh hiển thị đúng log và streak, lỗi lưu không tạo trạng thái hoàn thành giả.
- **AC5** Nếu hỗ trợ undo, kết quả activity được tính lại từ các log còn hợp lệ theo S2-D03/S3-D02.

### US-C01 Challenge cơ bản

**Là Admin, tôi muốn quản lý challenge; là Member, tôi muốn xem tiến độ của mình theo mục tiêu challenge.** Trạng thái Chờ D-04. WBS 3.5. Chủ việc/reviewer chờ nhóm phân công nếu được đưa vào sprint.

- **AC1** Admin quản lý tên, khoảng ngày và mục tiêu, Member chỉ truy cập chức năng được phép.
- **AC2** Tiến độ tính từ log có thật, không tính lại hai lần cùng hoạt động/ngày theo rule challenge.
- **AC3** Thành viên xem được tiến độ của mình và kết quả đạt/chưa đạt đúng theo rule.

Ghi quyết định giữ hoặc hoãn story này cùng người chốt và lý do. Nếu bắt buộc theo giảng viên, cập nhật kế hoạch trước khi nghiệm thu.

## Quy tắc và quyết định

| Mã | Cần thống nhất | Người theo dõi / trạng thái |
| --- | --- | --- |
| S3-D01 | Target kcal lấy từ đâu, có điều chỉnh theo goal không, dung sai ±10% trong CSV có được chấp nhận không, biên có tính bằng không | A + E, chờ chốt |
| S3-D02 | Các preference được hỗ trợ, ngân sách/ngày, bữa sáng/trưa/tối, lượng khẩu phần và món lặp, cách đổi lại kế hoạch/undo | E + D, chờ chốt |
| S3-D03 | Xác nhận ký hiệu lỗi trước số 60, chuẩn nguồn/khẩu phần/giá, cách lưu trữ món | A + E, chờ chốt, tạm dùng 60 món |
| S3-D04 | Chốt môi trường staging, ngày feature freeze, kịch bản UAT và người nghiệm thu | F + A, chờ chốt cùng D-06 |

**Thuật toán đề xuất** — Lọc món hợp lệ theo preference và slot bữa. Duyệt tổ hợp với khẩu phần đã chốt. Giữ các tổ hợp đạt ngân sách và giới hạn kcal. Chọn tổ hợp gần target nhất, rồi giá thấp hơn, rồi ID ổn định để giải thích kết quả. Trả no-match khi không có tổ hợp đạt.

Ví dụ fixture phần mềm, giả sử đã chốt target 2.000 kcal, dung sai 10% và ngân sách 100.000 VND. Khoảng chấp nhận là 1.800–2.200 kcal. Tổ hợp phù hợp preference, 1.950 kcal và 90.000 VND đạt. Tổ hợp 2.000 kcal nhưng 110.000 VND bị loại. Đây là ví dụ kiểm tra constraint của thuật toán.

Streak tiếp tục theo S2-D03. Rule ăn/tập dùng chung phải được cập nhật cùng test ở cả hai module khi thay đổi.

## Thiết kế và dữ liệu

| Thành phần | Kết quả thiết kế cần giao |
| --- | --- |
| UI | Preference, ngân sách, gợi ý kế hoạch, chi tiết, no-match, completion và lỗi |
| Database | foods, meal_plans, meal_plan_items, meal_logs và liên kết activity/user |
| Lịch sử | Lưu giá trị khẩu phần/kcal/giá và rule/đầu vào cần thiết khi sinh kế hoạch |
| API | Contract admin foods, tạo/đọc kế hoạch, meal completion và streak chung |
| Integrity | Khóa ngoại, quyền sở hữu, không trùng completion, giao dịch log/activity nhất quán |

Người thực hiện ghi method/path, request/response, auth và mã lỗi trong issue thiết kế trước khi tích hợp. Đây là contract cần xây trong sprint, hiện code chưa có nhóm API này.

**Mẫu món ăn** gồm `id`, tên Việt, mô tả/khối lượng khẩu phần, kcal, protein/carb/fat theo cùng khẩu phần, giá VND/khẩu phần, meal slot, preference tag, nguồn dinh dưỡng, nguồn/bối cảnh/ngày giá và người review. Giá ước tính được ghi rõ. Dữ liệu thiếu được bổ sung hoặc thay món có nguồn phù hợp trước khi dùng trong seed.

## Task và phân công

| Task | Kết quả cần giao | Chủ việc / review đề xuất | Phụ thuộc | Hạn | Trạng thái | Issue/PR |
| --- | --- | --- | --- | --- | --- | --- |
| S3-01 | Prototype, rule meal và các fixture thành công/no-match | E + C / A | D-02, S3-D01/S3-D02 | Chưa điền | Chưa làm | Chưa tạo |
| S3-02 | Schema/migration, contract, admin food và seed có nguồn | E + B / D | S3-D03 | Chưa điền | Chưa làm | Chưa tạo |
| S3-03 | Thuật toán gợi ý và màn hình kế hoạch đã lưu | E + C / D | S3-01, dữ liệu S3-02 | Chưa điền | Chưa làm | Chưa tạo |
| S3-04 | Meal completion và streak ăn/tập chung | E + D / B | S3-03, rule Sprint 2 | Chưa điền | Chưa làm | Chưa tạo |
| S3-05 | Challenge nếu được xác nhận trong phạm vi | Chờ phân công | D-04 | Chưa điền | Chờ quyết định | Chưa tạo |
| S3-06 | Regression, kiểm tra quyền và lỗi xuyên module | F + cả nhóm / B | Health/workout/meal tích hợp | Chưa điền | Chưa làm | Chưa tạo |
| S3-07 | Staging, hướng dẫn người dùng, demo và freeze bản release candidate | F + A / C | D-06, S3-D04, S3-06 | Chưa điền | Chưa làm | Chưa tạo |
| S3-08 | UAT cuối, sửa lỗi, tag và tài liệu bàn giao | Cả nhóm / người nghiệm thu chờ chốt | Bản release candidate | Chưa điền | Chưa làm | Chưa tạo |

S3-08 nối với mốc nghiệm thu cuối WBS 4.1–4.2. Nhóm điền lịch của mốc này theo ngày nộp thực tế.

## Kiểm thử, review và bàn giao

| Nhóm kiểm tra | Các ca cần có | Bằng chứng hiện tại |
| --- | --- | --- |
| Dữ liệu | Đơn vị/khẩu phần, nguồn, thiếu trường, âm, import trùng và sửa giá trong lịch sử | Chưa có |
| Meal search | Có lời giải, no-match, preference sai, thiếu target, budget bằng biên và kcal ở hai biên | Chưa có |
| Completion | Thành công, request lặp/đồng thời, người khác, ngày sai và lỗi transaction | Chưa có |
| Streak chung | Workout + meal cùng ngày, chỉ meal, chỉ workout, bỏ ngày và qua nửa đêm | Chưa có |
| Regression | Auth/health/workout còn hoạt động, migration giữ dữ liệu, Member/Admin đúng quyền | Chưa có |
| Release | Fresh setup, staging, restart giữ dữ liệu, backup/restore và UAT theo AC | Chưa có |

- [ ] Đạt [điều kiện Done chung](../PROJECT_SPEC.md#điều-kiện-hoàn-thành) cho phạm vi đã chốt.
- [ ] Demo health → workout → meal trên staging và một trường hợp no-match.
- [ ] Review lỗi, không còn lỗi critical/high đang mở theo tiêu chí kế hoạch.
- [ ] Ghi quyết định challenge, URL staging, commit và kết quả CI/test.
- [ ] Chốt release candidate và ghi các thay đổi tiếp theo vào bug/issue.

### Nghiệm thu cuối và tài liệu nộp

- [ ] Người nghiệm thu thực hiện kịch bản đã thống nhất và ghi kết quả thực tế.
- [ ] Có README chạy được từ máy khác, hướng dẫn sử dụng, ERD, sơ đồ kiến trúc và danh sách API khớp code.
- [ ] Có bảng story → task → commit/PR → test → kết quả nghiệm thu.
- [ ] Có báo cáo sprint, phản hồi và hành động retrospective thực tế.
- [ ] Có tag/commit cuối, cách backup/khôi phục và danh sách giới hạn/lỗi đã công bố.
- [ ] Sáu thành viên giải thích được đóng góp của mình, phần AI hỗ trợ và kiểm tra đã làm.

## Nhật ký và bàn giao AI

Dùng [prompt chung](../PROJECT_SPEC.md#prompt-dùng-chung). Hiện chưa có phiên thực hiện Sprint 3 được xác nhận.

| Nhật ký | Ngày / thành viên | Task | Kết quả | Commit/PR/test | Reviewer và kết luận |
| --- | --- | --- | --- | --- | --- |
| Chưa có | Chưa điền | Chưa điền | Chưa điền | Chưa điền | Chưa điền |

```text
Nhật ký: S3-LOG-[số]
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
| 0.1 | 19/11/2026 | Chi tiết hóa WBS 3.1–3.7 và nghiệm thu WBS 4.1–4.2 | Bản nháp soạn với AI, chờ nhóm chốt |
