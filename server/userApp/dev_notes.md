# userApp Developer Notes

## TODO items
- Wire up book visibility changes in `deactivate_author` and `reactivate_author` views when booksApp is built
- Add `has_moderator_profile` check to gate logic when moderator dashboard is built
- Change password — blacklist all tokens on change (already built)
- Change email — send notification to old email address (planned security enhancement)
- Reactivation — trigger mandatory password reset email on reactivation (planned enhancement)
- Payment name mismatch logging — wire up when Stripe/currency app is built
- Deep link support for password reset on native Expo app (Phase 2)

## Future features
- Multiple pen names under one account — currently requires separate login
- Moderator book approval — add moderator to book approval flow
- Free author admin management — expand admin_update_free_author if client requests
- Author featuring payment — currently handled offline, wire up to currency app later

## Notes on existing endpoints
- `deactivate_author` and `reactivate_author` need book visibility updates — see booksApp TODO
- `approve_author_request` handles new_author, leave_platform and rejoin_platform — other request types (new_genre, tier_review etc.) are approved but admin handles changes manually
- `public_authors` needs book count added when booksApp is built