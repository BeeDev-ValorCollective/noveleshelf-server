# Novel eShelf — booksApp

Handles all book, chapter, genre, and reading progress functionality.

---

[← Back to Server README](../README.md)

---

## Overview

The booksApp is split into three URL files based on who is accessing the endpoints:

| URL File | Prefix | Who Uses It | Platform |
|----------|--------|-------------|----------|
| `urls_admin.py` | `/api/books/admin/` | Admin/Moderator | Vite (noveleshelf.com) |
| `urls_author.py` | `/api/books/author/` | Paid and Free Authors | Vite (noveleshelf.com) |
| `urls_reader.py` | `/api/books/reader/` | Readers | Expo (app.noveleshelf.com) |
| `urls_public.py` | `/api/books/public/` | Anyone | Vite (noveleshelf.com) |

---

## Models

### Lookup tables (admin managed)
- `Genre` — book genres, admin adds/deactivates
- `ContentRating` — G, YA, M, E, X ratings
- `RelationshipTag` — F/M, M/M, F/F, POLY
- `Keyword` — searchable keywords like Dragon, Vampire etc.

### Core models
- `Book` — the main book record
- `BookPage` — special pages like prologue, epilogue, author's note
- `Chapter` — individual chapters
- `BookGenre` — many to many between Book and Genre
- `BookRelationshipTag` — many to many between Book and RelationshipTag
- `BookKeyword` — many to many between Book and Keyword

### Reader models
- `BookReview` — one review per user per book, with flag count
- `ChapterComment` — flat comments per chapter, with flag count
- `UserBook` — tracks a reader's relationship with a book — completion, last read
- `UserReadingProgress` — tracks per chapter unlock and read status

---

## Key Business Rules

### Free vs Paid books
- Books by `FreeAuthorProfile` authors are always free — no currency needed
- Books by `AuthorProfile` (paid) authors require currency to unlock chapters past the free threshold
- `Book.free_chapters` defaults to 3 — first 3 chapters always free for paid books
- `Chapter.is_free` is set automatically by signal when chapter is published

### Book approval (paid authors only)
- Paid author creates book → status = `draft`
- Author submits for review → status = `pending_approval`
- Admin approves → status = `approved`, author can publish chapters
- Admin requests changes → status = `changes_requested`
- Once first chapter of an approved book is published subsequent chapters publish freely
- Free author books do not need approval — publish freely

### Chapter publishing
- Auto numbered per book — next available number assigned automatically
- `is_free` set automatically based on `chapter_number <= book.free_chapters`
- `published_at` set automatically when status changes to published
- `is_new` defaults to True, cron job sets to False after 7 days
- Once published with unlocks — cannot be unpublished or deleted
- Published with no unlocks — can be unpublished back to draft

### Book visibility
- `is_visible = False` — book hidden from new readers, existing unlocks preserved
- Set automatically when author deactivates (TODO — wire up in deactivate_author view)
- Admin can manually set per book

### Reading and unlocking
- When reader opens any chapter a `UserReadingProgress` record is created
- Free chapters → `unlock_currency_type = 'free'`, no wallet deduction
- Paid chapters → currency deducted from wallet in order: black_ink first, then gold_ink, then quills
- Once unlocked always unlocked — even if book becomes hidden or paid
- `UserBook.completion_percentage` updates automatically via signal when chapter is read
- `UserBook.is_completed` set to True when book is complete and all chapters read

### Featured books
- `Book.is_featured` — admin sets, payment handled offline
- Use `?featured=true` query param on public endpoints to get featured books only

### New flags
- `Book.is_new` — True for 30 days from first published chapter, cron job resets
- `Chapter.is_new` — True for 7 days from published date, cron job resets

---

## Views to Build

### `views/admin_views.py`

**Lookup table management (Genre, ContentRating, RelationshipTag, Keyword):**
- `list_genres` — GET, list all with is_active filter
- `create_genre` — POST, create new genre
- `update_genre` — PATCH, update name or is_active
- Same pattern for ContentRating, RelationshipTag, Keyword

