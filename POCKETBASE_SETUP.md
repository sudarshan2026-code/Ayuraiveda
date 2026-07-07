# PocketBase Setup Guide — AyurAI Veda™

## 1. Download & Run PocketBase

Download from: https://pocketbase.io/docs/

```bash
# Windows — place pocketbase.exe in Ayurveda/ folder
pocketbase.exe serve
# Runs at: http://127.0.0.1:8090
# Admin UI: http://127.0.0.1:8090/_/
```

## 2. Create Admin Account
Open http://127.0.0.1:8090/_/ and create your admin account.

## 3. Create Collections

### Collection: `users` (use built-in Auth collection)
PocketBase has a built-in `users` auth collection. Add these extra fields:
| Field        | Type   | Required |
|--------------|--------|----------|
| name         | Text   | ✅       |
| role         | Select | ✅       | Values: user, doctor, admin
| phone        | Text   |          |
| age          | Number |          |
| gender       | Select |          | Values: Male, Female, Other
| city         | Text   |          |
| blood_group  | Text   |          |
| bio          | Text   |          |
| qualification| Text   |          | (doctor)
| specialization| Text  |          | (doctor)
| experience   | Number |          | (doctor)
| hospital     | Text   |          | (doctor)
| reg_number   | Text   |          | (doctor)

### Collection: `clinical_assessments`
| Field               | Type     | Required |
|---------------------|----------|----------|
| user_id             | Relation | ✅       | → users
| assessment_answers  | JSON     | ✅       |
| dosha_result        | Text     | ✅       |
| ai_analysis         | JSON     |          |
| report_status       | Select   |          | Values: completed, pending

### Collection: `notifications`
| Field    | Type     | Required |
|----------|----------|----------|
| user_id  | Relation | ✅       | → users
| title    | Text     | ✅       |
| message  | Text     | ✅       |
| is_read  | Bool     |          | Default: false

### Collection: `doctors`
| Field          | Type     | Required |
|----------------|----------|----------|
| user_id        | Relation | ✅       | → users
| doctor_name    | Text     | ✅       |
| specialization | Text     |          |
| availability   | Text     |          |
| contact_info   | Text     |          |

## 4. Set API Rules

### users
- List/View: `@request.auth.id != ""`
- Create: `""` (public — for registration)
- Update: `@request.auth.id = id`
- Delete: `@request.auth.id = id`

### clinical_assessments
- List/View: `@request.auth.id = user_id`
- Create: `@request.auth.id != ""`
- Update: `@request.auth.id = user_id`

### notifications
- List/View: `@request.auth.id = user_id`
- Create: `@request.auth.id != ""`
- Update: `@request.auth.id = user_id`

### doctors
- List/View: `""` (public)
- Create/Update: `@request.auth.id = user_id`

## 5. Install SDK & Run Frontend

```bash
cd frontend
npm install
npm run dev
```

## 6. Environment Variable
The `.env` file is already configured:
```
VITE_POCKETBASE_URL=http://127.0.0.1:8090
```
Change this URL for production deployment.
