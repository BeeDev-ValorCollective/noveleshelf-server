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
source /home/noveleshelf/virtualenv/public_html/api/3.10/bin/activate && cd /home/noveleshelf/public_html/api

### Mail Server — [Documentation](mailServer/readme.md)
Contact form email service. May be replaced by the main Django backend at a later date.

---

## Getting Started

### Django API
```bash
cd server
python -m venv venv
source venv/bin/activate  # Mac/Linux
pip install -r requirements.txt
touch .env      # fill in your values
python manage.py migrate
python manage.py runserver
```

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