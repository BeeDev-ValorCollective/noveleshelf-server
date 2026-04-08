This is the main app/website backend. 

To start it will not include the contact form but may incorporate it at a later date

## EndPoints:

| Method | Endpoint            | Description   | Auth Required               |
|--------|---------------------|---------------|-----------------------------|
| GET    | /api/health         | check status  | No                          |
| GET    | /admin              | Django admin  | Yes                         |
| POST   | /api/auth/register/ | Create User   | No                          |
| POST   | /api/auth/login/    | Login         | No                          |
| GET    | /api/auth/me/       | User details  | Yes                         |
| POST   | /api/auth/logout/   | Logout        | Yes                         |
| POST   | /api/auth/refresh/  | Refresh Token | Yes - refresh token in body |



## Endpoint Details
Make sure to store accessToken and refreshToken on login

### Register
#### Headers:
```
Content-Type    application/json
```
#### Body:
```
{
    "email": "user@example.com",
    "password": "password123",
    "confirm_password": "password123",
    "date_of_birth": "1990-01-01"
}
```
#### Success response 201:
```
{
    "user": {
        "id": 1,
        "email": "user@example.com",
        "date_of_birth": "1990-01-01",
        "default_login_role": "reader",
        "profile": {
            "username": null,
            "avatar_url": null,
            "bio": null,
            "created_at": "2026-04-08T12:00:00Z"
        },
        "wallet": {
            "quill_balance": 0,
            "gold_ink_balance": 0,
            "black_ink_balance": 0,
            "updated_at": "2026-04-08T12:00:00Z"
        },
        "admin_profile": null
    },
    "tokens": {
        "access": "eyJ...",
        "refresh": "eyJ..."
    }
}
```
#### Error response 400:
```
{
    "email": ["user with this email already exists."],
    "confirm_password": ["Passwords do not match"]
}
```

### Login
#### Headers:
```
Content-Type    application/json
```
#### Body:
```
{
    "email": "user@example.com",
    "password": "password123"
}
```
#### Success response 200:
```
{
    "user": {
        "id": 1,
        "email": "user@example.com",
        "date_of_birth": "1990-01-01",
        "default_login_role": "reader",
        "profile": {...},
        "wallet": {...},
        "admin_profile": null
    },
    "tokens": {
        "access": "eyJ...",
        "refresh": "eyJ..."
    }
}
```
#### Error Responses:
```
400: {"error": "Email and password are required"}
401: {"error": "Invalid credentials"}
```

### Logout
#### Headers:
```
Content-Type      application/json
Authorization     Bearer <access_token>
```
#### Body:
```
{
    "refresh": "eyJ..."
}
```
#### Success response 200:
```
{
    "message": "Successfully logged out"
}
```
#### Error Response 400:
```
{
    "error": "Invalid token"
}
```

### me
#### Headers:
```
Authorization    Bearer <access_token>
```
#### Body:
```
None
```
#### Success response 200:
```
{
    "id": 1,
    "email": "user@example.com",
    "date_of_birth": "1990-01-01",
    "default_login_role": "reader",
    "profile": {
        "username": null,
        "avatar_url": null,
        "bio": null,
        "created_at": "2026-04-08T12:00:00Z"
    },
    "wallet": {
        "quill_balance": 0,
        "gold_ink_balance": 0,
        "black_ink_balance": 0,
        "updated_at": "2026-04-08T12:00:00Z"
    },
    "admin_profile": null
}
```
#### Error response 401:
```
{
    "detail": "Authentication credentials were not provided."
}
```

### refresh
#### Headers:
```
Content-Type    application/json
```
#### Body:
```
{
    "refresh": "eyJ..."
}
```
#### Success response 200:
```
{
    "access": "eyJ..."
}
```
#### Error response 401:
```
{
    "detail": "Token is invalid or expired"
}
```


## Notes
### Routes and uses
| Endpoint | When to call | What it provides |
|----------|--------------|------------------|
| `/api/auth/register/` | User submits registration form | Tokens + full user data including profiles |
| `/api/auth/login/` | User submits login form | Tokens + full user data including profiles |
| `/api/auth/me/` | App opens and token exists in storage | Fresh user data to rebuild app state |
| `/api/auth/refresh/` | Any endpoint returns a `401` | New access token |
| `/api/auth/logout/` | User clicks logout | Confirms refresh token blacklisted |

### Notes for frontend team
- On login/register: store both tokens, use user data to route to correct dashboard
- On app load: check for stored token, if exists call `/me/` to rebuild user state
- On `401` response: automatically call `/refresh/`, update stored access token, retry original request
- On logout: call `/logout/`, delete both tokens from storage, redirect to login
- Never store access token in `localStorage` — use `sessionStorage` (web) or `SecureStore` (Expo)
- Refresh token expires after 7 days — user will need to log in again after that

## Login routing
- Single role user (reader only) → redirect to app.noveleshelf.com
- Multi role user → show gate to choose role
- If user has set a preferred role (default_login_role changed from reader) → skip gate, route directly to that role
- Reader chosen → app.noveleshelf.com
- Author/Admin/Mod chosen → noveleshelf.com