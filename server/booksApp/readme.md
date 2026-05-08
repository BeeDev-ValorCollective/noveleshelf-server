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
| POST | /api/books/admin/books/reject/ | Reject book | Yes |
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
| DELETE | /api/books/author/books/delete/ | Delete book | Yes |
| POST | /api/books/author/books/genres/add/ | Add genre | Yes |
| DELETE | /api/books/author/books/genres/remove/ | Delete genre | Yes |
| POST | /api/books/author/books/relationship-tags/add/ | Add Tag | Yes |
| DELETE | /api/books/author/books/relationship-tags/remove/ | Delete tag | Yes |
| POST | /api/books/author/books/keywords/add/ | Add Keyword | Yes |
| DELETE | /api/books/author/books/keywords/remove/ | Delete Keyword | Yes |
| POST | /api/books/author/chapters/create/ | Create chapter | Yes |
| GET | /api/books/author/chapters/ | List my chapters | Yes |
| PATCH | /api/books/author/chapters/update/ | Update chapter | Yes |
| POST | /api/books/author/chapters/publish/ | Publish chapter | Yes |
| POST | /api/books/author/chapters/unpublish/ | Unpublish chapter | Yes |
| DELETE | /api/books/author/chapters/delete/ | Delete chapter | Yes |
| POST | /api/books/author/pages/create-update/ | Create or update book page | Yes |
| POST | /api/books/author/pages/publish/ | Publish book page | Yes |
| POST | /api/books/author/pages/unpublish/ | Unpublish book page | Yes |

### Reader endpoints (`/api/books/user/`)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | /api/books/user/books/ | List all visible books | Yes |
| GET | /api/books/user/books/<id>/ | Get book details | Yes |
| GET | /api/books/user/search/ | Search books | Yes |
| GET | /api/books/user/chapters/<id>/ | Get chapter content | Yes |
| POST | /api/books/user/chapters/unlock/ | Unlock chapter | Yes |
| GET | /api/books/user/library/ | My library | Yes |
| GET | /api/books/user/progress/<book_id>/ | Reading progress for book | Yes |
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
#### Success response 200:
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

## Notes for developers

See [DEVELOPER_NOTES.md](DEVELOPER_NOTES.md) for full details on:
- Model descriptions and business rules
- View specifications
- TODO items
- Frontend notes

---

[← Back to Server README](../README.md)