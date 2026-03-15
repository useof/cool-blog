# API Reference

## Posts API

### GET /api/posts
- Returns paginated list of published posts (10 per page).
- Query params: `page` (default 1)
- Response: `{ items: [Post], total: int, page: int }`
- No authentication required.

### GET /api/posts/{id}
- Returns a single published post by ID.
- 404 if not found or not published.
- No authentication required.

### POST /api/posts
- Create a new post.
- Requires Bearer token authentication.
- Body: `{ title, content, author, status? }`
- Returns created post. Status 201.

### PUT /api/posts/{id}
- Update a post by ID.
- Requires Bearer token authentication.
- Body: `{ title?, content?, author?, status? }`
- Returns updated post.

### DELETE /api/posts/{id}
- Delete a post by ID.
- Requires Bearer token authentication.
- Returns 204 No Content.

#### Authentication
- All mutating/admin routes (POST, PUT, DELETE) require `Authorization: Bearer <token>` header.
- Any non-empty token is accepted for testing.

