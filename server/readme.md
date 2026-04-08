This is the main app/website backend. 

To start it will not include the contact form but may incorperate it at a later date

EndPoints:

| Method | Endpoint           | Description  | Auth Required |
|--------|--------------------|--------------|---------------|
| GET    | /api/health        | check status | No            |
| GET    | /admin             | Django admin | Yes           |
| POST   | /api/auth/register | Create User  | No            |
| POST   | /api/auth/login    | Login        | No            |
