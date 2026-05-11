# Novel eShelf — booksApp

Handles all book, chapter, genre, and reading progress functionality.

---

[← Back to Server README](../README.md)

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
|||||
| GET | /api/books/admin/books/ | List all books | Yes |
| PATCH | /api/books/admin/books/update/ | Update book | Yes |
| POST | /api/books/admin/books/approve/ | Approve book | Yes |
| POST | /api/books/admin/books/request-changes/ | Request book changes | Yes |
| POST | /api/books/admin/books/reject/ | Reject book | Yes |
|||||
| GET | /api/books/admin/flagged/reviews/ | List flagged reviews | Yes |
| GET | /api/books/admin/flagged/comments/ | List flagged comments | Yes |
| DELETE | /api/books/admin/reviews/delete/ | Delete review | Yes |
| DELETE | /api/books/admin/comments/delete/ | Delete comment | Yes |

### Author endpoints (`/api/books/author/`)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | /api/books/author/books/create/ | [Create book](#create-book) | Yes |
| GET | /api/books/author/books/ | [List my books](#list-my-books) | Yes |
| PATCH | /api/books/author/books/update/ | [Update book](#update-book) | Yes |
| POST | /api/books/author/books/submit/ | [Submit book for approval](#submit-book-for-approval) | Yes |
| DELETE | /api/books/author/books/delete/ | [Delete book](#delete-book) | Yes |
| POST | /api/books/author/books/genres/add/ | [Add genre to book](#add-genre-to-book) | Yes |
| DELETE | /api/books/author/books/genres/remove/ | [Remove genre from book](#remove-genre-from-book) | Yes |
| POST | /api/books/author/books/relationship-tags/add/ | [Add relationship tag to book](#add-relationship-tag-to-book) | Yes |
| DELETE | /api/books/author/books/relationship-tags/remove/ | [Remove relationship tag from book](#remove-relationship-tag-from-book) | Yes |
| POST | /api/books/author/books/keywords/add/ | [Add keyword to book](#add-keyword-to-book) | Yes |
| DELETE | /api/books/author/books/keywords/remove/ | [Remove keyword from book](#remove-keyword-from-book) | Yes |
|||||
| POST | /api/books/author/chapters/create/ | [Create chapter](#create-chapter) | Yes |
| GET | /api/books/author/chapters/ | [List my chapters](#list-my-chapters) | Yes |
| PATCH | /api/books/author/chapters/update/ | [Update chapter](#update-chapter) | Yes |
| POST | /api/books/author/chapters/publish/ | [Publish chapter](#publish-chapter) | Yes |
| POST | /api/books/author/chapters/unpublish/ | [Unpublish chapter](#unpublish-chapter) | Yes |
| DELETE | /api/books/author/chapters/delete/ | [Delete chapter](#delete-chapter) | Yes |
|||||
| POST | /api/books/author/pages/create-update/ | Create or update book page | Yes |
| POST | /api/books/author/pages/publish/ | Publish book page | Yes |
| POST | /api/books/author/pages/unpublish/ | Unpublish book page | Yes |

### User endpoints (`/api/books/user/`)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | /api/books/user/books/ | List all visible books | Yes |
| GET | /api/books/user/books/<id>/ | Get book details | Yes |
| GET | /api/books/user/search/ | Search books | Yes |
| GET | /api/books/user/chapters/<id>/ | Get chapter content | Yes |
| POST | /api/books/user/chapters/unlock/ | Unlock chapter | Yes |
| GET | /api/books/user/library/ | My library | Yes |
| GET | /api/books/user/progress/<book_id>/ | Reading progress for book | Yes |
|||||
| POST | /api/books/user/reviews/create/ | Create review | Yes |
| PATCH | /api/books/user/reviews/update/ | Update review | Yes |
| GET | /api/books/user/reviews/<book_id>/ | List book reviews | Yes |
| POST | /api/books/user/comments/create/ | Create comment | Yes |
| GET | /api/books/user/comments/<chapter_id>/ | List chapter comments | Yes |
| POST | /api/books/user/reviews/flag/ | Flag review | Yes |
| POST | /api/books/user/comments/flag/ | Flag comment | Yes |

### Public endpoints (`/api/books/public/`)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | /api/books/public/books/ | List all visible books | No |
| GET | /api/books/public/books/<id>/ | Get book details | No |

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

## Notes for developers

See [DEVELOPER_NOTES.md](DEVELOPER_NOTES.md) for full details on:
- Model descriptions and business rules
- View specifications
- TODO items
- Frontend notes

---

[← Back to Server README](../README.md)