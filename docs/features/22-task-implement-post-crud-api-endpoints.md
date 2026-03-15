## What it does
Implements full CRUD REST API endpoints for blog posts, including public (GET) and protected (POST, PUT, DELETE, admin GET) routes. Enforces authentication for mutating and admin endpoints, supports pagination for published posts, and returns proper HTTP status codes for all operations.

## How to use it
- `GET /api/posts?page=1` — Returns paginated list of published posts (10 per page)
- `GET /api/posts/{id}` — Returns a single published post by ID
- `POST /api/posts` — Creates a new post (requires Bearer token)
- `PUT /api/posts/{id}` — Updates a post (requires Bearer token)
- `DELETE /api/posts/{id}` — Deletes a post (requires Bearer token)
- `GET /api/admin/posts` — Returns all posts, including drafts (requires Bearer token)

Authentication: For protected routes, include `Authorization: Bearer <token>` header (any non-empty token is accepted for testing).

## Internals
- main.py: Adds all post CRUD API endpoints, enforces authentication for protected/admin routes, implements pagination, and returns correct HTTP status codes.
- models.py: Ensures Post model supports all required fields and status (published/draft/archived) for filtering and admin access.
- schemas.py: Defines Pydantic schemas for post creation, update, and response, including validation and status handling.
- database.py: Implements DB access functions for post CRUD operations and paginated queries, used by the API endpoints.
- tests/test_posts.py: Provides unit tests for all post API endpoints, covering authentication, validation, error cases, and pagination with a mock DB.
