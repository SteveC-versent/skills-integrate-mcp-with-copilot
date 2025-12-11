# Add basic user accounts and authentication (keep lightweight)

**Problem / Motivation**
The current app identifies students only by email strings. To assign creators to events and to protect certain actions (create/edit events), we need lightweight user accounts and authentication.

**Proposed change**
- Add a minimal `User` model backed by SQLite with fields: `id`, `email` (unique), `full_name` (optional), and `password_hash`.
- Use FastAPI's OAuth2 password flow with JWT tokens (`fastapi.security.OAuth2PasswordBearer` + `pyjwt` or `python-jose`) for auth.
- Add endpoints: `POST /auth/register`, `POST /auth/token` (for login), and `GET /auth/me` (profile).
- Update frontend to allow sign-up/login in a minimal way (optionally add a modal or simple form) and include token on protected requests.

**Acceptance criteria**
- Users can register and login to receive a JWT token.
- Protected endpoint example: `POST /activities` to create an activity requires valid token.
- README updated with auth instructions.

**Labels**: enhancement, auth, backend

**Estimated effort**: small (1–2 days)
