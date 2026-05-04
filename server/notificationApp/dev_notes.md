# notificationApp — Developer Notes

---

## Overview

The notificationApp handles all platform notifications. There are two types of notifications:

**Direct user emails** — go directly to a specific user, always send regardless of preferences:
- Verification email
- Password reset
- Author approved
- Author deactivated
- Author reactivated

**Admin/system notifications** — go to admins/moderators based on their preferences, plus any system notification emails:
- New user registered
- Free author upgrade
- New author request
- Book submitted for approval
- Flagged content
- Author request status change
- Book status change
- Author deactivated (admin copy)
- Author reactivated (admin copy)

---

## How to add a new notification type

**Step 1 — Add to `NotificationType` table:**
```sql
INSERT INTO notificationApp_notificationtype 
    (code, label, description, recipient_type, sends_to_user, sends_to_admins, is_active, created_at)
VALUES
    ('your_code', 'Your Label', 'Description of what triggers this', 'admin', 0, 1, 1, NOW());
```

**Step 2 — Add email content to `_build_email_content` in `utils/email_utils.py`:**
```python
'your_code': (
    'Novel eShelf — Email Subject',
    'Email message body here'
),
```

**Step 3 — Add bell message to `_build_bell_message` in `utils/email_utils.py`:**
```python
'your_code': f'Short bell notification message',
```

**Step 4 — Call `send_notification` in the relevant view:**
```python
from utils.email_utils import send_notification

try:
    send_notification(
        'your_code',
        user=affected_user,
        triggered_by=request.user,  # optional
        context={'key': 'value'}    # optional extra data
    )
except Exception as e:
    print(f'Notification failed: {e}')
```

---

## How `send_notification` works

Located in `utils/email_utils.py`. Flow:

1. Looks up `NotificationType` by code
2. If `sends_to_user = True` and user provided:
   - Adds user email to recipients
   - Creates `Notification` bell record for user
3. If `sends_to_admins = True`:
   - Finds all users with `admin_profile` or `moderator_profile`
   - Checks each one's `NotificationPreference` — defaults to enabled if no preference set
   - Adds enabled ones to recipients
   - Creates `Notification` bell record for each
   - Finds all active `SystemNotificationEmail` records linked to this type
   - Adds their emails to recipients
4. Sends one email to all recipients

---

## How `send_notification` is called

```python
send_notification(
    notification_code,   # required — the NotificationType code
    user=None,           # the affected user
    triggered_by=None,   # who caused the action (admin etc.)
    context=None         # dict of extra data for email content
)
```

**Context keys used by existing templates:**
- `request_type` — used by `new_author_request`
- `status` — used by `author_request_status_change` and `book_status_change`
- `reader_notes` — used by `author_request_status_change` and `book_status_change`
- `book_title` — used by `book_submitted_for_approval` and `book_status_change`
- `content_type` — used by `flagged_content`

---

## Notification Preferences

**Default behavior:**
- If a user has no `NotificationPreference` record for a type → defaults to enabled
- Preferences are only created when a user explicitly toggles a notification

**Permission hierarchy:**
- Super admin → can edit everyone's preferences and permissions
- Admin → can edit preferences of users they upgraded
- Moderator/upgraded admin → can only toggle what their granting admin allowed

---

## System Notification Emails

Managed in Django admin by super admin only. These are email addresses not tied to any user account that always receive certain notification types regardless of user preferences.

Example use case: `admin@noveleshelf.com` receives all admin notification types.

Add via Django admin → System Notification Emails → Add.

---

## Bell Notifications

`Notification` records are created automatically by `send_notification`. They power the frontend bell icon.

- Read only in Django admin — cannot be manually created
- Users can mark as read or clear via API endpoints
- Frontend polls `/api/notifications/my-notifications/` for unread count

---

## Files involved

| File | Purpose |
|------|---------|
| `notificationApp/models.py` | All notification models |
| `notificationApp/views.py` | All notification endpoints |
| `notificationApp/urls.py` | URL routing |
| `utils/email_utils.py` | Email content and `send_notification` function |
| `notificationApp_seed.sql` | Initial notification type data |

---

## TODO items
- Add notification bell to Vite frontend
- Add notification bell to Expo frontend
- Add notification preferences page to user profile
- Add admin notification management page
- Consider adding email templates for richer HTML emails
- Add `book_submitted_for_approval` and `book_status_change` calls when booksApp views are built
- Add `flagged_content` call when moderation views are built