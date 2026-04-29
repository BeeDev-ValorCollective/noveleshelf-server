# NovelShelf Django API

This is the main backend API for the NovelShelf platform.

---

## App Structure
```
server/
├── booksApp/        — Books, chapters, genres endpoints → [Documentation](booksApp/readme.md)
├── cronApp/         — Cron job logging → [Documentation](cronApp/readme.md)
├── currencyApp/     — Wallet, currency, transactions endpoints (pending) 
├── cron/            — Cron job functions
├── utils/           — Shared utility functions (email, tokens)
├── server/          — Core settings, URLs, debug endpoints
├── userApp/         — Auth, user profiles, admin endpoints → [Documentation](userApp/readme.md)
├── logs/            — Cron job log files
├── manage.py
├── requirements.txt
└── README.md
```

---

## App Documentation

| App | Description | Documentation | Developer Notes |
|-----|-------------|---------------|-----------------|
| userApp | Auth, user profiles, admin user management | [userApp README](userApp/readme.md) | [Developer Notes](userApp/dev_notes.md) |
| booksApp | Books, chapters, genres | [booksApp README](booksApp/readme.md) | [Developer Notes](booksApp/dev_notes.md) |
| cronApp | Cron job logging | [cronApp README](cronApp/readme.md) | — |
| currencyApp | Wallet, currency, transactions | Coming soon | — |

---

## API Root Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | / | API status | No |
| GET | /admin | Django admin | Yes |
| GET | /api/debug/health/ | Health check | No |
| GET | /api/debug/test-email/ | Test email sending | No |
| POST | /api/debug/login/ | Debug login | No |
| GET | /api/debug/me/ | Debug me | Yes |

---

## Debug Endpoint Details

### Health Check
#### Headers:
```
None
```
#### Body:
```
None
```
#### Success response 200:
```json
{
    "status": "ok",
    "message": "Django is talking!"
}
```
#### Notes:
- No auth required
- Used to confirm server is running and reachable

---

### Test Email
#### Headers:
```
None
```
#### Body:
```
None
```
#### Success response 200:
```json
{
    "message": "Test email sent successfully"
}
```
#### Notes:
- No auth required
- Used to confirm email is working
- Remove on production after tested

---

### Debug Login
#### Headers:
```
Content-Type    application/json
```
#### Body:
```json
{
    "email": "user@example.com",
    "password": "yourpassword"
}
```
#### Success response 200:
```json
{
    "user": {
        "id": 1,
        "email": "user@example.com",
        "date_of_birth": "1990-01-01",
        "default_login_role": "reader",
        "profile": {...},
        "wallet": {...},
        "admin_profile": {...},
        "author_profile": null,
        "moderator_profile": null,
        "free_author_profile": null,
        "is_verified": true
    },
    "tokens": {
        "access": "eyJ...",
        "refresh": "eyJ..."
    },
    "debug": {
        "is_staff": true,
        "is_superuser": true,
        "has_admin_profile": true,
        "has_author_profile": false,
        "has_moderator_profile": false,
        "has_free_author_profile": false,
        "default_login_role": "reader"
    }
}
```
#### Error responses:
```json
400: {"error": "Email and password are required"}
401: {"error": "Invalid credentials"}
```
#### Notes:
- Returns fresh tokens every time regardless of existing tokens
- Existing tokens remain valid until they naturally expire
- Dev only — remove before production

---

### Debug Me
#### Headers:
```
Authorization    Bearer <access_token>
```
#### Body:
```
None
```
#### Success response 200:
```json
{
    "user": {
        "id": 1,
        "email": "user@example.com",
        "date_of_birth": "1990-01-01",
        "default_login_role": "reader",
        "profile": {...},
        "wallet": {...},
        "admin_profile": {...},
        "author_profile": null,
        "moderator_profile": null,
        "free_author_profile": null,
        "is_verified": true
    },
    "debug": {
        "is_staff": true,
        "is_superuser": true,
        "has_admin_profile": true,
        "has_author_profile": false,
        "has_moderator_profile": false,
        "has_free_author_profile": false,
        "default_login_role": "reader"
    }
}
```
#### Error response 401:
```json
{
    "detail": "Authentication credentials were not provided."
}
```
#### Notes:
- Use this to verify which user a token belongs to
- No tokens returned — use debug/login/ if you need fresh tokens
- Dev only — remove before production

---

## Frontend Notes
- On login/register: store both tokens, use user data to route to correct dashboard
- On app load: check for stored token, if exists call `/me/` to rebuild user state
- On `401` response: automatically call `/refresh/`, update stored access token, retry original request
- On logout: call `/logout/`, delete both tokens from storage, redirect to login
- Never store access token in `localStorage` — use `sessionStorage` (web) or `SecureStore` (Expo)
- Refresh token expires after 7 days — user will need to log in again after that
- Always display role context alongside usernames in UI e.g. "QueenBee (Author)" not just "QueenBee" to avoid confusion across profile types

---

## Login Routing
- Single role user (reader only) → redirect to app.noveleshelf.com
- Multi role user → show gate to choose role
- If user has set a preferred role (default_login_role changed from reader) → skip gate, route directly to that role
- Reader chosen → app.noveleshelf.com
- Author/Admin/Mod chosen → noveleshelf.com

---

[← Back to Repository README](../README.md)