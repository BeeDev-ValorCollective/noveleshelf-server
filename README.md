# NovelShelf Server

This repository contains the backend services for the NovelShelf platform.

---

## Repository Structure
```
noveleshelf-server/
├── mailServer/          — Contact form email service (Node, iFast)
├── server/              — Django REST API backend (Digital Ocean)
└── README.md
```

---

## Services

### Django API — [Documentation](server/readme.md)
The main backend API for the NovelShelf platform. Handles authentication, user management, books, chapters, and currency.

- Built with Django 5.x and Django REST Framework
- MySQL/MariaDB database
- JWT authentication
- Hosted on Digital Ocean (Ubuntu, gunicorn + nginx)

#### Shell access:
```
ssh root@64.225.52.134
cd /var/www/noveleshelf/noveleshelf-server
source /var/www/noveleshelf/venv/bin/activate
```

See `server/readme.md` for full deployment commands.

### Mail Server — [Documentation](mailServer/readme.md)
Contact form email service. Node.js, deployed on iFast cPanel hosting. May be replaced by the main Django backend at a later date.

#### Shell access:
```
ssh -p 1394 noveleshelf@noveleshelf.com
```
Password is the db password on env. To activate the environment:
```bash
source /home/noveleshelf/virtualenv/public_html/api/3.10/bin/activate && cd /home/noveleshelf/public_html/api
```

> **Note:** the iFast/cPanel access info above was previously (and incorrectly) listed under the Django API section in this README. The Django API moved to Digital Ocean — this cPanel access is for `mailServer` only. If `mailServer` is itself Node (not the Python venv path shown), confirm and correct this shell access block — the venv path was carried over from before the split and may no longer be accurate for the Node mail service.

---

## Getting Started

### Django API
```bash
cd server
python -m venv venv
source venv/bin/activate  # Mac/Linux (windows = venv/Scripts/activate)
pip install -r requirements.txt
touch .env      # copy on drive update local mysql password
python manage.py migrate
python manage.py runserver
```

---

## Environment Variables
See Google drive for current required variables and create the env file inside `server/server/.env`.

---

## Backend Tech Stack
- **Backend**: Django 5.x, Django REST Framework
- **Database**: MySQL / MariaDB
- **Auth**: JWT via djangorestframework-simplejwt
- **Storage**: Local (S3 planned)
- **Email**: Google Workspace SMTP
- **Hosting**: Digital Ocean (Ubuntu, gunicorn + nginx) — IP `64.225.52.134`

---

## Frontend Tech Stack
- **Web (Vite):** React, React Router, Zustand
- **Mobile (Expo):** React Native, Expo Router, Zustand, Tamagui
- **Shared:** Zustand store logic is largely reusable across both platforms

---

## Deployment — Django API (Digital Ocean)

### Standard deploy (code changes, no database changes)
```
ssh root@64.225.52.134
cd /var/www/noveleshelf/noveleshelf-server
git pull origin deployed
cd server
source /var/www/noveleshelf/venv/bin/activate
python3 manage.py migrate
sudo systemctl restart gunicorn
sudo systemctl status gunicorn
```

### New tables / schema changes
MariaDB on this host has `ALTER TABLE` restrictions, so schema changes need a SQL file workaround rather than relying on `manage.py migrate` alone for the DDL:
1. Generate the migration locally as normal (`python manage.py makemigrations`)
2. Export the resulting schema change as a SQL file
3. Run the SQL file manually against the production database (via the DO box directly or your MySQL client of choice — confirm current preferred method, this may have changed since cPanel days)
4. SSH in, pull the code, and run `python3 manage.py migrate --fake` if needed to sync Django's migration state with the manually-applied schema, then `python3 manage.py migrate`
5. Restart gunicorn

> **This section needs verification.** The previous cPanel/phpMyAdmin-based process (export structure only, find/replace collation, disable foreign key checks, import via phpMyAdmin) doesn't apply on Digital Ocean — there's no phpMyAdmin in this setup by default. Confirm and document the actual current process for schema changes next time one is needed, rather than relying on this placeholder.

### If migration conflicts (duplicate column/table errors)
```bash
python manage.py migrate --fake booksApp [migration_name]
```
Then run `python manage.py migrate` again. Repeat until all migrations show `[X]` in `showmigrations`.

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
Cron jobs are managed via `django-crontab`.

**On first deployment or when cron jobs change:**
```bash
ssh root@64.225.52.134
cd /var/www/noveleshelf/noveleshelf-server/server
source /var/www/noveleshelf/venv/bin/activate
python manage.py crontab add
python manage.py crontab show
```

**Current cron jobs:** see [`server/cronApp/readme.md`](server/cronApp/readme.md) — kept there as the single source of truth so this file doesn't drift out of sync with `settings.py` again.

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

---

## Deployment — Mail Server (iFast/cPanel)

See [`mailServer/readme.md`](mailServer/readme.md) for Node-specific deployment steps on iFast. Not yet documented in this top-level file — add a summary here once that README is reviewed.
