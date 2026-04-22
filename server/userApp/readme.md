# NovelShelf — userApp

Handles all authentication, user profiles, and admin user management.

---

[← Back to Server README](../README.md)

---

## Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| | | | |
| GET | /api/public/authors/ | [Public authors list](#public-authors) | No |
| | | | |
| POST | /api/auth/register/ | [Create User](#register) | No |
| POST | /api/auth/login/ | [Login](#login) | No |
| GET | /api/auth/me/ | [User details](#me) | Yes |
| POST | /api/auth/logout/ | [Logout](#logout) | Yes |
| POST | /api/auth/refresh/ | [Refresh Token](#refresh) | Yes - refresh token in body |
| GET | /api/auth/verify-email/ | [Verify email address](#verify-email) | No |
| POST | /api/auth/resend-verification/ | [Resend verification email](#resend-verification) | Yes |
| POST | /api/auth/forgot-password/ | [Request password reset](#forgot-password) | No |
| POST | /api/auth/reset-password/ | [Reset password with token](#reset-password) | No |
| | | | |
| PATCH | /api/user/profile/update/ | [Update reader profile](#update-profile) | Yes |
| PATCH | /api/user/default-role/update/ | [Update default login role](#update-default-login-role) | Yes |
| PATCH | /api/user/admin-profile/update/ | [Update admin profile](#update-admin-profile) | Yes |
| PATCH | /api/user/author-profile/update/ | [Update author profile](#update-author-profile-author-side) | Yes |
| PATCH | /api/user/moderator-profile/update/ | [Update moderator profile](#update-moderator-profile) | Yes |
| POST | /api/user/change-password/ | [Change password](#change-password) | Yes |
| POST | /api/user/change-email/ | [Change email](#change-email) | Yes |
| POST | /api/user/free-author/upgrade/ | Upgrade to free author | Yes |
| PATCH | /api/user/free-author-profile/update/ | Update free author profile | Yes |
| | | | |
| POST | /api/admin/users/author-upgrade/ | [Upgrade user to author](#upgrade-to-author) | Yes |
| POST | /api/admin/users/admin-upgrade/ | [Upgrade user to admin](#upgrade-to-admin) | Yes |
| POST | /api/admin/users/moderator-upgrade/ | [Upgrade user to moderator](#upgrade-to-moderator) | Yes |
| PATCH | /api/admin/users/author-update/ | [Admin update author](#admin-author-profile-update) | Yes |
| POST | /api/admin/users/deactivate-user/ | [Deactivate user](#deactivate-user) | Yes |
| POST | /api/admin/users/reactivate-user/ | [Reactivate user](#reactivate-user) | Yes |
| GET | /api/admin/users/list/ | [List users](#list-users) | Yes |

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
            "author_username": null,
            "display_name": "Lily Bee",
            "pen_name": "Lily Bee",
            "bio": null,
            "avatar_url": "/media/avatars/author/default.png",
            "tier": 2
        }
    ]
}
```
#### Notes:
- No auth required — public facing endpoint for Vite website
- Only returns authors where `is_publicly_visible` is `True` and account is active
- `display_name` logic:
  - If `show_real_name` is `True` and `first_name` exists → shows real name
  - If `show_real_name` is `False` → shows `pen_name`
  - If no `pen_name` → falls back to `author_username`
- Does not expose email, date of birth, contract link or any sensitive data

---

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
        "moderator_profile": null
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

### Verify email
#### Headers:
```
None
```
#### Query params:
```
token    the verification token from the email link
```
#### Body:
```
None
```
#### Success response 200:
```json
{
    "message": "Email verified successfully. You now have full access to NovelShelf."
}
```
#### Error responses:
```json
400: {"error": "Token is required"}
400: {"error": "Invalid or expired token"}
400: {"error": "Token has expired. Please request a new verification email."}
```
#### Notes:
- No auth required — user clicks link from email
- Token expires after 24 hours
- Once used token cannot be used again
- Frontend should call this endpoint when user lands on /verify-email?token=xyz

---

### Resend verification
#### Headers:
```
Authorization    Bearer <access_token>
```
#### Body
```
None
```
#### Success response 200:
```json
{
    "message": "Verification email sent to user@example.com. Please check your inbox."
}
```
#### Error response 400:
```json
{
    "error": "Your email is already verified"
}
```
#### Notes:
- Auth required — user must be logged in
- Invalidates any existing unused tokens before sending new one
- New token expires after 24 hours
- Use this endpoint for the resend button on the verification reminder page

---

### Forgot password
#### Headers:
```
Content-Type     application/json
```
#### Body:
```json
{
    "email": "user@example.com"
}
```
#### Success response 200:
```json
{
    "message": "If an account exists with that email you will receive a password reset link shortly."
}
```
#### Error responses:
```json
400: {"error": "Email is required"}
400: {"error": "Your email address is not verified. Please verify your email before resetting your password."}
500: {"error": "Failed to send reset email. Please try again."}
```
#### Notes:
- No auth required
- Same response whether email exists or not — prevents email enumeration
- Invalidates any existing unused reset tokens before sending new one
- Token expires after 24 hours
- User must have verified email before requesting reset

---

### Reset password
#### Headers:
```
Content-Type     application/json
```
#### Body:
```json
{
    "token": "eyJ...",
    "new_password": "newpassword123",
    "confirm_password": "newpassword123"
}
```
#### Success response 200:
```json
{
    "message": "Password reset successfully. Please log in with your new password."
}
```
#### Error responses:
```json
400: {"error": "Token, new password and confirm password are required"}
400: {"error": "Passwords do not match"}
400: {"error": "Password must be at least 8 characters"}
400: {"error": "Invalid or expired reset token"}
400: {"error": "Reset token has expired. Please request a new password reset."}
```
#### Notes:
- No auth required
- Token comes from the reset email link
- All existing tokens blacklisted on success
- User must log in again after reset
- Frontend extracts token from URL query param and sends in request body

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
avatar_url       <image file>
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
admin_username    new username
avatar_url        <image file>
```
#### Success response 200:
```json
{
    "message": "Admin profile updated successfully",
    "admin_profile": {
        "admin_username": "QueenAdmin",
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
pen_name           new pen name
bio                bio content
show_real_name     true/false
avatar_url         <image file>
```
#### Success response 200:
```json
{
    "message": "Author profile updated successfully",
    "author_profile": {
        "author_username": null,
        "pen_name": "Lily Bee",
        "first_name": "Melissa",
        "last_name": "Payne",
        "show_real_name": false,
        "is_publicly_visible": true,
        "bio": null,
        "tier": 2,
        "contract_link": "https://drive.google.com/drive/folders/example",
        "avatar_url": "/media/avatars/author/default.png",
        "created_at": "2026-04-10T12:34:12.171145-04:00"
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
- `tier`, `contract_link`, `first_name`, `last_name` and `is_publicly_visible` cannot be updated through this endpoint — admin only
- Uses PATCH not PUT — only send fields you want to change
- Body must be form-data not JSON to support image uploads
- Pre-populate fields from `/me/` on form load, only send changed fields
- `show_real_name` can be toggled by author or admin
- `first_name` and `last_name` are admin only — silently ignored if sent from author side

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
avatar_url      <image file>
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

### Change password
#### Headers:
```
Authorization    Bearer <access_token>
Content-Type     application/json
```
#### Body:
```json
{
    "current_password": "currentpassword",
    "new_password": "newpassword123",
    "confirm_password": "newpassword123"
}
```
#### Success response 200:
```json
{
    "message": "Password changed successfully. Please log in again."
}
```
#### Error responses:
```json
400: {"error": "Current password, new password and confirm password are required"}
400: {"error": "Current password is incorrect"}
400: {"error": "New passwords do not match"}
400: {"error": "New password must be at least 8 characters"}
400: {"error": "New password must be different from current password"}
```
#### Notes:
- All existing tokens are blacklisted on success
- User must log in again after changing password

---

### Change email
#### Headers:
```
Authorization    Bearer <access_token>
Content-Type     application/json
```
#### Body:
```json
{
    "new_email": "newemail@example.com",
    "password": "yourpassword"
}
```
#### Success response 200:
```json
{
    "message": "Email changed successfully. Please verify your new email address at newemail@example.com. You have been logged out."
}
```
#### Error responses:
```json
400: {"error": "New email and password are required"}
400: {"error": "Password is incorrect"}
400: {"error": "New email must be different from current email"}
400: {"error": "Email already in use"}
```
#### Notes:
- Password confirmation required for security
- `is_verified` resets to False on email change
- Verification email sent to new address automatically
- All existing tokens blacklisted on success
- User must log in again and verify new email
- Grace period resets to 7 days from change date

#### Planned security enhancement:
- On email change a notification email will be sent to the old address with an option to cancel/revert the change in case of unauthorized access

---
### Upgrade to free author
#### Headers:
```
Authorization    Bearer <access_token>
```
#### Body:
```
None
```
#### Success response 201:
```json
{
    "message": "You have been upgraded to free author successfully",
    "is_also_paid_author": false,
    "free_author_profile": {
        "author_username": null,
        "pen_name": null,
        "first_name": null,
        "last_name": null,
        "show_real_name": false,
        "is_publicly_visible": false,
        "is_active": true,
        "bio": null,
        "avatar_url": "/media/avatars/free_author/default.png",
        "created_at": "2026-04-21T12:00:00Z"
    }
}
```
#### Error responses:
```json
403: {"error": "Please verify your email before upgrading to a free author"}
400: {"error": "You already have a free author profile"}
```
#### Notes:
- Email must be verified before upgrading
- Any verified reader can upgrade themselves — no admin approval needed
- `default_login_role` is set to `free_author` unless user already has a paid author profile
- `is_also_paid_author` flag in response tells frontend which confirmation message to show
- Frontend should show confirmation dialog before calling this endpoint:
  - Reader: "As a free author your books will always be free to read. Are you sure?"
  - Paid author: "You already have a paid author profile. Adding a free author profile means two separate author identities. Are you sure?"
- Free author books are always free to read — no currency unlock required

---

### Update free author profile
#### Headers:
```
Authorization    Bearer <access_token>
Content-Type     multipart/form-data
```
#### Body (form-data, all fields optional):
```
author_username    new username
avatar_url         <image file>
```
#### Success response 200:
```json
{
    "message": "Free author profile updated successfully",
    "free_author_profile": {
        "author_username": "TestFreeAuthor",
        "pen_name": "Free Pen Name",
        "first_name": null,
        "last_name": null,
        "show_real_name": false,
        "is_publicly_visible": false,
        "is_active": true,
        "bio": "This is my free author bio",
        "avatar_url": "/media/avatars/free_author/default.png",
        "created_at": "2026-04-21T12:00:00Z"
    }
}
```
#### Error responses:
```json
403: {"error": "Free author profile not found"}
400: {"error": "Author username already taken"}
```
#### Notes:
- Only users with a free author profile can access this endpoint
- Unlike paid author profile, free authors can update their own first and last name
- `show_real_name` can be toggled by the free author
- `is_publicly_visible` and `is_active` are admin only — silently ignored if sent
- Uses PATCH not PUT — only send fields you want to change
- Body must be form-data not JSON to support image uploads
- Pre-populate fields from `/me/` on form load, only send changed fields

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
        "is_publicly_visible": false,
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
- `is_publicly_visible` defaults to `false` — admin must explicitly make author public
- Author will need to set their own username and pen name via the author profile update endpoint
- Contract link is set by admin separately via the author management endpoint
- `first_name` and `last_name` are optional at upgrade time — can be set later via admin author update endpoint
- `show_real_name` defaults to false — author or admin can toggle

---

### Admin Author Profile Update
#### Headers:
```
Content-Type      application/json
Authorization     Bearer <access_token>
```
#### Body (all fields optional except user_id):
```json
{
    "user_id": 2,
    "tier": 2,
    "contract_link": "https://drive.google.com/drive/folders/example",
    "first_name": "Melissa",
    "last_name": "Payne",
    "show_real_name": false,
    "is_publicly_visible": true
}
```
#### Success response 200:
```json
{
    "message": "user@example.com author profile updated successfully",
    "author_profile": {
        "author_username": null,
        "pen_name": "Lily Bee",
        "first_name": "Melissa",
        "last_name": "Payne",
        "show_real_name": false,
        "is_publicly_visible": true,
        "bio": null,
        "tier": 2,
        "contract_link": "https://drive.google.com/drive/folders/example",
        "avatar_url": "/media/avatars/author/default.png",
        "created_at": "2026-04-10T12:34:12.171145-04:00"
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
- `first_name` and `last_name` are admin only
- `is_publicly_visible` controls whether author appears on public authors page
- Author updates their own username, pen name, bio, show_real_name and avatar via the author profile update endpoint

---

### Upgrade to Admin
#### Headers:
```
Content-Type      application/json
Authorization     Bearer <access_token>
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
- Upgraded admin gets `is_staff` set to `True` automatically
- `admin_username` defaults to the user's email — can be updated via admin profile update endpoint
- `is_super_admin` is always `False` for upgraded admins — superadmin is set internally only

---

### Upgrade to Moderator
#### Headers:
```
Content-Type      application/json
Authorization     Bearer <access_token>
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
- `assigned_by` is automatically set to the admin performing the upgrade
- `mod_username` defaults to null — moderator sets it via moderator profile update endpoint

---

### Deactivate User
#### Headers:
```
Content-Type      application/json
Authorization     Bearer <access_token>
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

### Reactivate User
#### Headers:
```
Content-Type      application/json
Authorization     Bearer <access_token>
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

### List users
#### Headers:
```
Authorization    Bearer <access_token>
```
#### Body:
```
None
```
#### Query params (all optional):
```
?role=         filter by role: reader, author, admin, moderator
?is_active=    filter by active status: true, false
?page=         page number, defaults to 1
```
#### Success response 200:
```json
{
    "count": 10,
    "page": 1,
    "page_size": 20,
    "total_pages": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "email": "user@example.com",
            "date_of_birth": "1990-01-01",
            "default_login_role": "reader",
            "profile": {...},
            "wallet": {...},
            "admin_profile": null,
            "author_profile": null,
            "moderator_profile": null
        }
    ]
}
```
#### Error response 403:
```json
{
    "error": "You do not have permission to perform this action"
}
```
#### Notes:
- Admin access required
- Returns all users by default — use query params to filter
- `role=reader` returns users with no author, admin or moderator profile
- `is_active=false` returns deactivated users
- Results are paginated at 20 per page
- Use `page` param to navigate through results

---

[← Back to Server README](../readme.md)
