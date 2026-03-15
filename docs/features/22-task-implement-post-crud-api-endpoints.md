## What it does
Implements full CRUD REST API endpoints for blog posts, including public and admin routes. Public endpoints allow anyone to view published posts, while creating, updating, deleting, and viewing all posts (including drafts) require admin authentication. All endpoints return appropriate HTTP status codes and support pagination for listing posts.

## How to use it
- `GET /api/posts?page=1&size=10`: Returns a paginated list of published posts (no auth required).
- `GET /api/posts/{id}`: Returns a single published post by ID (no auth required).
- `POST /api/posts` (admin only): Creates a new post. Requires `Authorization: Bearer admin-token` header and a JSON body matching the PostCreate schema.
- `PUT /api/posts/{id}` (admin only): Updates a post. Requires `Authorization: Bearer admin-token` header and a JSON body matching the PostUpdate schema.
- `DELETE /api/posts/{id}` (admin only): Deletes a post. Requires `Authorization: Bearer admin-token` header.
- `GET /api/admin/posts` (admin only): Returns all posts, including drafts. Requires `Authorization: Bearer admin-token` header.

## Internals
main.py: Adds all CRUD API endpoints for posts, including authentication checks, pagination, and proper status codes.
models.py: Ensures the Post model supports published/draft/archived status and all required fields for CRUD operations.
schemas.py: Defines Pydantic schemas for post creation, update, and response, including status and validation.
database.py: Implements database utility functions for post CRUD operations and pagination.
tests/test_posts.py: Provides unit tests for all post API endpoints, using mock database functions to cover all acceptance criteria.
docs/api.md: Documents the new post API endpoints, authentication requirements, and response formats.
