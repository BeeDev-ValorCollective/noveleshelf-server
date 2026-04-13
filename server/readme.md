# NovelShelf Backend API

This is the main app/website backend.

To start it will not include the contact form but may incorporate it at a later date.

---

## Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | /admin | Django admin | Yes |
| | | | |
| GET | /api/public/authors/ | [Public authors list](#public-authors) | No |
| | | | |
| POST | /api/auth/register/ | [Create User](#register) | No |
| POST | /api/auth/login/ | [Login](#login) | No |
| GET | /api/auth/me/ | [User details](#me) | Yes |
| POST | /api/auth/logout/ | [Logout](#logout) | Yes |
| POST | /api/auth/refresh/ | [Refresh Token](#refresh) | Yes - refresh token in body |
| | | | |
| PATCH | /api/user/profile/update/ | [Update reader profile](#update-profile) | Yes |
| PATCH | /api/user/default-role/update/ | [Update default login role](#update-default-login-role) | Yes |
| PATCH | /api/user/admin-profile/update/ | [Update admin profile](#update-admin-profile) | Yes |
| PATCH | /api/user/author-profile/update/ | [Update author profile](#update-author-profile-author-side) | Yes |
| PATCH | /api/user/moderator-profile/update/ | [Update moderator profile](#update-moderator-profile) | Yes |
| | | | |
| POST | /api/admin/author-upgrade/ | [Upgrade user to author](#upgrade-to-author) | Yes |
| POST | /api/admin/admin-upgrade/ | [Upgrade user to admin](#upgrade-to-admin) | Yes |
| POST | /api/admin/moderator-upgrade/ | [Upgrade user to moderator](#upgrade-to-moderator) | Yes |
| PATCH | /api/admin/author-update/ | [Admin update author tier and contract](#admin-author-profile-update) | Yes |
| POST | /api/admin/deactivate-user/ | [Deactivate user](#deactivate-user) | Yes |
| POST | /api/admin/reactivate-user/ | [Reactivate user](#reactivate-user) | Yes |

---

## Notes

### Frontend Notes
- On login/register: store both tokens, use user data to route to correct dashboard
- On app load: check for stored token, if exists call `/me/` to rebuild user state
- On `401` response: automatically call `/refresh/`, update stored access token, retry original request
- On logout: call `/logout/`, delete both tokens from storage, redirect to login
- Never store access token in `localStorage` — use `sessionStorage` (web) or `SecureStore` (Expo)
- Refresh token expires after 7 days — user will need to log in again after that
- Always display role context alongside usernames in UI e.g. "QueenBee (Author)" not just "QueenBee" to avoid confusion across profile types

### Login Routing
- Single role user (reader only) → redirect to app.noveleshelf.com
- Multi role user → show gate to choose role
- If user has set a preferred role (default_login_role changed from reader) → skip gate, route directly to that role
- Reader chosen → app.noveleshelf.com
- Author/Admin/Mod chosen → noveleshelf.com

---

## Endpoint Details

### Public authors
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
    "count": 1,
    "authors": [
        {
            "author_username": "TestAuthor",
            "display_name": "Test Pen Name",
            "pen_name": "Test Pen Name",
            "bio": "This is my author bio",
            "avatar_url": "/media/avatars/author/default.png",
            "tier": 1
        }
    ]
}
```
#### Notes:
- No auth required — public facing endpoint for Vite website
- Only returns authors where is_publicly_visible is True and account is active
- display_name shows real name if show_real_name is True and first_name exists
- Falls back to pen_name then author_username if real name not available
- Does not expose email, date of birth, contract link or any sensitive data

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
        "author_profile": null,
        "moderator_profile": null
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

---

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
        "author_profile": null,
        "moderator_profile": null,
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

---

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

---

### Me
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
    "author_profile": null,
    "moderator_profile": null
}
```
#### Error response 401:
```json
{
    "detail": "Authentication credentials were not provided."
}
```

---

### Refresh
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

---

### Update Profile
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
- Form loads with values from `/me/`; on submit only include changed fields in the request body

---

### Update Admin Profile
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

---

### Update Author Profile (author side)
#### Headers:
```
Authorization    Bearer <access_token>
Content-Type     multipart/form-data
```
#### Body (form-data, all fields optional):
```
author_username    new username
bio                bio content
```
#### Success response 200:
```json
{
    "message": "Author profile updated successfully",
    "author_profile": {
        "author_username": null,
        "pen_name": null,
        "first_name": "Test",
        "last_name": "Author",
        "show_real_name": false,
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
403: {"error": "Author profile not found"}
400: {"error": "Author username already taken"}
```
#### Notes:
- Only users with an author profile can access this endpoint
- `tier` and `contract_link` cannot be updated through this endpoint — admin only
- Uses PATCH not PUT — only send fields you want to change
- Body must be form-data not JSON to support image uploads
- Pre-populate fields from `/me/` on form load, only send changed fields
- show_real_name can be toggled by author or admin
- first_name and last_name are admin only — silently ignored if sent from author side

---

### Update Moderator Profile
#### Headers:
```
Authorization    Bearer <access_token>
Content-Type     multipart/form-data
```
#### Body (form-data, all fields optional):
```
mod_username    new username
```
#### Success response 200:
```json
{
    "message": "Moderator profile updated successfully",
    "moderator_profile": {
        "mod_username": "TestModerator",
        "avatar_url": "/media/avatars/moderator/default.png",
        "assigned_by": 1,
        "created_at": "2026-04-09T12:00:00Z"
    }
}
```
#### Error responses:
```json
403: {"error": "Moderator profile not found"}
400: {"error": "Moderator username already taken"}
```
#### Notes:
- Only users with a moderator profile can access this endpoint
- Uses PATCH not PUT — only send fields you want to change
- Body must be form-data not JSON to support image uploads
- Pre-populate fields from `/me/` on form load, only send changed fields

---

### Update Default Login Role
#### Headers:
```
Authorization    Bearer <access_token>
Content-Type     application/json
```
#### Body:
```json
{
    "default_login_role": "author"
}
```
#### Success response 200:
```json
{
    "message": "Default login role updated to author",
    "default_login_role": "author"
}
```
#### Error responses:
```json
400: {"error": "default_login_role is required"}
400: {"error": "Invalid role. Must be one of: reader, author, moderator, admin"}
403: {"error": "You do not have an author profile"}
403: {"error": "You do not have a moderator profile"}
403: {"error": "You do not have an admin profile"}
```
#### Notes:
- User can only set a role they actually have a profile for
- Setting to reader is always allowed since every user is a reader
- Once set the login gate will be skipped and user will be routed directly to this role on login
- User can always change back to reader or any other role they have

---

### Upgrade to Author
#### Headers:
```
Content-Type      application/json
Authorization     Bearer <access_token>
```
#### Body:
```json
{
    "user_id": 3,
    "first_name": "Test",
    "last_name": "Author",
    "show_real_name": false
}
```
#### Success response 201:
```json
{
    "message": "user@example.com has been upgraded to author successfully",
    "author_profile": {
        "author_username": null,
        "pen_name": null,
        "first_name": "Test",
        "last_name": "Author",
        "show_real_name": false,
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
- first_name and last_name are optional at upgrade time — can be set later via admin author update endpoint
- show_real_name defaults to false — author or admin can toggle

---

### Admin Author Profile Update
#### Headers:
```
Content-Type    application/json
Authorization    Bearer <access_token>
```
#### Body (all fields optional except user_id):
```json
{
    "user_id": 2,
    "tier": 2,
    "contract_link": "https://drive.google.com/drive/folders/example",
    "first_name": "Test",
    "last_name": "Author",
    "show_real_name": true
}
```
#### Success response 200:
```json
{
    "message": "user@example.com author profile updated successfully",
    "author_profile": {
        "author_username": null,
        "pen_name": null,
        "first_name": "Test",
        "last_name": "Author",
        "show_real_name": false,
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
400: {"error": "Tier must be between 1 and 5"}
400: {"error": "Tier must be a number"}
404: {"error": "User not found"}
404: {"error": "User does not have an author profile"}
```
#### Notes:
- Admin access required
- Tier must be between 1 and 5
- Contract link should be a Google Drive folder URL
- Author updates their own username, pen name, bio and avatar via the author profile update endpoint

---

### Upgrade to Admin
#### Headers:
```
Content-Type    application/json
Authorization    Bearer <access_token>
```
#### Body:
```json
{
    "user_id": 2
}
```
#### Success response 201:
```json
{
    "message": "user@example.com has been upgraded to admin successfully",
    "admin_profile": {
        "admin_username": "user@example.com",
        "is_super_admin": false,
        "avatar_url": "/media/avatars/admin/default.png",
        "created_at": "2026-04-09T12:00:00Z"
    }
}
```
#### Error responses:
```json
403: {"error": "You do not have permission to perform this action"}
400: {"error": "user_id is required"}
400: {"error": "User is already an admin"}
404: {"error": "User not found"}
```
#### Notes:
- Any is_staff user can upgrade others to admin
- Upgraded admin gets is_staff set to True automatically
- admin_username defaults to the user's email — can be updated via admin profile update endpoint
- is_super_admin is always False for upgraded admins — superadmin is set internally only

---

### Upgrade to Moderator
#### Headers:
```
Content-Type    application/json
Authorization    Bearer <access_token>
```
#### Body:
```json
{
    "user_id": 5
}
```
#### Success response 201:
```json
{
    "message": "user@example.com has been upgraded to moderator successfully",
    "moderator_profile": {
        "mod_username": null,
        "avatar_url": "/media/avatars/moderator/default.png",
        "assigned_by": 1,
        "created_at": "2026-04-09T12:00:00Z"
    }
}
```
#### Error responses:
```json
403: {"error": "You do not have permission to perform this action"}
400: {"error": "user_id is required"}
400: {"error": "User is already a moderator"}
404: {"error": "User not found"}
```
#### Notes:
- Any is_staff user can upgrade others to moderator
- assigned_by is automatically set to the admin performing the upgrade
- mod_username defaults to null — moderator sets it via moderator profile update endpoint

---

### Deactivate user
#### Headers:
```
Content-Type    application/json
Authorization    Bearer <access_token>
```
#### Body:
```json
{
    "user_id": 2
}
```
#### Success response 200:
```json
{
    "message": "user@example.com has been deactivated successfully"
}
```
#### Error responses:
```json
403: {"error": "You do not have permission to perform this action"}
400: {"error": "user_id is required"}
400: {"error": "You cannot deactivate your own account"}
404: {"error": "User not found"}
```
#### Notes:
- Any is_staff user can deactivate users
- Deactivated users cannot log in and existing tokens stop working
- All user data is preserved — use reactivate to restore access
- Cannot deactivate your own account

---

### Reactivate user
#### Headers:
```
Content-Type    application/json
Authorization    Bearer <access_token>
```
#### Body:
```json
{
    "user_id": 2
}
```
#### Success response 200:
```json
{
    "message": "user@example.com has been reactivated successfully"
}
```
#### Error responses:
```json
403: {"error": "You do not have permission to perform this action"}
400: {"error": "user_id is required"}
404: {"error": "User not found"}
```
#### Notes:
- Any is_staff user can reactivate users
- Restores full account access immediately
- Future enhancement: will trigger a mandatory password reset email on reactivation

---

## Debug Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | /api/debug/health/ | [Health check](#health-check) | No |
| POST | /api/debug/login/ | [Login with full debug info](#debug-login) | No |
| GET | /api/debug/me/ | [Token owner + debug info](#debug-me) | Yes |

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
        "moderator_profile": null
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
        "moderator_profile": null
    },
    "debug": {
        "is_staff": true,
        "is_superuser": true,
        "has_admin_profile": true,
        "has_author_profile": false,
        "has_moderator_profile": false,
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