**Book management:**
- `list_books_admin` — GET, all books with filters (status, author, featured)
- `update_book_admin` — PATCH, update status, admin_notes, reader_notes, is_visible, is_featured, free_chapters
- `approve_book` — POST, sets status to approved, sends email to author
- `request_book_changes` — POST, sets status to changes_requested, sends email with notes

**Flagged content:**
- `list_flagged_reviews` — GET, reviews with flag_count > 0
- `list_flagged_comments` — GET, comments with flag_count > 0
- `delete_review` — DELETE, remove flagged review
- `delete_comment` — DELETE, remove flagged comment

### `views/author_views.py`

**Book management:**
- `create_book` — POST, create new book, sets book_tier from author tier
- `list_my_books` — GET, author's own books
- `update_book` — PATCH, update title, description, cover, content_rating, genres, tags, keywords
- `submit_book_for_approval` — POST, changes status from draft to pending_approval (paid authors only)
- `mark_book_complete` — POST, sets is_complete to True — cannot be undone
- `convert_book_to_paid` — POST, convert free book to paid — complex logic (see notes below)

**Chapter management:**
- `create_chapter` — POST, auto assigns next chapter number
- `list_my_chapters` — GET, chapters for a specific book
- `update_chapter` — PATCH, update title and content
- `publish_chapter` — POST, sets status to published
- `unpublish_chapter` — POST, sets status back to draft — only if no unlocks exist
- `delete_chapter` — DELETE — only if draft or published with no unlocks

**Book pages:**
- `create_update_page` — POST/PATCH, create or update a book page (prologue, epilogue etc.)
- `publish_page` — POST, sets is_published to True
- `unpublish_page` — POST, sets is_published to False

### `views/reader_views.py`

**Browsing:**
- `list_books` — GET, all visible approved books with filters (genre, rating, keyword, featured, new, free_only)
- `get_book` — GET, single book details with chapters list (no content)
- `search_books` — GET, search by title, author username, pen name, genre

**Reading:**
- `get_chapter` — GET, returns chapter content if unlocked or free — creates UserReadingProgress record
- `unlock_chapter` — POST, deducts currency and creates unlock record

**Library:**
- `my_library` — GET, all books user has started or unlocked chapters in
- `my_reading_progress` — GET, reading progress for a specific book

**Reviews and comments:**
- `create_review` — POST, one per user per book
- `update_review` — PATCH, update own review
- `list_reviews` — GET, all reviews for a book
- `create_comment` — POST, comment on a chapter
- `list_comments` — GET, all comments for a chapter
- `flag_review` — POST, increment flag_count on a review
- `flag_comment` — POST, increment flag_count on a comment

### `views/public_views.py`
- `list_books_public` — GET, all visible approved books, no auth needed, with featured filter
- `get_book_public` — GET, single book details, no auth needed

---

## Convert Free Book to Paid (complex logic)

When a free author upgrades to paid author and wants to convert a free book:

1. Check if any chapters have been unlocked — they will always have `unlock_currency_type = 'free'`
2. Chapters with existing free unlocks — readers keep access, chapter stays accessible to them
3. Chapters with no unlocks — can be switched to paid
4. Going forward new chapters are paid

This is a future feature — note it as TODO for now.

---

## Notes for Frontend Team

### Vite (noveleshelf.com) handles:
- Author dashboard — book creation, chapter uploads, book pages
- Admin dashboard — genre management, book approval, flagged content
- Public book listings

### Expo (app.noveleshelf.com) handles:
- Reader library
- Reading experience
- Unlocking chapters
- Reviews and comments

### Currency order for unlocking
When unlocking a chapter deduct in this order:
1. Black ink drops first
2. Gold ink drops second
3. Quills last

### Book tier snapshot
`Book.book_tier` is a snapshot of the author's tier at time of book creation. If the author's tier changes later existing books keep their original tier rate. New books get the new tier rate.

---

## TODO items
- Wire up book visibility changes in `deactivate_author` view in userApp
- Build convert free book to paid logic
- Add book count to public authors endpoint
- Add featured filter to public book listings