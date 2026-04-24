# Novel eShelf — Master Project Status

> **Home base:** [`noveleshelf-server`](https://github.com/BeeDev-ValorCollective/noveleshelf-server)
> **Last updated:** 4/24/26
> **Current phase:** booksApp backend in progress · Web auth flow complete · Mobile TBD

---

## Repos at a Glance

| Repo | Purpose | Status |
|------|---------|--------|
| [noveleshelf-server](https://github.com/BeeDev-ValorCollective/noveleshelf-server) | Django/DRF backend API | 🔄 Active — booksApp in progress |
| [noveleshelf-client](https://github.com/BeeDev-ValorCollective/noveleshelf-client) | Vite/React web frontend | 🔄 Active — auth flow done, booksApp integration pending |
| [noveleshelf-app](https://github.com/BeeDev-ValorCollective/noveleshelf-app) | Expo/React Native mobile app | 🔲 Pending — awaiting backend stability |

---

## Cross-Repo Handoff Table

Tracks features/endpoints as they move from backend → web → mobile.
**Status key:** ✅ Done · 🔄 In Progress · 🔲 Not Started · 🚫 Blocked

| Feature | Server | Client (Web) | App (Mobile) | Notes |
|---------|--------|--------------|--------------|-------|
| **Auth — Signup** | ✅ | ✅ | 🔲 | |
| **Auth — Login** | ✅ | ✅ | 🔲 | |
| **Auth — Logout** | ✅ | ✅ | 🔲 | |
| **Auth — Email Verification** | ✅ | 🔲 | 🔲 | 24hr token, 7-day grace |
| **Auth — Resend Verification** | ✅ | 🔲 | 🔲 | |
| **Auth — Change Password** | ✅ | 🔲 | 🔲 | Blacklists all tokens |
| **Auth — Change Email** | ✅ | 🔲 | 🔲 | Blacklists all tokens |
| **Auth — Forgot/Reset Password** | ✅ | 🔲 | 🔲 | |
| **Free Author Upgrade** | ✅ | 🔲 | 🔲 | Self-service |
| **Free Author Profile Update** | ✅ | 🔲 | 🔲 | |
| **Author Requests (all 6 types)** | ✅ | 🔲 | 🔲 | Admin-facing primarily |
| **Admin — Author Request Management** | ✅ | 🔲 | 🔲 | List/update/approve + email triggers |
| **Admin — Deactivate/Reactivate Authors** | ✅ | 🔲 | 🔲 | |
| **Admin — Update Free Author** | ✅ | 🔲 | 🔲 | |
| **Books — Genre/Rating/Tags/Keywords** | 🔄 | 🔲 | 🔲 | Models migrated locally |
| **Books — Book CRUD** | 🔄 | 🔲 | 🔲 | Approval rules in place |
| **Books — Chapter CRUD** | 🔄 | 🔲 | 🔲 | |
| **Books — BookPage** | 🔄 | 🔲 | 🔲 | |
| **Books — Reviews & Comments** | 🔄 | 🔲 | 🔲 | |
| **Books — UserBook (library)** | 🔄 | 🔲 | 🔲 | |
| **Books — Reading Progress** | 🔄 | 🔲 | 🔲 | Tracks unlock_currency_type |
| **Cron — is_new reset (books/chapters)** | 🔄 | N/A | N/A | Book 30d, Chapter 7d |
| **Currency / Payments** | 🔲 | 🔲 | 🔲 | Future currencyApp |

---

## Architecture Decisions Log

Decisions already made — don't re-litigate these.

| # | Decision | Details |
|---|----------|---------|
| 1 | **Dual author profile system** | `AuthorProfile` (paid, admin-created, tier system, contract link) and `FreeAuthorProfile` (self-service, always free books, `is_publicly_visible` defaults True). Both can coexist on one account with separate usernames. |
| 2 | **Paid author book approval** | Paid author books require admin approval before publishing. Free author books publish freely. |
| 3 | **Chapter unlock lock-in** | Books with chapter unlocks cannot be unpublished or deleted. |
| 4 | **`is_complete` is permanent** | Once a book is marked complete, it cannot be undone. |
| 5 | **Featured flags** | On both profile types and books. Admin-managed. Payment handled offline. |
| 6 | **`is_new` resets via cron** | `Book.is_new` resets after 30 days; `Chapter.is_new` after 7 days. |
| 7 | **`unlock_currency_type` choices** | `free`, `black_ink`, `gold_ink`, `quills` — tracked in `UserReadingProgress`. |
| 8 | **Deployment process** | cPanel/MariaDB at `api.noveleshelf.com`. ALTER TABLE workaround via SQL file. Manual copy from `repositories/noveleshelf-server/` to `public_html/api/` after git pull. |
| 9 | **`.env` pattern** | Commented/uncommented pairs for local vs. server settings. Date comment at bottom. |
| 10 | **Frontend API calls** | Use `${import.meta.env.VITE_DB_API}` pattern throughout. |
| 11 | **Header nav pattern** | Uses anchor `href` tags (not React Router `navigate`) for Login/Signup/Dashboard/Logout. |
| 12 | **Auth token blacklist** | Both change-password and change-email blacklist ALL existing tokens. |
| 13 | **AuthorRequest statuses** | `pending`, `in_progress`, `approved`, `not_at_this_time`, `cleared` |
| 14 | **AuthorRequest types** | `new_author`, `new_genre`, `tier_review`, `contract_addendum`, `leave_platform`, `rejoin_platform` |
| 15 | **CronLog** | File logging (`logs/cron.log`) + DB logging via `CronLog` model. |

---

## Per-Repo Tracker Files

- 📋 [Server Tracker](./TRACKER.md) — `noveleshelf-server`
- 📋 Client Tracker — `noveleshelf-client` *(to be created)*
- 📋 App Tracker — `noveleshelf-app` *(to be created)*

---

## Notes / Parking Lot

> Use this section for things that need a decision or are on the radar but not yet scoped.

- `PaymentNameMismatch` log model — noted for future `currencyApp`, not yet designed
- Admin panel approach (Django admin vs. custom frontend) — not yet decided
- Mobile auth flow — needs scoping once backend stabilizes