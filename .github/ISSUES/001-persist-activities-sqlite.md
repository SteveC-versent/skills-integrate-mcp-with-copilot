# Persist activities to SQLite and replace in-memory store

**Problem / Motivation**
Currently the application stores activities in an in-memory Python dict. Data is lost on restart and it's difficult to extend the app with create/update/delete operations safely. Adding a lightweight persistence layer will keep the project small while enabling important features.

**Proposed change**
- Add a simple SQLite backend using `SQLModel` or `SQLAlchemy` (choose whichever you prefer; `SQLModel` is lightweight and fits FastAPI well).
- Create an `Activity` model with fields: `id` (int autoincrement), `name` (unique), `description`, `schedule`, `max_participants`, and `participants` (could be a serialized JSON array or a separate participant table depending on scope).
- Replace the in-memory `activities` dict with DB-backed queries in endpoints (`/activities`, signup, unregister).
- Provide a small migration or initialization script to create the DB file and tables (no heavy migration tool required for now—just `create_all`).

**Acceptance criteria**
- Running the app creates or opens a local `sqlite` DB (e.g., `data.db`) if not present.
- `GET /activities` returns activities persisted in the DB.
- Signing up and unregistering update the DB and persist after server restarts.
- Unit test(s) demonstrate persistence behavior.

**Labels**: enhancement, persistence, backend

**Estimated effort**: small (1–2 days)
