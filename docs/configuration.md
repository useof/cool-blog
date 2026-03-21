# Configuration

## Environment Variables

- `ADMIN_USERNAME`: Admin login username (required for authentication)
- `ADMIN_PASSWORD`: Admin login password (required for authentication)
- `JWT_SECRET`: Secret key for signing JWT tokens (required for authentication)

All authentication endpoints require these environment variables to be set. If any are missing, authentication will be disabled and all login attempts will be rejected.
