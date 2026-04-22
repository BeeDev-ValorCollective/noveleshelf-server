# Novel eShelf — booksApp

Handles all book, chapter, genre, and reading progress functionality.

---

[← Back to Server README](../README.md)

---

## Endpoints

### Admin endpoints (`/api/books/admin/`)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | /api/books/admin/genres/ | List all genres | Yes |
| POST | /api/books/admin/genres/create/ | Create genre | Yes |
| PATCH | /api/books/admin/genres/update/ | Update genre | Yes |
| GET | /api/books/admin/content-ratings/ | List all content ratings | Yes |
| POST | /api/books/admin/content-ratings/create/ | Create content rating | Yes |
| PATCH | /api/books/admin/content-ratings/update/ | Update content rating | Yes |
| GET | /api/books/admin/relationship-tags/ | List all relationship tags | Yes |
| POST | /api/books/admin/relationship-tags/create/ | Create relationship tag | Yes |
| PATCH | /api/books/admin/relationship-tags/update/ | Update relationship tag | Yes |
| GET | /api/books/admin/keywords/ | List all keywords | Yes |
| POST | /api/books/admin/keywords/create/ | Create keyword | Yes |
| PATCH | /api/books/admin/keywords/update/ | Update keyword | Yes |
| GET | /api/books/admin/books/ | List all books | Yes |
| PATCH | /api/books/admin/books/update/ | Update book | Yes |
| POST | /api/books/admin/books/approve/ | Approve book | Yes |
| POST | /api/books/admin/books/request-changes/ | Request book changes | Yes |
| GET | /api/books/admin/flagged/reviews/ | List flagged reviews | Yes |
| GET | /api/books/admin/flagged/comments/ | List flagged comments | Yes |
| DELETE | /api/books/admin/reviews/delete/ | Delete review | Yes |
| DELETE | /api/books/admin/comments/delete/ | Delete comment | Yes |

### Author endpoints (`/api/books/author/`)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | /api/books/author/books/create/ | Create book | Yes |
| GET | /api/books/author/books/ | List my books | Yes |
| PATCH | /api/books/author/books/update/ | Update book | Yes |
| POST | /api/books/author/books/submit/ | Submit book for approval | Yes |
| POST | /api/books/author/books/complete/ | Mark book as complete | Yes |
| POST | /api/books/author/chapters/create/ | Create chapter | Yes |
| GET | /api/books/author/chapters/ | List my chapters | Yes |
| PATCH | /api/books/author/chapters/update/ | Update chapter | Yes |
| POST | /api/books/author/chapters/publish/ | Publish chapter | Yes |
| POST | /api/books/author/chapters/unpublish/ | Unpublish chapter | Yes |
| DELETE | /api/books/author/chapters/delete/ | Delete chapter | Yes |
| POST | /api/books/author/pages/create-update/ | Create or update book page | Yes |
| POST | /api/books/author/pages/publish/ | Publish book page | Yes |
| POST | /api/books/author/pages/unpublish/ | Unpublish book page | Yes |

### Reader endpoints (`/api/books/reader/`)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | /api/books/reader/books/ | List all visible books | Yes |
| GET | /api/books/reader/books/<id>/ | Get book details | Yes |
| GET | /api/books/reader/search/ | Search books | Yes |
| GET | /api/books/reader/chapters/<id>/ | Get chapter content | Yes |
| POST | /api/books/reader/chapters/unlock/ | Unlock chapter | Yes |
| GET | /api/books/reader/library/ | My library | Yes |
| GET | /api/books/reader/progress/<book_id>/ | Reading progress for book | Yes |
| POST | /api/books/reader/reviews/create/ | Create review | Yes |
| PATCH | /api/books/reader/reviews/update/ | Update review | Yes |
| GET | /api/books/reader/reviews/<book_id>/ | List book reviews | Yes |
| POST | /api/books/reader/comments/create/ | Create comment | Yes |
| GET | /api/books/reader/comments/<chapter_id>/ | List chapter comments | Yes |
| POST | /api/books/reader/reviews/flag/ | Flag review | Yes |
| POST | /api/books/reader/comments/flag/ | Flag comment | Yes |

### Public endpoints (`/api/books/public/`)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | /api/books/public/books/ | List all visible books | No |
| GET | /api/books/public/books/<id>/ | Get book details | No |

---

## Endpoint Details

*Endpoint details will be added as views are built and tested.*

---

## Notes for developers

See [DEVELOPER_NOTES.md](DEVELOPER_NOTES.md) for full details on:
- Model descriptions and business rules
- View specifications
- TODO items
- Frontend notes

---

[← Back to Server README](../README.md)