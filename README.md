# NovelShelf Server

This repository contains the backend services for the NovelShelf platform.

---

## Repository Structure
noveleshelf-server/
├── mailServer/          — Contact form email service
├── server/              — Django REST API backend
└── README.md
---

## Services

### Django API — [Documentation](server/readme.md)
The main backend API for the NovelShelf platform. Handles authentication, user management, books, chapters, and currency.

- Built with Django 5.x and Django REST Framework
- MySQL database
- JWT authentication

#### Shell access:
- ssh -p 1394 noveleshelf@noveleshelf.com
- password=(db password on env)
- turn on environment:
    - source /home/noveleshelf/virtualenv/public_html/api/3.10/bin/activate && cd /home/noveleshelf/public_html/api

### Mail Server — [Documentation](mailServer/readme.md)
Contact form email service. May be replaced by the main Django backend at a later date.

---

## Getting Started

### Django API
```bash
cd server
python -m venv venv
source venv/bin/activate  # Mac/Linux (windows = venv/Scripts/activate)
pip install -r requirements.txt
touch .env      # fill in your values
python manage.py migrate
python manage.py runserver
```
/home/noveleshelf/public_html/api/manage.py migrate --fake
---

## Environment Variables
See Google drive for current required variables and create the env file inside `server/server/.env`.

---

## Tech Stack
- **Backend**: Django 5.x, Django REST Framework
- **Database**: MySQL / MariaDB
- **Auth**: JWT via djangorestframework-simplejwt
- **Storage**: Local (S3 planned)
- **Email**: Google Workspace SMTP (planned)

---

## Deployment

### Repository structure note
The git repository (`repositories/noveleshelf-server/`) contains both the Django API and mailServer. The Django app runs from `public_html/api/`. After a git pull the relevant files need to be copied from the repository to the site folder.

### New code changes (no database changes)
1. `git pull` in `repositories/noveleshelf-server/`
2. Copy relevant files from `repositories/noveleshelf-server/server/` to `public_html/api/`
3. Restart app in cPanel Python app panel

### New tables
1. Export structure only from MySQL Workbench — select only new tables
2. Find and replace `utf8mb4_0900_ai_ci` with `utf8mb4_unicode_ci` in exported file
3. In phpMyAdmin import tab — uncheck **Enable foreign key checks**
4. Import file
5. SSH into server and run:
```bash
source /home/noveleshelf/virtualenv/public_html/api/3.10/bin/activate && cd /home/noveleshelf/public_html/api
python manage.py migrate --fake
python manage.py migrate
```
6. Copy relevant files from repository to site folder
7. Restart app in cPanel Python app panel

### Changes to existing tables
1. Write ALTER statements in `alterations[nn].sql` file
2. Run in phpMyAdmin SQL tab against the live database
3. SSH into server and run fake migrate for affected migrations
4. Run `python manage.py migrate`
5. Copy relevant files from repository to site folder
6. Restart app in cPanel Python app panel

### If migration conflicts (duplicate column/table errors)
- Fake the specific conflicting migration:
```bash
python manage.py migrate --fake userApp [migration_name]
```
- Then run `python manage.py migrate` again
- Repeat until all migrations show `[X]` in `showmigrations`

### Environment variables
The `.env` file is not tracked in git (`.gitignore`) and must be managed manually on the server.

The local `.env` has a date comment at the bottom (`# UPDATED MM/DD/YY`) indicating when it was last updated.

**On each deployment check:**
- Compare the date on the server `.env` with the local `.env`
- If the server `.env` date is older — update it
- The `.env` is organized in local/server pairs — comment out local values and uncomment server values
- Sections to swap:
  - `DEBUG`
  - `Database` — comment local, uncomment server
  - `SITE_URL` — comment local, uncomment server
  - `Email/Address` — comment local, uncomment client

**Never commit the `.env` file to git — it contains passwords and secret keys.**

### Cron jobs
Cron jobs are managed via `django-crontab` — do NOT use the cPanel cron job interface.

**On first deployment or when cron jobs change:**
```bash
source /home/noveleshelf/virtualenv/public_html/api/3.10/bin/activate && cd /home/noveleshelf/public_html/api
python manage.py crontab add
python manage.py crontab show
```

**Current cron jobs:**
| Schedule | Job | Description |
|----------|-----|-------------|
| Daily at midnight | `cron.user_cron.deactivate_unverified_users` | Deactivates unverified users past 7 day grace period |
| Sundays at 3am | `cron.user_cron.flush_expired_tokens` | Cleans up expired JWT tokens |

**Notes:**
- Running `crontab add` removes and re-adds all jobs — this is normal
- Run `crontab add` after any changes to `CRONJOBS` in `settings.py`
- Run `crontab show` to confirm jobs are registered
- New cron functions go in `cron/` folder at the server root

### Testing cron jobs
To test a cron job without waiting for the scheduled time:

**Step 1 — Get job hashes:**
```bash
python manage.py crontab show
```

**Step 2 — Set up test conditions (example for deactivate_unverified_users):**
```bash
python manage.py shell
```
```python
from userApp.models import User
from django.utils import timezone
from datetime import timedelta

user = User.objects.get(email='test@example.com')
user.verification_grace_ends = timezone.now() - timedelta(days=1)
user.save()
exit()
```

**Step 3 — Run the job manually:**
```bash
python manage.py crontab run <hash>
```

**Step 4 — Verify results:**
- Check `logs/cron.log` for file log entry
- Check Django admin → CronApp → Cron logs for database entry
- Verify expected data changes occurred