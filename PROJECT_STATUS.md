# Novel eShelf — Architecture Decisions Log

> **Home base:** [`noveleshelf-server`](https://github.com/BeeDev-ValorCollective/noveleshelf-server)
> **Last updated:** 6/17/26 — trimmed to decisions log only; the cross-repo handoff table and per-repo status sections were removed because they went stale and were no longer maintained. Current status now lives in each app's own README (Parking Lot sections) rather than a separate hand-maintained tracker.

---

## Architecture Decisions Log

Decisions already made — don't re-litigate these. This list only grows when a new durable, rarely-changing decision is made — not a place for in-progress feature status.

| # | Decision | Details |
|---|----------|---------|
| 1 | **Dual author profile system** | `AuthorProfile` (paid, admin-created, tier system, contract link) and `FreeAuthorProfile` (self-service, always free books, `is_publicly_visible` defaults True). Both can coexist on one account with separate usernames. |
| 2 | **Paid author book approval** | Paid author books require admin approval before publishing. Free author books publish freely. |
| 3 | **Chapter unlock lock-in** | Books with chapter unlocks cannot be unpublished or deleted. |
| 4 | **`is_complete` is permanent** | Once a book is marked complete, it cannot be undone. |
| 5 | **Featured flags** | On both profile types and books. Admin-managed. Payment handled offline. |
| 6 | **`is_new` resets via cron** | `Book.is_new` resets after 30 days; `Chapter.is_new` after 7 days. See `cronApp` README for the current job list. |
| 7 | **`unlock_currency_type` choices** | `free`, `black_ink`, `gold_ink`, `quills` — tracked in `UserReadingProgress`. Spend order on unlock is always black_ink → gold_ink → quills. |
| 8 | **`.env` pattern** | Commented/uncommented pairs for local vs. server settings. Date comment at bottom. |
| 9 | **Auth token blacklist** | Both change-password and change-email blacklist ALL existing tokens. |
| 10 | **AuthorRequest statuses** | `pending`, `in_progress`, `approved`, `not_at_this_time`, `cleared` |
| 11 | **AuthorRequest types** | `new_author`, `new_genre`, `tier_review`, `contract_addendum`, `leave_platform`, `rejoin_platform` |
| 12 | **CronLog** | File logging (`logs/cron.log`) + DB logging via `CronLog` model. |
| 13 | **Daily login reward fires on `/me/`, not login** | Ensures mobile sessions that stay logged in for days still get credited daily, since they may not hit a literal login endpoint often. |
| 14 | **Quills purchased via Stripe on web only** | Sidesteps Apple/Google 30% in-app purchase cut. Ink Drops (black/gold) are earned, not purchased, so no app store payment rules apply to them. |
| 15 | **Follow system lives under its own `/api/follow/` prefix** | Not nested under `/api/user/` — uses `author_profile_id`/`free_author_profile_id` directly rather than a combined `author_type`/`author_id` pair. |

---

## Removed sections (for context, not to be restored)

The following sections were removed from this file on 6/17/26 because they had drifted from reality and were not being kept current:
- **Repos at a Glance** — repo status summary
- **Cross-Repo Handoff Table** — feature-by-feature server/client/app status
- **Per-Repo Tracker Files** — links to `TRACKER.md` files
- **Notes / Parking Lot** — superseded by the Parking Lot sections now living in each app's own README and the server-level README

If a cross-repo status view becomes useful again later, prefer pulling current status fresh from each app's README Parking Lot rather than reviving a separate hand-maintained table.