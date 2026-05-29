# Novel eShelf — notificationApp

Handles all platform notifications including email preferences, bell notifications and system notification emails.

---

[← Back to Server README](../README.md)

---

## Endpoints

### User endpoints (`/api/notifications/`)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | /api/notifications/my-notifications/ | Get my notifications | Yes |
| POST | /api/notifications/mark-read/ | Mark notification as read | Yes |
| POST | /api/notifications/mark-all-read/ | Mark all notifications as read | Yes |
| DELETE | /api/notifications/clear/ | Clear all notifications | Yes |
| GET | /api/notifications/my-preferences/ | Get my notification preferences | Yes |
| PATCH | /api/notifications/my-preferences/update/ | Update my notification preference | Yes |

### Admin endpoints (`/api/notifications/admin/`)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | /api/notifications/admin/types/ | List all notification types | Yes |
| GET | /api/notifications/admin/user-preferences/ | Get a user's preferences | Yes |
| PATCH | /api/notifications/admin/user-preferences/update/ | Update a user's preference | Yes |
| PATCH | /api/notifications/admin/user-permissions/update/ | Update a user's permission | Yes |
| GET | /api/notifications/admin/system-emails/ | List system notification emails | Yes |
| POST | /api/notifications/admin/system-emails/create/ | Create system notification email | Yes |
| PATCH | /api/notifications/admin/system-emails/update/ | Update system notification email | Yes |

---

## Endpoint Details

*Endpoint details will be added as views are tested and confirmed.*

---

## Notification Types

Seeded via `notificationApp_seed.sql` — do not add manually through Django admin unless necessary.

| Code | Label | Recipient | Description |
|------|-------|-----------|-------------|
| `new_user_registered` | New User Registered | Admin | Triggered when a new user registers |
| `free_author_upgrade` | Free Author Upgrade | Admin | Triggered when a reader upgrades to free author |
| `new_author_request` | New Author Request | Admin | Triggered when a user submits a paid author request |
| `author_request_approved` | Author Request Approved | Both | Triggered when an author request is approved |
| `author_request_status_change` | Author Request Status Change | User | Triggered when an author request status is updated |
| `book_submitted_for_approval` | Book Submitted for Approval | Admin | Triggered when a paid author submits a book for approval |
| `book_status_change` | Book Status Change | User | Triggered when a book status changes |
| `flagged_content` | Flagged Content | Admin | Triggered when a review or comment is flagged |
| `author_deactivated` | Author Deactivated | Both | Triggered when an author profile is deactivated |
| `author_reactivated` | Author Reactivated | Both | Triggered when an author profile is reactivated |

---

## Notes for developers

See [DEVELOPER_NOTES.md](dev_notes.md) for full details on:
- How to add new notification types
- How `send_notification` works
- Email content templates
- Bell notification records

---

[← Back to Server README](../README.md)