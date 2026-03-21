# API Reference

## Posts API

### GET /api/posts
- Returns paginated list of published posts.
- Query params: `page` (int, default 1), `size` (int, default 10)
- Response: `{ "items": [PostResponse], "total": int }`
- No authentication required.

### GET /api/posts/{id}
- Returns a single published post by ID.
- 404 if not found or not published.
- No authentication required.

### POST /api/posts
- Create a new post (admin only).
- Requires `Authorization: Bearer <JWT token>` header.
- Body: PostCreate
- Response: PostResponse, 201 Created
- 401 if not authenticated as admin.

### PUT /api/posts/{id}
- Update a post (admin only).
- Requires `Authorization: Bearer <JWT token>` header.
- Body: PostUpdate
- Response: PostResponse
- 404 if not found, 401 if not admin.

### DELETE /api/posts/{id}
- Delete a post (admin only).
- Requires `Authorization: Bearer <JWT token>` header.
- Response: 204 No Content
- 404 if not found, 401 if not admin.

#### PostCreate
- title: str (max 255)
- content: str
- author: str (max 100)
- status: draft|published|archived (optional, default draft)

#### PostUpdate
- title/content/author/status: optional fields

#### PostResponse
- id, title, content, author, status, created_at, updated_at

## Authentication API

### POST /api/auth/login
- Accepts: `{ "username": str, "password": str }` (JSON body)
- Validates credentials against `ADMIN_USERNAME` and `ADMIN_PASSWORD` environment variables.
- On success: returns `{ "token": <JWT token> }` (signed with `JWT_SECRET`, expires in 1 hour).
- On failure: returns 401 Unauthorized.

### GET /api/auth/me
- Requires: `Authorization: Bearer <JWT token>` header.
- On valid token: returns `{ "authenticated": true }`.
- On invalid/missing/expired token: returns 401 Unauthorized.
