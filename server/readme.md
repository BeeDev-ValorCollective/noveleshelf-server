This is the main app/website backend. 

To start it will not include the contact form but may incorporate it at a later date

## EndPoints:

| Method | Endpoint                        | Description                | Auth Required               |
|--------|---------------------------------|----------------------------|-----------------------------|
| GET    | /admin                          | Django admin               | Yes                         |
| POST   | /api/auth/register/             | Create User                | No                          |
| POST   | /api/auth/login/                | Login                      | No                          |
| GET    | /api/auth/me/                   | User details               | Yes                         |
| POST   | /api/auth/logout/               | Logout                     | Yes                         |
| POST   | /api/auth/refresh/              | Refresh Token              | Yes - refresh token in body |
| PATCH  | /api/auth/profile/update/       | Update reader profile      | Yes                         |
| PATCH  | /api/auth/admin-profile/update/ | Update admin profile       | Yes                         |
| POST   | /api/auth/admin/author-upgrade/ | Update user to author      | Yes                         |

## Notes:
### Frontend Notes
- On login/register: store both tokens, use user data to route to correct dashboard
- On app load: check for stored token, if exists call `/me/` to rebuild user state
- On `401` response: automatically call `/refresh/`, update stored access token, retry original request
- On logout: call `/logout/`, delete both tokens from storage, redirect to login
- Never store access token in `localStorage` — use `sessionStorage` (web) or `SecureStore` (Expo)
- Refresh token expires after 7 days — user will need to log in again after that

### Login routing
- Single role user (reader only) → redirect to app.noveleshelf.com
- Multi role user → show gate to choose role
- If user has set a preferred role (default_login_role changed from reader) → skip gate, route directly to that role
- Reader chosen → app.noveleshelf.com
- Author/Admin/Mod chosen → noveleshelf.com



## Endpoint Details

### Register
#### Headers:
```
Content-Type    application/json
```
#### Body:
```json
{
    "email": "user@example.com",
    "password": "password123",
    "confirm_password": "password123",
    "date_of_birth": "1990-01-01"
}
```
#### Success response 201:
```json
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
        "admin_profile": null,
        "author_profile": null
    },
    "tokens": {
        "access": "eyJ...",
        "refresh": "eyJ..."
    }
}
```
#### Error response 400:
```json
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
```json
{
    "email": "user@example.com",
    "password": "password123"
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
        "admin_profile": null,
        "author_profile": null
    },
    "tokens": {
        "access": "eyJ...",
        "refresh": "eyJ..."
    }
}
```
#### Error Responses:
```json
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
```json
{
    "refresh": "eyJ..."
}
```
#### Success response 200:
```json
{
    "message": "Successfully logged out"
}
```
#### Error Response 400:
```json
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
```json
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
    "admin_profile": null,
    "author_profile": null
}
```
#### Error response 401:
```json
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
```json
{
    "refresh": "eyJ..."
}
```
#### Success response 200:
```json
{
    "access": "eyJ..."
}
```
#### Error response 401:
```json
{
    "detail": "Token is invalid or expired"
}
```

### update profile
#### Headers:
```
Authorization    Bearer <access_token>
Content-Type     multipart/form-data
```
#### Body (form-data, all fields optional):
```
username         new username
bio              bio content
```
#### Success response 200:
```json
{
    "message": "Profile updated successfully",
    "profile": {
        "username": "QueenBee",
        "avatar_url": "/media/avatars/reader/default.png",
        "bio": "I am the Owner",
        "created_at": "2026-04-08T16:29:47.299265-04:00"
    }
}
```
#### Error response 400:
```json
{
    "error": "Username already taken"
}
```
#### Notes:
- Uses PATCH not PUT — only send fields you want to change
- Body must be form-data not JSON to support image uploads
- Users can clear their bio by sending an empty string
- form loads with values from /me/ url on submit only include changed fields in the request body

### update admin profile
#### Headers:
```
Authorization    Bearer <access_token>
Content-Type     multipart/form-data
```
#### Body (form-data, all fields optional):
```
admin_username         new username
```
#### Success response 200:
```json
{
    "message": "Admin profile updated successfully",
    "admin_profile": {
        "admin_username": "QueenBee",
        "is_super_admin": true,
        "avatar_url": "/media/avatars/admin/default.png",
        "created_at": "2026-04-09T12:00:00Z"
    }
}
```
#### Error responses:
```json
403: {"error": "Admin profile not found"}
400: {"error": "Admin username already taken"}
```
#### Notes:
- Only users with an admin profile can access this endpoint
- `is_super_admin` cannot be updated through this endpoint
- Uses PATCH not PUT — only send fields you want to change
- Body must be form-data not JSON to support image uploads
- Pre-populate fields from `/me/` on form load, only send changed fields

### Upgrade to Author
#### Headers:
```
Content-Type      application/json
Authorization     Bearer <access_token>
```
#### Body:
```json
{
    "user_id": 3
}
```
#### Success response 201:
```json
{
    "message": "user@example.com has been upgraded to author successfully",
    "author_profile": {
        "author_username": null,
        "pen_name": null,
        "bio": null,
        "tier": 1,
        "contract_link": null,
        "avatar_url": "/media/avatars/author/default.png",
        "created_at": "2026-04-09T12:00:00Z"
    }
}
```
#### Error responses:
```json
403: {"error": "You do not have permission to perform this action"}
400: {"error": "user_id is required"}
400: {"error": "User is already an author"}
404: {"error": "User not found"}
```
#### Notes:
- Admin access required
- Author profile is created with tier 1 by default
- Author will need to set their own username and pen name via the author profile update endpoint
- Contract link is set by admin separately via the author management endpoint


## Debug EndPoints:

| Method | Endpoint                        | Description                | Auth Required               |
|--------|---------------------------------|----------------------------|-----------------------------|
| GET    | /api/debug/health/              | check status               | No                          |
| POST   | /api/debug/login/               | Login with full debug info | No                          |
| GET    | /api/debug/me/                  | token owner + debug info   | Yes                         |


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
        "author_profile": null
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
- Add has_moderator_profile to debug block when moderator profile is built

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
        "author_profile": null
    },
    "debug": {
        "is_staff": true,
        "is_superuser": true,
        "has_admin_profile": true,
        "has_author_profile": false,
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
- Add has_moderator_profile to debug block when moderator profile is built


