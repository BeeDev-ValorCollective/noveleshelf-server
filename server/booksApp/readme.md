# Novel eShelf — booksApp

Handles all book, chapter, genre, and reading progress functionality.

---

[← Back to Server README](../readme.md)

---

## Endpoints

### Admin endpoints (`/api/books/admin/`)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | /api/books/admin/genres/ | [List all genres](#list-genres) | Yes |
| POST | /api/books/admin/genres/create/ | [Create genre](#create-genre) | Yes |
| PATCH | /api/books/admin/genres/update/ | [Update genre](#update-genre) | Yes |
| GET | /api/books/admin/content-ratings/ | [List all content ratings](#list-content-ratings) | Yes |
| POST | /api/books/admin/content-ratings/create/ | [Create content rating](#create-content-rating) | Yes |
| PATCH | /api/books/admin/content-ratings/update/ | [Update content rating](#update-content-rating) | Yes |
| GET | /api/books/admin/relationship-tags/ | [List all relationship tags](#list-relationship-tags) | Yes |
| POST | /api/books/admin/relationship-tags/create/ | [Create relationship tag](#create-relationship-tag) | Yes |
| PATCH | /api/books/admin/relationship-tags/update/ | [Update relationship tag](#update-relationship-tag) | Yes |
| GET | /api/books/admin/keywords/ | [List all keywords](#list-keywords) | Yes |
| POST | /api/books/admin/keywords/create/ | [Create keyword](#create-keyword) | Yes |
| PATCH | /api/books/admin/keywords/update/ | [Update keyword](#update-keyword) | Yes |
| GET | /api/books/admin/books/ | [List all books](#list-all-books-admin) | Yes |
| PATCH | /api/books/admin/books/update/ | [Update book](#admin-update-book) | Yes |
| POST | /api/books/admin/books/approve/ | [Approve book](#approve-book) | Yes |
| POST | /api/books/admin/books/request-changes/ | [Request book changes](#request-book-changes) | Yes |
| POST | /api/books/admin/books/reject/ | [Reject book](#reject-book) | Yes |

> **Not yet built:** flagged review/comment moderation endpoints (`flagged/reviews/`, `flagged/comments/`, review/comment delete). Reviews and comments are not implemented anywhere in the app yet — see Parking Lot below.

### Author endpoints (`/api/books/author/`)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | /api/books/author/books/create/ | [Create book](#create-book) | Yes |
| GET | /api/books/author/books/ | [List my books](#list-my-books) | Yes |
| GET | /api/books/author/books/<id>/ | [Get book detail (manage view)](#get-book-detail-manage-view) | Yes |
| PATCH | /api/books/author/books/update/ | [Update book](#update-book) | Yes |
| POST | /api/books/author/books/submit/ | [Submit book for approval](#submit-book-for-approval) | Yes |
| DELETE | /api/books/author/books/delete/ | [Delete book](#delete-book) | Yes |
| POST | /api/books/author/books/genres/add/ | [Add genre to book](#add-genre-to-book) | Yes |
| DELETE | /api/books/author/books/genres/remove/ | [Remove genre from book](#remove-genre-from-book) | Yes |
| POST | /api/books/author/books/relationship-tags/add/ | [Add relationship tag to book](#add-relationship-tag-to-book) | Yes |
| DELETE | /api/books/author/books/relationship-tags/remove/ | [Remove relationship tag from book](#remove-relationship-tag-from-book) | Yes |
| POST | /api/books/author/books/keywords/add/ | [Add keyword to book](#add-keyword-to-book) | Yes |
| DELETE | /api/books/author/books/keywords/remove/ | [Remove keyword from book](#remove-keyword-from-book) | Yes |
| POST | /api/books/author/chapters/create/ | [Create chapter](#create-chapter) | Yes |
| GET | /api/books/author/chapters/ | [List my chapters](#list-my-chapters) | Yes |
| PATCH | /api/books/author/chapters/update/ | [Update chapter](#update-chapter) | Yes |
| POST | /api/books/author/chapters/publish/ | [Publish chapter](#publish-chapter) | Yes |
| POST | /api/books/author/chapters/unpublish/ | [Unpublish chapter](#unpublish-chapter) | Yes |
| DELETE | /api/books/author/chapters/delete/ | [Delete chapter](#delete-chapter) | Yes |
| POST | /api/books/author/pages/create-update/ | [Create or update book page](#create-or-update-book-page) | Yes |
| POST | /api/books/author/pages/publish/ | [Publish book page](#publish-book-page) | Yes |
| POST | /api/books/author/pages/unpublish/ | [Unpublish book page](#unpublish-book-page) | Yes |
| DELETE | /api/books/author/pages/delete/ | [Delete book page](#delete-book-page) | Yes |

> **Not yet built:** author preview/bypass endpoints for reading own paid chapters without affecting reader stats — in progress.

### Reader endpoints (`/api/books/reader/`)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | /api/books/reader/library/ | [My library](#my-library) | Yes |
| POST | /api/books/reader/library/ | [Add book to library](#add-book-to-library) | Yes |
| DELETE | /api/books/reader/library/<book_id>/ | [Remove book from library](#remove-book-from-library) | Yes |
| GET | /api/books/reader/chapters/<chapter_id>/read/ | [Read chapter](#read-chapter) | Yes |
| POST | /api/books/reader/chapters/<chapter_id>/unlock/ | [Unlock chapter](#unlock-chapter) | Yes |

> **Not yet built:** library detail view (single book within library context), reviews, comments, flagging. See Parking Lot below.

### Public endpoints (`/api/books/public/`)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | /api/books/public/featured/ | [Featured books and authors](#featured-books-and-authors) | No |
| GET | /api/books/public/books/ | [Browse all books](#browse-all-books) | No |
| GET | /api/books/public/books/<id>/ | [Book detail](#book-detail) | No |
| GET | /api/books/public/books/reference-data/ | Genres, keywords, relationship tags, content ratings for filter UIs | No |

---

## Endpoint Details

### List genres
#### Headers:
```
Authorization    Bearer <access_token>
```
#### Body:
```
None
```
#### Success response 200:
```json
{
    "count": 2,
    "genres": [
        {
            "id": 1,
            "name": "Romance",
            "is_active": true,
            "created_at": "2026-05-08T12:00:00Z"
        },
        {
            "id": 2,
            "name": "Romantasy",
            "is_active": true,
            "created_at": "2026-05-08T12:00:00Z"
        }
    ]
}
```
#### Query params (optional):
```
is_active    filter by active status: true, false
```
#### Notes:
- Admin access required
- Returns all genres ordered alphabetically by name

---

### Create genre
#### Headers:
```
Authorization    Bearer <access_token>
Content-Type     application/json
```
#### Body:
```json
{
    "name": "Romance"
}
```
#### Success response 201:
```json
{
    "message": "Genre \"Romance\" created successfully",
    "genre": {
        "id": 1,
        "name": "Romance",
        "is_active": true,
        "created_at": "2026-05-08T12:00:00Z"
    }
}
```
#### Error responses:
```json
403: {"error": "You do not have permission to perform this action"}
400: {"error": "name is required"}
400: {"error": "A genre with this name already exists"}
```
#### Notes:
- Admin access required
- Name is case-insensitive unique check

---

### Update genre
#### Headers:
```
Authorization    Bearer <access_token>
Content-Type     application/json
```
#### Body (all fields optional except genre_id):
```json
{
    "genre_id": 1,
    "name": "Romantasy",
    "is_active": true
}
```
#### Success response 200:
```json
{
    "message": "Genre \"Romantasy\" updated successfully",
    "genre": {
        "id": 1,
        "name": "Romantasy",
        "is_active": true,
        "created_at": "2026-05-08T12:00:00Z"
    }
}
```
#### Error responses:
```json
403: {"error": "You do not have permission to perform this action"}
400: {"error": "genre_id is required"}
400: {"error": "A genre with this name already exists"}
404: {"error": "Genre not found"}
```
#### Notes:
- Admin access required
- Use `is_active: false` to deactivate a genre — deactivated genres are not shown to authors when tagging books

---

### List content ratings
#### Headers:
```
Authorization    Bearer <access_token>
```
#### Body:
```
None
```
#### Success response 200:
```json
{
    "count": 1,
    "content_ratings": [
        {
            "id": 1,
            "code": "G",
            "name": "General",
            "description": "Suitable for all ages",
            "is_active": true
        }
    ]
}
```
#### Query params (optional):
```
is_active    filter by active status: true, false
```
#### Notes:
- Admin access required
- Returns all content ratings ordered by code

---

### Create content rating
#### Headers:
```
Authorization    Bearer <access_token>
Content-Type     application/json
```
#### Body:
```json
{
    "code": "G",
    "name": "General",
    "description": "Suitable for all ages"
}
```
#### Success response 201:
```json
{
    "message": "Content rating \"General\" created successfully",
    "content_rating": {
        "id": 1,
        "code": "G",
        "name": "General",
        "description": "Suitable for all ages",
        "is_active": true
    }
}
```
#### Error responses:
```json
403: {"error": "You do not have permission to perform this action"}
400: {"error": "code, name and description are required"}
400: {"error": "A content rating with this code already exists"}
```
#### Notes:
- Admin access required
- Code is automatically uppercased on save
- Code is case-insensitive unique check

---

### Update content rating
#### Headers:
```
Authorization    Bearer <access_token>
Content-Type     application/json
```
#### Body (all fields optional except rating_id):
```json
{
    "rating_id": 1,
    "code": "GA",
    "name": "General Audiences",
    "description": "Suitable for all ages",
    "is_active": true
}
```
#### Success response 200:
```json
{
    "message": "Content rating \"General Audiences\" updated successfully",
    "content_rating": {
        "id": 1,
        "code": "GA",
        "name": "General Audiences",
        "description": "Suitable for all ages",
        "is_active": true
    }
}
```
#### Error responses:
```json
403: {"error": "You do not have permission to perform this action"}
400: {"error": "rating_id is required"}
400: {"error": "A content rating with this code already exists"}
404: {"error": "Content rating not found"}
```
#### Notes:
- Admin access required
- Code is automatically uppercased on save

---

### List relationship tags
#### Headers:
```
Authorization    Bearer <access_token>
```
#### Body:
```
None
```
#### Success response 200:
```json
{
    "count": 1,
    "relationship_tags": [
        {
            "id": 1,
            "code": "FF",
            "name": "Female/Female",
            "is_active": true
        }
    ]
}
```
#### Query params (optional):
```
is_active    filter by active status: true, false
```
#### Notes:
- Admin access required
- Returns all relationship tags ordered by name

---

### Create relationship tag
#### Headers:
```
Authorization    Bearer <access_token>
Content-Type     application/json
```
#### Body:
```json
{
    "code": "FF",
    "name": "Female/Female"
}
```
#### Success response 201:
```json
{
    "message": "Relationship tag \"Female/Female\" created successfully",
    "relationship_tag": {
        "id": 1,
        "code": "FF",
        "name": "Female/Female",
        "is_active": true
    }
}
```
#### Error responses:
```json
403: {"error": "You do not have permission to perform this action"}
400: {"error": "code and name are required"}
400: {"error": "A relationship tag with this code already exists"}
```
#### Notes:
- Admin access required
- Code is automatically uppercased on save
- Code is case-insensitive unique check

---

### Update relationship tag
#### Headers:
```
Authorization    Bearer <access_token>
Content-Type     application/json
```
#### Body (all fields optional except tag_id):
```json
{
    "tag_id": 1,
    "code": "FF",
    "name": "Female/Female Romance",
    "is_active": true
}
```
#### Success response 201:
```json
{
    "message": "Relationship tag \"Female/Female Romance\" updated successfully",
    "relationship_tag": {
        "id": 1,
        "code": "FF",
        "name": "Female/Female Romance",
        "is_active": true
    }
}
```
#### Error responses:
```json
403: {"error": "You do not have permission to perform this action"}
400: {"error": "tag_id is required"}
400: {"error": "A relationship tag with this code already exists"}
404: {"error": "Relationship tag not found"}
```
#### Notes:
- Admin access required
- Code is automatically uppercased on save

---

### List keywords
#### Headers:
```
Authorization    Bearer <access_token>
```
#### Body:
```
None
```
#### Success response 200:
```json
{
    "count": 1,
    "keywords": [
        {
            "id": 1,
            "name": "Dragons",
            "is_active": true
        }
    ]
}
```
#### Query params (optional):
```
is_active    filter by active status: true, false
```
#### Notes:
- Admin access required
- Returns all keywords ordered alphabetically by name

---

### Create keyword
#### Headers:
```
Authorization    Bearer <access_token>
Content-Type     application/json
```
#### Body:
```json
{
    "name": "Dragons"
}
```
#### Success response 201:
```json
{
    "message": "Keyword \"Dragons\" created successfully",
    "keyword": {
        "id": 1,
        "name": "Dragons",
        "is_active": true
    }
}
```
#### Error responses:
```json
403: {"error": "You do not have permission to perform this action"}
400: {"error": "name is required"}
400: {"error": "A keyword with this name already exists"}
```
#### Notes:
- Admin access required
- Name is case-insensitive unique check

---

### Update keyword
#### Headers:
```
Authorization    Bearer <access_token>
Content-Type     application/json
```
#### Body (all fields optional except keyword_id):
```json
{
    "keyword_id": 1,
    "name": "Dragon Shifters",
    "is_active": true
}
```
#### Success response 200:
```json
{
    "message": "Keyword \"Dragon Shifters\" updated successfully",
    "keyword": {
        "id": 1,
        "name": "Dragon Shifters",
        "is_active": true
    }
}
```
#### Error responses:
```json
403: {"error": "You do not have permission to perform this action"}
400: {"error": "keyword_id is required"}
400: {"error": "A keyword with this name already exists"}
404: {"error": "Keyword not found"}
```
#### Notes:
- Admin access required
- Name is case-insensitive unique check

---

### Create book
#### Headers:
```
Authorization    Bearer <access_token>
Content-Type     multipart/form-data
```
#### Body (all fields optional except title):
```
title               book title
description         book description
cover_image         <image file>
content_rating_id   id of content rating
free_chapters       number of free chapters (default 3)
author_type         paid or free (required if user has both profiles)
```
#### Success response 201:
```json
{
    "message": "Book \"My First Book\" created successfully",
    "book": {
        "id": 1,
        "title": "My First Book",
        "description": "A great story",
        "cover_image": "/media/bookCovers/paid/default.png",
        "content_rating": null,
        "book_tier": null,
        "status": "draft",
        "is_visible": true,
        "is_featured": false,
        "is_new": true,
        "is_complete": false,
        "free_chapters": 3,
        "has_pending_changes": false,
        "genres": [],
        "relationship_tags": [],
        "keywords": [],
        "pages": [],
        "chapters": [],
        "chapter_count": 0,
        "published_chapter_count": 0,
        "created_at": "2026-05-08T12:00:00Z",
        "updated_at": "2026-05-08T12:00:00Z"
    }
}
```
#### Error responses:
```json
403: {"error": "You must be an author to perform this action"}
400: {"error": "title is required"}
400: {"error": "free_chapters must be a number"}
400: {"error": "author_type is required when you have both paid and free author profiles. Must be paid or free."}
404: {"error": "Content rating not found"}
```
#### Notes:
- User must have an author or free_author profile
- `author_type` is optional if user only has one profile type
- `author_type` is required if user has both paid and free author profiles
- Paid author books default to `status: draft` and require approval before publishing chapters
- Free author books default to `status: approved` and can publish chapters immediately
- Cover image defaults to `bookCovers/paid/default.png` or `bookCovers/free/default.png` based on author type
- Body must be multipart/form-data to support image uploads

---

### List my books
#### Headers:
```
Authorization    Bearer <access_token>
```
#### Body:
```
None
```
#### Success response 200:
```json
{
    "count": 1,
    "books": [
        {
            "id": 1,
            "title": "My First Book",
            "description": "A great story",
            "cover_image": "/media/bookCovers/paid/default.png",
            "content_rating": null,
            "book_tier": null,
            "status": "draft",
            "is_visible": true,
            "is_featured": false,
            "is_new": true,
            "is_complete": false,
            "free_chapters": 3,
            "has_pending_changes": false,
            "genres": [],
            "relationship_tags": [],
            "keywords": [],
            "pages": [],
            "chapters": [],
            "chapter_count": 0,
            "published_chapter_count": 0,
            "created_at": "2026-05-08T12:00:00Z",
            "updated_at": "2026-05-08T12:00:00Z"
        }
    ]
}
```
#### Query params (optional):
```
status         filter by status: draft, pending_approval, approved, changes_requested, rejected
author_type    paid or free (required if user has both profiles)
```
#### Notes:
- User must have an author or free_author profile
- Returns books ordered by most recently created
- `author_type` is optional if user only has one profile type

---

### Get book detail (manage view)
#### Headers:
```
Authorization    Bearer <access_token>
```
#### Body:
```
None
```
#### Success response 200:
```json
{
    "id": 1,
    "title": "My First Book",
    "description": "A great story",
    "cover_image": "/media/bookCovers/paid/default.png",
    "content_rating": null,
    "book_tier": null,
    "status": "draft",
    "is_visible": true,
    "is_featured": false,
    "is_new": true,
    "is_complete": false,
    "free_chapters": 3,
    "has_pending_changes": false,
    "genres": [],
    "relationship_tags": [],
    "keywords": [],
    "pages": [],
    "chapters": [],
    "chapter_count": 0,
    "published_chapter_count": 0,
    "created_at": "2026-05-08T12:00:00Z",
    "updated_at": "2026-05-08T12:00:00Z"
}
```
#### Error responses:
```json
403: {"error": "You must be an author to perform this action"}
404: {"error": "Book not found"}
```
#### Notes:
- Same shape as a single item from [List my books](#list-my-books)
- Ownership-checked — only the owning author can fetch this
- Backs the frontend manage-book page (add chapter, add page, edit details actions)

---

### Update book
#### Headers:
```
Authorization    Bearer <access_token>
Content-Type     multipart/form-data
```
#### Body (all fields optional except book_id):
```
book_id             id of book to update
title               new title
description         new description
cover_image         <image file>
content_rating_id   id of content rating
free_chapters       new number of free chapters
author_type         paid or free (required if user has both profiles)
```
#### Success response 200:
```json
{
    "message": "Book \"Updated Title\" updated successfully",
    "book": {...}
}
```
#### Error responses:
```json
403: {"error": "You must be an author to perform this action"}
400: {"error": "book_id is required"}
400: {"error": "Rejected books cannot be edited"}
400: {"error": "free_chapters must be a number"}
400: {"error": "author_type is required when you have both paid and free author profiles. Must be paid or free."}
404: {"error": "Book not found"}
404: {"error": "Content rating not found"}
```
#### Notes:
- Uses PATCH not PUT — only send fields you want to change
- Body must be multipart/form-data to support image uploads
- Rejected books cannot be edited
- If book is `pending_approval` and is edited, `has_pending_changes` is set to True to alert admin

---

### Submit book for approval
#### Headers:
```
Authorization    Bearer <access_token>
Content-Type     application/json
```
#### Body:
```json
{
    "book_id": 1,
    "author_type": "paid"
}
```
#### Success response 200:
```json
{
    "message": "Book \"My First Book\" submitted for approval successfully",
    "book": {...}
}
```
#### Error responses:
```json
403: {"error": "Only paid authors can submit books for approval"}
400: {"error": "book_id is required"}
400: {"error": "Books with status \"approved\" cannot be submitted for approval"}
400: {"error": "author_type is required when you have both paid and free author profiles. Must be paid or free."}
404: {"error": "Book not found"}
```
#### Notes:
- Only paid authors can submit books for approval
- Free author books are automatically approved on creation
- Only books with status `draft` or `changes_requested` can be submitted
- Sets `submitted_at` timestamp and clears `has_pending_changes` on submission

---

### Delete book
#### Headers:
```
Authorization    Bearer <access_token>
Content-Type     application/json
```
#### Body:
```json
{
    "book_id": 1,
    "author_type": "paid"
}
```
#### Success response 200:
```json
{
    "message": "Book \"My First Book\" deleted successfully"
}
```
#### Error responses:
```json
403: {"error": "You must be an author to perform this action"}
400: {"error": "book_id is required"}
400: {"error": "Books with published chapters cannot be deleted"}
400: {"error": "author_type is required when you have both paid and free author profiles. Must be paid or free."}
404: {"error": "Book not found"}
```
#### Notes:
- Books with published chapters cannot be deleted
- All draft chapters, pages, genres, tags and keywords are deleted with the book

---

### Add genre to book
#### Headers:
```
Authorization    Bearer <access_token>
Content-Type     application/json
```
#### Body:
```json
{
    "book_id": 1,
    "genre_id": 1,
    "author_type": "paid"
}
```
#### Success response 200:
```json
{
    "message": "Genre \"Romance\" added to \"My First Book\" successfully",
    "book": {...}
}
```
#### Error responses:
```json
403: {"error": "You must be an author to perform this action"}
400: {"error": "book_id and genre_id are required"}
400: {"error": "This genre is already added to the book"}
400: {"error": "author_type is required when you have both paid and free author profiles. Must be paid or free."}
404: {"error": "Book not found"}
404: {"error": "Genre not found"}
```
#### Notes:
- Genre must be active to be added
- A book can have multiple genres

---

### Remove genre from book
#### Headers:
```
Authorization    Bearer <access_token>
Content-Type     application/json
```
#### Body:
```json
{
    "book_id": 1,
    "genre_id": 1,
    "author_type": "paid"
}
```
#### Success response 200:
```json
{
    "message": "Genre removed successfully",
    "book": {...}
}
```
#### Error responses:
```json
403: {"error": "You must be an author to perform this action"}
400: {"error": "book_id and genre_id are required"}
400: {"error": "author_type is required when you have both paid and free author profiles. Must be paid or free."}
404: {"error": "Book not found"}
404: {"error": "Genre not found on this book"}
```

---

### Add relationship tag to book
#### Headers:
```
Authorization    Bearer <access_token>
Content-Type     application/json
```
#### Body:
```json
{
    "book_id": 1,
    "tag_id": 1,
    "author_type": "paid"
}
```
#### Success response 200:
```json
{
    "message": "Tag \"Female/Female\" added to \"My First Book\" successfully",
    "book": {...}
}
```
#### Error responses:
```json
403: {"error": "You must be an author to perform this action"}
400: {"error": "book_id and tag_id are required"}
400: {"error": "This tag is already added to the book"}
400: {"error": "author_type is required when you have both paid and free author profiles. Must be paid or free."}
404: {"error": "Book not found"}
404: {"error": "Relationship tag not found"}
```
#### Notes:
- Tag must be active to be added
- A book can have multiple relationship tags

---

### Remove relationship tag from book
#### Headers:
```
Authorization    Bearer <access_token>
Content-Type     application/json
```
#### Body:
```json
{
    "book_id": 1,
    "tag_id": 1,
    "author_type": "paid"
}
```
#### Success response 200:
```json
{
    "message": "Tag removed successfully",
    "book": {...}
}
```
#### Error responses:
```json
403: {"error": "You must be an author to perform this action"}
400: {"error": "book_id and tag_id are required"}
400: {"error": "author_type is required when you have both paid and free author profiles. Must be paid or free."}
404: {"error": "Book not found"}
404: {"error": "Tag not found on this book"}
```

---

### Add keyword to book
#### Headers:
```
Authorization    Bearer <access_token>
Content-Type     application/json
```
#### Body:
```json
{
    "book_id": 1,
    "keyword_id": 1,
    "author_type": "paid"
}
```
#### Success response 200:
```json
{
    "message": "Keyword \"Dragons\" added to \"My First Book\" successfully",
    "book": {...}
}
```
#### Error responses:
```json
403: {"error": "You must be an author to perform this action"}
400: {"error": "book_id and keyword_id are required"}
400: {"error": "This keyword is already added to the book"}
400: {"error": "author_type is required when you have both paid and free author profiles. Must be paid or free."}
404: {"error": "Book not found"}
404: {"error": "Keyword not found"}
```
#### Notes:
- Keyword must be active to be added
- A book can have multiple keywords

---

### Remove keyword from book
#### Headers:
```
Authorization    Bearer <access_token>
Content-Type     application/json
```
#### Body:
```json
{
    "book_id": 1,
    "keyword_id": 1,
    "author_type": "paid"
}
```
#### Success response 200:
```json
{
    "message": "Keyword removed successfully",
    "book": {...}
}
```
#### Error responses:
```json
403: {"error": "You must be an author to perform this action"}
400: {"error": "book_id and keyword_id are required"}
400: {"error": "author_type is required when you have both paid and free author profiles. Must be paid or free."}
404: {"error": "Book not found"}
404: {"error": "Keyword not found on this book"}
```

---

### Create chapter
#### Headers:
```
Authorization    Bearer <access_token>
Content-Type     application/json
```
#### Body:
```json
{
    "book_id": 1,
    "content": "Chapter content goes here.",
    "title": "The Beginning",
    "is_final": false,
    "author_type": "paid"
}
```
#### Success response 201:
```json
{
    "message": "Chapter 1 created successfully",
    "chapter": {
        "id": 1,
        "chapter_number": 1,
        "title": "The Beginning",
        "display_title": "Chapter 1: The Beginning",
        "content": "Chapter content goes here.",
        "status": "draft",
        "is_free": false,
        "is_new": true,
        "is_final": false,
        "word_count": 4,
        "unlock_cost": 0,
        "published_at": null,
        "created_at": "2026-05-08T12:00:00Z",
        "updated_at": "2026-05-08T12:00:00Z"
    }
}
```
#### Error responses:
```json
403: {"error": "You must be an author to perform this action"}
400: {"error": "book_id is required"}
400: {"error": "content is required"}
400: {"error": "Book must be submitted for approval before adding chapters"}
400: {"error": "Cannot add chapters to a completed book"}
400: {"error": "author_type is required when you have both paid and free author profiles. Must be paid or free."}
404: {"error": "Book not found"}
```
#### Notes:
- `chapter_number` is auto-incremented — authors never set it manually
- `word_count` is auto-calculated from content on save
- `title` is optional — display will show "Chapter N" if no title set
- `display_title` combines chapter number and title for frontend display
- `is_free` is auto-set based on chapter number vs book's `free_chapters` setting
- Free author chapters are always `is_free: true`
- Paid author books must be at least submitted for approval before chapters can be added
- Setting `is_final: true` will mark the book as complete — this is permanent

---

### List my chapters
#### Headers:
```
Authorization    Bearer <access_token>
```
#### Success response 200:
```json
{
    "count": 2,
    "chapters": [
        {
            "id": 1,
            "chapter_number": 1,
            "title": "The Beginning",
            "display_title": "Chapter 1: The Beginning",
            "content": "Chapter content goes here.",
            "status": "draft",
            "is_free": true,
            "is_new": true,
            "is_final": false,
            "word_count": 4,
            "unlock_cost": 0,
            "published_at": null,
            "created_at": "2026-05-08T12:00:00Z",
            "updated_at": "2026-05-08T12:00:00Z"
        },
        {
            "id": 2,
            "chapter_number": 2,
            "title": null,
            "display_title": "Chapter 2",
            "content": "Chapter two content.",
            "status": "draft",
            "is_free": true,
            "is_new": true,
            "is_final": false,
            "word_count": 3,
            "unlock_cost": 0,
            "published_at": null,
            "created_at": "2026-05-08T12:00:00Z",
            "updated_at": "2026-05-08T12:00:00Z"
        }
    ]
}
```
#### Query params:
```
book_id      required — id of the book
status       optional — filter by status: draft, published
author_type  optional — paid or free (required if user has both profiles)
```
#### Notes:
- `book_id` is required
- Returns chapters ordered by chapter number
- Author can see all chapters including drafts

---

### Update chapter
#### Headers:
```
Authorization    Bearer <access_token>
Content-Type     application/json
```
#### Body (all fields optional except chapter_id):
```json
{
    "chapter_id": 1,
    "title": "Updated Title",
    "content": "Updated content.",
    "is_final": false,
    "unlock_cost": 10,
    "author_type": "paid"
}
```
#### Success response 200:
```json
{
    "message": "Chapter 1 updated successfully",
    "chapter": {...}
}
```
#### Error responses:
```json
403: {"error": "You must be an author to perform this action"}
400: {"error": "chapter_id is required"}
400: {"error": "Cannot unmark final chapter once book is marked complete"}
400: {"error": "unlock_cost must be a number"}
400: {"error": "author_type is required when you have both paid and free author profiles. Must be paid or free."}
404: {"error": "Chapter not found"}
```
#### Notes:
- Uses PATCH not PUT — only send fields you want to change
- `word_count` recalculates automatically if content is updated
- `is_final` cannot be unset once book is marked complete
- Send empty string for `title` to clear it

---

### Publish chapter
#### Headers:
```
Authorization    Bearer <access_token>
Content-Type     application/json
```
#### Body:
```json
{
    "chapter_id": 1,
    "author_type": "paid"
}
```
#### Success response 200:
```json
{
    "message": "Chapter 1 published successfully",
    "chapter": {...}
}
```
#### Error responses:
```json
403: {"error": "You must be an author to perform this action"}
400: {"error": "chapter_id is required"}
400: {"error": "Book must be approved before publishing chapters"}
400: {"error": "Chapter is already published"}
400: {"error": "author_type is required when you have both paid and free author profiles. Must be paid or free."}
404: {"error": "Chapter not found"}
```
#### Notes:
- Book must be `approved` before any chapters can be published
- Sets `published_at` timestamp automatically via signal
- Sets `is_free` based on chapter number vs book's `free_chapters` setting via signal
- Sets `book.is_new` to True when first chapter is published via signal

---

### Unpublish chapter
#### Headers:
```
Authorization    Bearer <access_token>
Content-Type     application/json
```
#### Body:
```json
{
    "chapter_id": 1,
    "author_type": "paid"
}
```
#### Success response 200:
```json
{
    "message": "Chapter 1 unpublished successfully",
    "chapter": {...}
}
```
#### Error responses:
```json
403: {"error": "You must be an author to perform this action"}
400: {"error": "chapter_id is required"}
400: {"error": "Chapter is already unpublished"}
400: {"error": "Cannot unpublish a chapter that has been unlocked by readers"}
400: {"error": "author_type is required when you have both paid and free author profiles. Must be paid or free."}
404: {"error": "Chapter not found"}
```
#### Notes:
- Cannot unpublish a chapter that has been unlocked by readers
- Clears `published_at` on unpublish

---

### Delete chapter
#### Headers:
```
Authorization    Bearer <access_token>
Content-Type     application/json
```
#### Body:
```json
{
    "chapter_id": 1,
    "author_type": "paid"
}
```
#### Success response 200:
```json
{
    "message": "Chapter 1 deleted successfully"
}
```
#### Error responses:
```json
403: {"error": "You must be an author to perform this action"}
400: {"error": "chapter_id is required"}
400: {"error": "Published chapters cannot be deleted"}
400: {"error": "author_type is required when you have both paid and free author profiles. Must be paid or free."}
404: {"error": "Chapter not found"}
```
#### Notes:
- Only draft chapters can be deleted
- Published chapters must be unpublished before they can be deleted

---

### List all books (admin)
#### Headers:
```
Authorization    Bearer <access_token>
```
#### Body:
```
None
```
#### Success response 200:
```json
{
    "count": 2,
    "books": [
        {
            "id": 1,
            "title": "My First Book",
            "description": "A great story",
            "cover_image": "/media/bookCovers/paid/default.png",
            "content_rating": null,
            "book_tier": null,
            "status": "pending_approval",
            "is_visible": true,
            "is_featured": false,
            "is_new": false,
            "is_complete": false,
            "free_chapters": 3,
            "has_pending_changes": false,
            "author_type": "paid",
            "author": {
                "id": 2,
                "pen_name": "Jane Doe",
                "author_username": "janedoe"
            },
            "genres": [],
            "relationship_tags": [],
            "keywords": [],
            "chapter_count": 0,
            "published_chapter_count": 0,
            "submitted_at": "2026-05-08T12:00:00Z",
            "created_at": "2026-05-08T12:00:00Z",
            "updated_at": "2026-05-08T12:00:00Z"
        }
    ]
}
```
#### Query params (optional):
```
status                 filter by status: draft, pending_approval, approved, changes_requested, rejected
author_type            filter by author type: paid, free
has_pending_changes    filter by pending changes flag: true, false
```
#### Notes:
- Admin access required
- Returns all books across all authors ordered by most recently updated
- Use `status=pending_approval` to see the approval queue

---

### Admin update book
#### Headers:
```
Authorization    Bearer <access_token>
Content-Type     application/json
```
#### Body (all fields optional except book_id):
```json
{
    "book_id": 1,
    "book_tier": 2,
    "is_visible": true,
    "is_featured": false,
    "admin_notes": "Internal note about this book",
    "reader_notes": "Note visible to the author"
}
```
#### Success response 200:
```json
{
    "message": "Book \"My First Book\" updated successfully",
    "book": {...}
}
```
#### Error responses:
```json
403: {"error": "You do not have permission to perform this action"}
400: {"error": "book_id is required"}
400: {"error": "book_tier must be a number"}
404: {"error": "Book not found"}
```
#### Notes:
- Admin access required
- Use `is_visible: false` to hide a book from new readers without deleting it — existing unlocked chapters remain accessible
- `is_featured` requires offline payment arrangement with author before setting
- `admin_notes` are internal only — not visible to the author
- `reader_notes` are visible to the author

---

### Approve book
#### Headers:
```
Authorization    Bearer <access_token>
Content-Type     application/json
```
#### Body:
```json
{
    "book_id": 1,
    "reader_notes": "Your book has been approved. You can now publish chapters."
}
```
#### Success response 200:
```json
{
    "message": "Book \"My First Book\" approved successfully",
    "book": {...}
}
```
#### Error responses:
```json
403: {"error": "You do not have permission to perform this action"}
400: {"error": "book_id is required"}
400: {"error": "reader_notes is required"}
400: {"error": "Only books with status \"pending_approval\" can be approved"}
404: {"error": "Book not found"}
```
#### Notes:
- Admin access required
- Only books with status `pending_approval` can be approved
- Sets status to `approved` — author can now publish chapters
- `reader_notes` is required — author receives this message

---

### Request book changes
#### Headers:
```
Authorization    Bearer <access_token>
Content-Type     application/json
```
#### Body:
```json
{
    "book_id": 1,
    "reader_notes": "Please update the book description before we can approve.",
    "admin_notes": "Description too short, cover image low quality"
}
```
#### Success response 200:
```json
{
    "message": "Changes requested for book \"My First Book\"",
    "book": {...}
}
```
#### Error responses:
```json
403: {"error": "You do not have permission to perform this action"}
400: {"error": "book_id is required"}
400: {"error": "reader_notes is required"}
400: {"error": "Only books with status \"pending_approval\" can have changes requested"}
404: {"error": "Book not found"}
```
#### Notes:
- Admin access required
- Only books with status `pending_approval` can have changes requested
- Sets status to `changes_requested` — author must edit and resubmit
- `reader_notes` is required — author receives this message explaining what to fix
- `admin_notes` is optional — internal note for admin reference

---

### Reject book
#### Headers:
```
Authorization    Bearer <access_token>
Content-Type     application/json
```
#### Body:
```json
{
    "book_id": 1,
    "reader_notes": "Unfortunately your book does not meet our content guidelines.",
    "admin_notes": "Content violations found in chapters 2 and 3"
}
```
#### Success response 200:
```json
{
    "message": "Book \"My First Book\" rejected",
    "book": {...}
}
```
#### Error responses:
```json
403: {"error": "You do not have permission to perform this action"}
400: {"error": "book_id is required"}
400: {"error": "reader_notes is required"}
400: {"error": "Only books with status \"pending_approval\" can be rejected"}
404: {"error": "Book not found"}
```
#### Notes:
- Admin access required
- Only books with status `pending_approval` can be rejected
- Sets status to `rejected` — book cannot be edited or resubmitted
- `reader_notes` is required — author receives this message
- `admin_notes` is optional — internal note for admin reference

---

### Create or update book page
#### Headers:
```
Authorization    Bearer <access_token>
Content-Type     application/json
```
#### Body:
```json
{
    "book_id": 1,
    "page_type": "prologue",
    "content": "Page content goes here."
}
```
#### Success response 200/201:
```json
{
    "message": "Prologue saved successfully",
    "page": {
        "id": 1,
        "page_type": "prologue",
        "content": "Page content goes here.",
        "is_published": false,
        "created_at": "2026-05-08T12:00:00Z",
        "updated_at": "2026-05-08T12:00:00Z"
    }
}
```
#### Error responses:
```json
403: {"error": "You must be an author to perform this action"}
400: {"error": "book_id, page_type and content are required"}
400: {"error": "Invalid page_type. Must be one of: prologue, authors_note, dedication, acknowledgements, next_book_teaser"}
404: {"error": "Book not found"}
```
#### Notes:
- This endpoint creates or updates — if a page of this type already exists for the book it will be overwritten
- Valid page types: `prologue`, `authors_note`, `dedication`, `acknowledgements`, `next_book_teaser`
- Each book can have at most one of each page type
- Returns 201 on create, 200 on update

---

### Publish book page
#### Headers:
```
Authorization    Bearer <access_token>
Content-Type     application/json
```
#### Body:
```json
{
    "book_id": 1,
    "page_type": "prologue"
}
```
#### Success response 200:
```json
{
    "message": "Prologue published successfully",
    "page": {...}
}
```
#### Error responses:
```json
403: {"error": "You must be an author to perform this action"}
400: {"error": "book_id and page_type are required"}
400: {"error": "Page is already published"}
404: {"error": "Book not found"}
404: {"error": "Page not found"}
```
#### Notes:
- Can be published regardless of book approval status
- Pages will only be visible to readers once the book itself is approved and has published chapters

---

### Unpublish book page
#### Headers:
```
Authorization    Bearer <access_token>
Content-Type     application/json
```
#### Body:
```json
{
    "book_id": 1,
    "page_type": "prologue"
}
```
#### Success response 200:
```json
{
    "message": "Prologue unpublished successfully",
    "page": {...}
}
```
#### Error responses:
```json
403: {"error": "You must be an author to perform this action"}
400: {"error": "book_id and page_type are required"}
400: {"error": "Page is already unpublished"}
404: {"error": "Book not found"}
404: {"error": "Page not found"}
```

---

### Delete book page
#### Headers:
```
Authorization    Bearer <access_token>
Content-Type     application/json
```
#### Body:
```json
{
    "book_id": 1,
    "page_type": "prologue"
}
```
#### Success response 200:
```json
{
    "message": "Prologue deleted successfully"
}
```
#### Error responses:
```json
403: {"error": "You must be an author to perform this action"}
400: {"error": "book_id and page_type are required"}
404: {"error": "Book not found"}
404: {"error": "Page not found"}
```
#### Notes:
- Deletes the page entirely — use unpublish if you just want to hide it from readers

---

### My library
#### Headers:
```
Authorization    Bearer <access_token>
```
#### Body:
```
None
```
#### Success response 200:
```json
[
    {
        "id": 1,
        "book": {
            "id": 1,
            "title": "My First Book",
            "cover_image": "/media/bookCovers/paid/default.png",
            "author": {
                "author_username": "janedoe",
                "pen_name": "Jane Doe",
                "avatar_url": "https://api.noveleshelf.com/media/avatars/author/default.png"
            },
            "genre_list": ["Romance"],
            "is_complete": false,
            "book_tier": 1
        },
        "completion_percentage": "0.00",
        "is_completed": false,
        "started_at": "2026-06-08T12:00:00Z",
        "completed_at": null,
        "last_read_at": null
    }
]
```
#### Notes:
- Returns book card info inline — no second call needed to render the shelf
- Ordered by most recently read, then most recently added

---

### Add book to library
#### Headers:
```
Authorization    Bearer <access_token>
Content-Type     application/json
```
#### Body:
```json
{
    "book_id": 1
}
```
#### Success response 201 (created) or 200 (already in library):
```json
{
    "id": 1,
    "book": {...},
    "completion_percentage": "0.00",
    "is_completed": false,
    "started_at": "2026-06-08T12:00:00Z",
    "completed_at": null,
    "last_read_at": null
}
```
#### Error responses:
```json
400: {"detail": "book_id is required."}
404: Book not found / not visible / not approved
```
#### Notes:
- Book must be `status=approved` and `is_visible=True`
- Adding a book already in the library returns 200, not an error

---

### Remove book from library
#### Headers:
```
Authorization    Bearer <access_token>
```
#### Body:
```
None
```
#### Success response 204:
```
No content
```
#### Notes:
- Removes the `UserBook` record entirely — does not affect chapter unlocks or reading progress

---

### Read chapter
#### Headers:
```
Authorization    Bearer <access_token>
```
#### Body:
```
None
```
#### Success response 200 (accessible):
```json
{
    "id": 1,
    "chapter_number": 1,
    "title": "The Beginning",
    "content": "Full chapter text...",
    "word_count": 1250,
    "is_free": true,
    "unlock_cost": 0,
    "is_final": false,
    "book_title": "My First Book",
    "total_chapters": 5,
    "published_at": "2026-05-08T12:00:00Z"
}
```
#### Locked response 402 (needs unlock):
```json
{
    "locked": true,
    "chapter": {
        "id": 2,
        "chapter_number": 2,
        "title": "The Middle",
        "unlock_cost": 10,
        "book_title": "My First Book",
        "word_count": 1400
    },
    "wallet": {
        "quill_balance": 0,
        "gold_ink_balance": 0,
        "black_ink_balance": 8
    }
}
```
#### Notes:
- Free chapters auto-create a `UserReadingProgress` record and auto-add the book to the reader's library on first read
- Already-unlocked chapters return content directly and mark `is_read`
- Locked chapters never return content — frontend must call unlock first

---

### Unlock chapter
#### Headers:
```
Authorization    Bearer <access_token>
```
#### Body:
```
None
```
#### Success response 200:
```json
{
    "detail": "Chapter unlocked.",
    "used": {
        "black_ink": 8,
        "gold_ink": 0,
        "quills": 2
    },
    "wallet": {
        "quill_balance": 0,
        "gold_ink_balance": 0,
        "black_ink_balance": 0
    }
}
```
#### Error response 402 (insufficient funds):
```json
{
    "detail": "Insufficient funds.",
    "wallet": {
        "quill_balance": 0,
        "gold_ink_balance": 0,
        "black_ink_balance": 8
    },
    "cost": 10
}
```
#### Notes:
- Spend order is always black_ink → gold_ink → quills
- Writes one `Transaction` record per currency type actually used
- Auto-adds the book to the reader's library if not already there
- Already-unlocked chapters return 200 with a message, no double charge
- Free chapters return 400 — use the read endpoint directly, no unlock needed

---

### Featured books and authors
#### Headers:
```
None
```
#### Body:
```
None
```
#### Success response 200:
```json
{
    "featured_books": [
        {
            "id": 1,
            "title": "My First Book",
            "cover_image": "bookCovers/paid/default.png",
            "description": "A great story about...",
            "description_truncated": true,
            "content_rating": {
                "code": "G",
                "name": "General"
            },
            "book_tier": 1,
            "is_complete": false,
            "is_new": true,
            "is_featured": true,
            "chapter_count": 5,
            "published_chapter_count": 3,
            "genres": [
                {"id": 1, "name": "Romance"}
            ],
            "relationship_tags": [
                {"id": 1, "code": "FF", "name": "Female/Female"}
            ],
            "keywords": [
                {"id": 1, "name": "Dragons"}
            ],
            "author": {
                "display_name": "Jane Doe",
                "username": "janedoe",
                "avatar_url": "avatars/author/default.png",
                "is_featured": true,
                "author_type": "paid"
            }
        }
    ],
    "featured_authors": [
        {
            "display_name": "Jane Doe",
            "username": "janedoe",
            "avatar_url": "avatars/author/default.png",
            "bio": "Author bio here",
            "is_featured": true,
            "is_new": false,
            "author_type": "paid",
            "book_count": 3
        }
    ]
}
```
#### Notes:
- No auth required
- Returns up to 6 featured books and up to 4 featured authors
- Featured books ordered by most recently updated
- Author display name follows: `show_real_name` → `pen_name` → `author_username` → `email`
- Both paid and free authors can appear in featured authors
- Only `is_publicly_visible=True` authors appear in featured authors

---

### Browse all books
#### Headers:
```
None
```
#### Body:
```
None
```
#### Success response 200:
```json
{
    "count": 24,
    "page": 1,
    "page_size": 12,
    "total_pages": 2,
    "results": [
        {
            "id": 1,
            "title": "My First Book",
            "cover_image": "bookCovers/paid/default.png",
            "description": "A great story about...",
            "description_truncated": true,
            "content_rating": {
                "code": "G",
                "name": "General"
            },
            "book_tier": 1,
            "is_complete": false,
            "is_new": true,
            "is_featured": false,
            "chapter_count": 5,
            "published_chapter_count": 3,
            "genres": [],
            "relationship_tags": [],
            "keywords": [],
            "author": {
                "display_name": "Jane Doe",
                "username": "janedoe",
                "avatar_url": "avatars/author/default.png",
                "is_featured": false,
                "author_type": "paid"
            }
        }
    ]
}
```
#### Query params (optional):
```
search              search title, author name, genre, keyword, relationship tag
genre               filter by genre id
relationship_tag    filter by relationship tag id
keyword             filter by keyword id
content_rating      filter by content rating id
is_featured         filter by featured status: true, false
is_new              filter by new status: true, false
is_complete         filter by completion status: true, false
page                page number (default 1)
page_size           results per page (default 12, max 50)
```
#### Notes:
- No auth required
- Only returns books with `status=approved` and `is_visible=True`
- Description truncated to 150 characters — check `description_truncated` flag
- Results ordered by most recently created
- Both paid and free author books appear together

---

### Book detail
#### Headers:
```
None
```
#### Body:
```
None
```
#### Success response 200:
```json
{
    "id": 1,
    "title": "My First Book",
    "cover_image": "bookCovers/paid/default.png",
    "description": "Full description here, not truncated.",
    "description_truncated": false,
    "content_rating": {
        "code": "G",
        "name": "General"
    },
    "book_tier": 1,
    "is_complete": false,
    "is_new": true,
    "is_featured": false,
    "chapter_count": 5,
    "published_chapter_count": 3,
    "genres": [
        {"id": 1, "name": "Romance"}
    ],
    "relationship_tags": [
        {"id": 1, "code": "FF", "name": "Female/Female"}
    ],
    "keywords": [
        {"id": 1, "name": "Dragons"}
    ],
    "author": {
        "display_name": "Jane Doe",
        "username": "janedoe",
        "avatar_url": "avatars/author/default.png",
        "is_featured": false,
        "author_type": "paid"
    },
    "pages": [
        {
            "id": 1,
            "page_type": "prologue",
            "content": "Prologue content here."
        }
    ],
    "chapters": [
        {
            "id": 1,
            "chapter_number": 1,
            "title": "The Beginning",
            "display_title": "Chapter 1: The Beginning",
            "is_free": true,
            "is_new": true,
            "is_final": false,
            "word_count": 1250,
            "unlock_cost": 0,
            "published_at": "2026-05-08T12:00:00Z"
        }
    ]
}
```
#### Error responses:
```json
404: {"error": "Book not found"}
```
#### Notes:
- No auth required
- Returns full description — not truncated
- Only published pages are included
- Only published chapters are included — no content, just metadata for the chapter list
- Chapter list ordered by chapter number

---

## Parking Lot

> Things known to be missing or not yet decided — not blockers for current testing, but worth tracking.

- **Reviews, comments, flagging** — not built anywhere (model exists, no views/urls). Pulled from this README until implemented.
- **Library detail view** — single book within library context (vs. flat list) not yet built.
- **Author preview / bypass** — authors reading their own paid chapters without affecting reader stats. In progress.
- **Page + chapter ordering** — `BookPage.page_type` and `Chapter.chapter_number` aren't merged into one reading-order sequence yet. Planned as a fixed positional rule by `page_type` (no migration), not a free-form `order` field.
- **Reading progress completion %** — `UserBook.completion_percentage` is not yet updated automatically as chapters are read.
- **Convert free book to paid** — when a free author upgrades to paid author and wants to convert an existing free book: chapters with existing unlocks (always `unlock_currency_type: 'free'`) must stay accessible to readers who already unlocked them; only chapters with no unlocks can switch to paid; new chapters going forward are paid. Not designed in detail or built yet.
- **Book tier snapshot** — `Book.book_tier` is meant to snapshot the author's tier at the time of book creation, so that if the author's tier changes later, existing books keep their original tier rate and only new books get the new rate. Confirm this snapshot behavior is actually implemented in `create_book` before relying on it.

---

[← Back to Server README](../readme.md)