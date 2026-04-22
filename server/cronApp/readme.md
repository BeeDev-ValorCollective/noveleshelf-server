# Novel eShelf — cronApp

Handles logging for all scheduled cron jobs across the platform.

---

[← Back to Server README](../README.md)

---

## Overview

`cronApp` provides the `CronLog` model which records every cron job run — both scheduled and manual. All cron job functions live in the `cron/` folder at the server root, not in this app.

---

## Models

### CronLog
Records every cron job execution.

| Field | Type | Description |
|-------|------|-------------|
| `job_name` | string | Name of the cron function that ran |
| `status` | choice | success, failure, warning |
| `message` | text | Output message from the job |
| `records_affected` | integer | Number of records changed |
| `created_at` | datetime | When the job ran |

---

## Viewing logs

Logs are visible in two places:
- **Django admin** → CronApp → Cron logs — read only, no add or delete
- **`logs/cron.log`** — file log on the server, same information in text format

---

## Current cron jobs

| Schedule | Function | Description |
|----------|----------|-------------|
| Daily midnight | `cron.user_cron.deactivate_unverified_users` | Deactivates unverified users past 7 day grace period |
| Sundays 3am | `cron.user_cron.flush_expired_tokens` | Cleans up expired JWT tokens |
| Daily 1am | `cron.books_cron.mark_books_not_new` | Marks books older than 30 days as not new |
| Daily 1am | `cron.books_cron.mark_chapters_not_new` | Marks chapters older than 7 days as not new |

---

## Adding new cron jobs

1. Add function to relevant file in `cron/` folder — `user_cron.py`, `books_cron.py` etc.
2. Add `CronLog.objects.create(...)` call inside the function for both success and failure
3. Add to `CRONJOBS` in `settings.py`
4. Run `python manage.py crontab add` on server
5. Update the cron jobs table above

---

[← Back to Server README](../README.md)