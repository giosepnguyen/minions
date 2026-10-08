# Báo cáo phần việc Backend – AI Assessment

## 1. Phạm vi công việc

Triển khai Backend API cho chức năng Health Check và AI Assessment theo format đã thống nhất với phần AI.

Phạm vi hiện tại tập trung vào **Mock API**, để Web có thể tích hợp trước khi AI Model thật sẵn sàng.

## 2. API đã triển khai

**Method:** `POST`

**Endpoint:**
`/api/v1/assessment/evaluate`

**Production URL:**
`https://minions-qtug.onrender.com/api/v1/assessment/evaluate`

## 3. Request / Response

Đã tạo model cho:

- `AIAssessmentInput`
- `AIAssessmentOutput`

Request gồm:
- `sessionId`
- `userContext`
- `conversationHistory`

Response gồm:
- `sessionId`
- `status`
- `confidenceScore`
- `nextAction`

## 4. Mock API đã triển khai

Đã hỗ trợ 3 trường hợp:

### Mock 1 – NEEDS_CLARIFICATION
Khi chưa đủ thông tin, Backend trả về một câu hỏi tiếp theo.

Ví dụ:
`How long have you been experiencing these symptoms?`

### Mock 2 – COMPLETED
Khi đủ dữ liệu mẫu, Backend trả về kết quả assessment gồm:
- `triageLevel`
- `possibleConditions`
- `explanation`
- `supportingFactors`
- `recommendations`
- `warningSigns`

### Mock 3 – EMERGENCY_REDIRECTIONS
Khi phát hiện từ khóa khẩn cấp, Backend trả về:
- `triageLevel = CRITICAL`
- hướng dẫn khẩn cấp
- warning signs
- thông tin cơ sở cấp cứu

## 5. Kiểm thử

Đã kiểm thử thành công:

**Local**
- `NEEDS_CLARIFICATION` ✅
- `COMPLETED` ✅
- `EMERGENCY_REDIRECTIONS` ✅

**Render Production**
- `NEEDS_CLARIFICATION` ✅
- `COMPLETED` ✅
- `EMERGENCY_REDIRECTIONS` ✅

Swagger/OpenAPI cũng đã hiển thị schema `AIAssessmentOutput`.

## 6. Các API cũ được giữ nguyên

Không thay đổi các API đã hoàn thành:

- `GET /api/diseases`
- `GET /api/symptoms`
- `GET /api/diseases-by-symptoms`

## 7. Trạng thái hiện tại

**Đã hoàn thành:**
- Request schema
- Response schema
- Mock Assessment API
- 3 mock response
- Kiểm thử local
- Deploy lên Render
- Kiểm thử production

**Để xử lý sau:**
- Kết nối AI Model thật
- Hoàn thiện hội thoại AI nhiều lượt
- Tích hợp đầy đủ Web AI Chat với Backend
- Mở rộng logic assessment

## 8. Kết luận

Phần Backend Mock AI Assessment API đã được triển khai, kiểm thử và đưa lên môi trường production, sẵn sàng để Web tích hợp trước khi AI Model thật được kết nối.
