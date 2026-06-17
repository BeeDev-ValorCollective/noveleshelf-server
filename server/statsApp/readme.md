# Novel eShelf — statsApp

Houses reporting and analytics across the platform — admin-facing stats today, with author and reader stats planned as the same pattern grows. Read-only aggregation lives here; it does not own the underlying data (transactions, books, library entries, etc.), it only reports on it.

---

[← Back to Server README](../readme.md)

---

## Overview

`statsApp` is organized by audience, mirroring the `booksApp` pattern:

| Folder | Audience | Status |
|--------|----------|--------|
| `views/admin_views.py` | Platform admins | ✅ Live |
| `views/author_views.py` | Authors (e.g. earnings, readership) | 🚧 Not built |
| `views/reader_views.py` | Readers (e.g. reading stats) | 🚧 Not built |

URLs follow the same split: `/api/stats/admin/`, with `/api/stats/author/` and `/api/stats/reader/` to be added later.

This app currently has no models of its own — all admin endpoints below query existing models from other apps (`currencyApp.Transaction`). A future analytics feature (site visit / ad-source tracking) is planned to live here as well, and will likely introduce this app's first models.

---

## Endpoints

### Admin endpoints (`/api/stats/admin/`)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | /api/stats/admin/transactions/ | [Search transaction log](#search-transaction-log) | Yes (admin) |
| GET | /api/stats/admin/transactions/totals/ | [Transaction totals by type](#transaction-totals-by-type) | Yes (admin) |

---

## Endpoint Details

### Search transaction log
#### Headers:
```
Authorization    Bearer <access_token>
```
#### Query Parameters (all optional):
| Param | Type | Notes |
|-------|------|-------|
| `user_id` | int | Filter to one user |
| `transaction_type` | string | One of `Transaction.TRANSACTION_TYPES` |
| `currency_type` | string | `black_ink`, `gold_ink`, or `quills` |
| `date_from` | date (`YYYY-MM-DD`) | Used alone, filters to that single day |
| `date_to` | date (`YYYY-MM-DD`) | Used with `date_from`, filters an inclusive range |
| `page` | int | Standard DRF page number pagination |

#### Example:
```
GET /api/stats/admin/transactions/?transaction_type=admin_gift&date_from=2026-06-17
```
#### Success response 200:
```json
{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 42,
            "user_id": 1,
            "user_email": "melissa@beedev-services.com",
            "transaction_type": "admin_gift",
            "currency_type": "black_ink",
            "amount": 10,
            "balance_after": 18,
            "notes": "Testing gift endpoint (gifted by melissa@beedev-services.com)",
            "created_at": "2026-06-17T14:02:11Z"
        }
    ]
}
```
#### Error responses:
```json
403: {"detail": "Admin access required."}
```
#### Notes:
- Open to any admin account (checked via `hasattr(request.user, 'admin_profile')`), not restricted to super admin
- Paginated at 25 results per page using DRF's `PageNumberPagination` (no global default is configured in `settings.py`, so this is set explicitly in the view)
- Results are ordered newest-first, per `Transaction.Meta.ordering`
- All filters are combinable (e.g. `user_id` + `transaction_type` + date range together)

---

### Transaction totals by type
#### Headers:
```
Authorization    Bearer <access_token>
```
#### Query Parameters (all optional):
| Param | Type | Notes |
|-------|------|-------|
| `date_from` | date (`YYYY-MM-DD`) | Used alone, totals for that single day |
| `date_to` | date (`YYYY-MM-DD`) | Used with `date_from`, totals over an inclusive range |

Omitting both returns all-time totals.

#### Example:
```
GET /api/stats/admin/transactions/totals/
```
#### Success response 200:
```json
{
    "daily_login": { "count": 142, "total_amount": 284 },
    "ad_reward": { "count": 0, "total_amount": 0 },
    "quill_purchase": { "count": 0, "total_amount": 0 },
    "chapter_unlock": { "count": 12, "total_amount": -340 },
    "author_payout": { "count": 0, "total_amount": 0 },
    "admin_adjustment": { "count": 2, "total_amount": 100 },
    "admin_gift": { "count": 1, "total_amount": 10 }
}
```
#### Error responses:
```json
403: {"detail": "Admin access required."}
```
#### Notes:
- Every `transaction_type` from `Transaction.TRANSACTION_TYPES` is always present in the response, with `count: 0, total_amount: 0` if no matching rows exist — the response shape never changes based on data
- `total_amount` is a sum of the signed `amount` field, so spend-type transactions (e.g. `chapter_unlock`) appear as negative totals — this is expected, not a bug
- Date filtering uses the same `date_from`/`date_to` rules as the transaction log endpoint above

---

## Parking Lot

> Things known to be missing or not yet decided — not blockers for current testing, but worth tracking.

- **Author stats** — not designed yet. Likely candidates: earnings over time, most-read chapters, follower counts.
- **Reader stats** — not designed yet. Likely candidates: books in library, chapters read, currency spent.
- **Site analytics / ad attribution** — separate, larger feature (UTM tracking, landing page visits, signup source attribution) discussed with the client but deliberately deferred. Will likely require this app's first model(s) and a public (unauthenticated) tracking endpoint, in addition to admin-facing reporting views.
- **Serializer for transaction log** — currently built as a manual dict in the view rather than a DRF serializer. Revisit if a `TransactionSerializer` already exists elsewhere or becomes worth standardizing.

---

[← Back to Server README](../readme.md)