# Novel eShelf — currencyApp

Handles the platform's virtual currency system: wallet balances, transaction history, the daily login reward, and admin-driven manual currency adjustments.

---

[← Back to Server README](../readme.md)

---

## Overview

Novel eShelf uses three currency types, all tracked on `UserWallet` (defined in `userApp`):

| Currency | Field | How it's earned |
|----------|-------|------------------|
| Black Ink Drops | `black_ink_balance` | Daily login reward (automatic) |
| Gold Ink Drops | `gold_ink_balance` | Watching ads — **not yet built** |
| Quills | `quill_balance` | Stripe purchase — **not yet built** |

Every change to a wallet balance — earned, spent, or manually adjusted — writes a `Transaction` record. This is the system's full audit trail; there is currently no other way to reconstruct wallet history.

Chapter unlock spend order is always **black_ink → gold_ink → quills** (see `booksApp` README, [Unlock chapter](../booksApp/README.md#unlock-chapter)).

---

## Endpoints

### Admin endpoints (`/api/currency/admin/`)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | /api/currency/admin/add/ | [Manually add currency to a user](#manually-add-currency-to-a-user) | Yes (super admin) |

There is no endpoint to trigger the daily login reward directly — it fires automatically as a side effect of the `/me/` request in `userApp`, not through a `currencyApp` URL.

---

## Endpoint Details

### Manually add currency to a user
#### Headers:
```
Authorization    Bearer <access_token>
Content-Type     application/json
```
#### Body:
```json
{
    "user_id": 1,
    "currency_type": "quills",
    "amount": 50,
    "notes": "Testing chapter unlock flow"
}
```
#### Success response 200:
```json
{
    "detail": "Added 50 quills to melissa@beedev-services.com.",
    "wallet": {
        "quill_balance": 50,
        "gold_ink_balance": 0,
        "black_ink_balance": 8
    }
}
```
#### Error responses:
```json
403: {"detail": "Super admin access required."}
400: {"detail": "user_id, currency_type, and amount are required."}
400: {"detail": "currency_type must be one of: black_ink, gold_ink, quills"}
400: {"detail": "amount must be a positive integer."}
404: User not found
```
#### Notes:
- Restricted to `is_super_admin` accounts only (checked via `request.user.admin_profile.is_super_admin`)
- `notes` is optional — defaults to `"Manual admin credit"`, and the requesting admin's email is always appended automatically
- Writes a `Transaction` with `transaction_type: admin_adjustment`
- Creates the user's `UserWallet` if it doesn't exist yet (`get_or_create`)
- This is a temporary testing tool — Stripe (Quills) and ad-reward (Gold Ink) flows will eventually replace most real-world use of this endpoint, but it stays available afterward for support/customer-service adjustments

---

## How the Daily Login Reward Works

There's no dedicated endpoint for this — it's triggered as a side effect inside the `userApp` `/me/` view on every call, via `process_daily_login_reward(user)` in `currencyApp/views/reward_views.py`.

**Logic:**
1. Look up (or create) the user's `DailyLoginReward` record
2. If `last_reward_date` is already today, do nothing — return `False`
3. Otherwise, read `daily_black_ink_reward` from `PlatformSettings` (defaults to `2` if no settings row exists)
4. Add that amount to `wallet.black_ink_balance`
5. Update `last_reward_date` to today and increment `total_earned`
6. Write a `Transaction` with `transaction_type: daily_login`
7. Return `True`

**Why it fires on `/me/` instead of login:** mobile app sessions can stay logged in for days without hitting a literal "login" endpoint. Tying the reward to `/me/` (called on every app open / token refresh) ensures readers get credit for showing up daily regardless of platform.

**Changing the reward amount:** edit the single `PlatformSettings` row in Django admin — no code or deploy needed. There should only ever be one `PlatformSettings` row (singleton pattern); if none exists, the reward falls back to a hardcoded default of `2`.

---

## Models

### `DailyLoginReward`
One-to-one with `User`. Tracks `last_reward_date` (used to prevent double-rewarding the same day) and a running `total_earned` lifetime counter.

### `Transaction`
The audit log. Every wallet change — earned or spent — gets a row here.

**`transaction_type` choices:**

| Value | Meaning | Status |
|-------|---------|--------|
| `daily_login` | Daily login black ink reward | ✅ Live |
| `chapter_unlock` | Currency spent unlocking a chapter | ✅ Live (in `booksApp`) |
| `admin_adjustment` | Manual admin-added currency | ✅ Live |
| `ad_reward` | Gold ink earned by watching an ad | 🚧 Not built |
| `quill_purchase` | Quills purchased via Stripe | 🚧 Not built |
| `author_payout` | Author's earnings payout | 🚧 Not built — payout logic not designed yet |

**`currency_type` choices:** `black_ink`, `gold_ink`, `quills`

`amount` is signed — positive for credits, negative for spends (see `chapter_unlock` transactions in `booksApp`, which write negative amounts per currency actually used).

`balance_after` records the wallet balance for that specific currency immediately after the transaction, making it possible to reconstruct historical balances without recalculating from scratch.

### `PlatformSettings`
Singleton model (only one row should ever exist) holding platform-wide tunables. Currently just `daily_black_ink_reward`. Manage via Django admin.

---

## Parking Lot

> Things known to be missing or not yet decided — not blockers for current testing, but worth tracking.

- **Gold Ink Drop ad-reward flow** — no ad integration or endpoint yet. `ad_reward` transaction type exists in the model but nothing writes it.
- **Quill purchases via Stripe** — not built. `quill_purchase` transaction type exists but nothing writes it.
- **Author payout calculation** — business logic for splitting revenue to authors (50% ink-funded unlocks, 30% quill-funded unlocks per earlier discussions) is not designed or built. `author_payout` transaction type exists as a placeholder only.
- **Admin currency add — permission scope** — currently restricted to super admin only. May loosen to "any admin" once Django Groups permissions are in place to control this more granularly per the client/staff group system being built separately.

---

[← Back to Server README](../readme.md)