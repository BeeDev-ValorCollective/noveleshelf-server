# noveleshelf-server — Tracker

> Part of the Novel eShelf project · [Master Status](./PROJECT_STATUS.md)
> **Stack:** Django 5.x · DRF · PyMySQL · MariaDB (cPanel/iFast)
> **Deployed at:** `api.noveleshelf.com`
> **Last updated:** 4/24/26

---

## ✅ Completed

### userApp
- [x] Email verification — 24hr token, 7-day grace period
- [x] Resend verification endpoint
- [x] Verify endpoint
- [x] Change password — blacklists all tokens
- [x] Change email — blacklists all tokens
- [x] Forgot password
- [x] Reset password
- [x] Self-service free author upgrade
- [x] Free author profile update endpoint
- [x] `default_login_role` updated to include `free_author`
- [x] **AuthorRequest system**
  - [x] 6 request types: `new_author`, `new_genre`, `tier_review`, `contract_addendum`, `leave_platform`, `rejoin_platform`
  - [x] Statuses: `pending`, `in_progress`, `approved`, `not_at_this_time`, `cleared`
  - [x] Two notes fields: `admin_notes` (internal) · `reader_notes` (user-visible)
- [x] **Admin endpoints**
  - [x] List author requests
  - [x] Update author request
  - [x] Approve author request (with email trigger)
  - [x] Deactivate author (with email trigger)
  - [x] Reactivate author (with email trigger)
  - [x] Update free author profile

### cronApp
- [x] `CronLog` model
- [x] File logging → `logs/cron.log`
- [x] DB logging
- [x] booksApp cron jobs scaffolded in `cron/books_cron.py`
  - [x] `Book.is_new` reset after 30 days
  - [x] `Chapter.is_new` reset after 7 days

### booksApp — Models & Migrations (local)
- [x] `Genre`
- [x] `ContentRating`
- [x] `RelationshipTag`
- [x] `Keyword`
- [x] `Book` (with paid author approval rules, `is_complete` permanence, unlock lock-in)
- [x] `BookPage`
- [x] `BookGenre`
- [x] `BookRelationshipTag`
- [x] `BookKeyword`
- [x] `Chapter`
- [x] `BookReview`
- [x] `ChapterComment`
- [x] `UserBook`
- [x] `UserReadingProgress` (with `unlock_currency_type`: `free`, `black_ink`, `gold_ink`, `quills`)
- [x] Signals
- [x] Serializers

---

## 🔄 In Progress

### booksApp — Endpoints & Views
- [ ] Genre endpoints (list, detail — probably read-only for most users)
- [ ] ContentRating endpoints
- [ ] Book CRUD endpoints
  - [ ] Create (paid author → pending approval; free author → publishes freely)
  - [ ] Read / list (public browse)
  - [ ] Update (author-owned, with restriction checks)
  - [ ] Delete (blocked if chapter unlocks exist)
- [ ] Chapter CRUD endpoints
- [ ] BookPage endpoints
- [ ] BookReview endpoints
- [ ] ChapterComment endpoints
- [ ] UserBook endpoints (reader library)
- [ ] UserReadingProgress endpoints
- [ ] **Admin endpoints for book approval**
  - [ ] List pending books
  - [ ] Approve/reject book

### Deployment
- [ ] booksApp migrations need to be deployed to production via SQL file workaround
- [ ] Verify cron jobs are wired up on production server

---

## 🔲 Up Next Queue

*Ordered by priority — work top to bottom.*

1. **Finish booksApp views/endpoints** — get the API to feature-complete for books
2. **Wire up booksApp admin endpoints** — book approval flow
3. **Deploy booksApp to production** — SQL workaround for ALTER TABLE, copy files
4. **Verify cron on production** — confirm `is_new` resets are running
5. **Scope currencyApp** — `PaymentNameMismatch` log noted but not yet designed
6. **Scope admin panel approach** — Django admin vs. custom frontend decision needed

---

## 🔗 Ready to Hand Off to Client/App

*Server work done — these are waiting on the frontend teams.*

| Endpoint Group | Ready For | Notes |
|----------------|-----------|-------|
| All userApp auth endpoints | Client (web) · App (mobile) | Fully deployed |
| Author request endpoints (user-facing) | Client (web) | User can submit requests |
| Admin endpoints | Client (web) — admin views | Email triggers fire automatically |
| Free author upgrade/profile | Client (web) · App (mobile) | |

---

## 🚫 Blocked / Waiting On

*Nothing currently blocked — note anything here that's stalled waiting on a decision or external dependency.*

---

## 🗒️ Notes

- ALTER TABLE workaround: export schema changes as SQL file, run manually on production via cPanel phpMyAdmin or CLI
- After any git pull on server: manually copy from `repositories/noveleshelf-server/` → `public_html/api/`
- `.env` uses commented/uncommented pairs for local vs. server; date comment at bottom marks last switch