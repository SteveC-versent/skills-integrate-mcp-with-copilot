# Add protected event creation and basic CRUD endpoints

**Problem / Motivation**
Activities are currently hard-coded. Allowing authenticated users to create and manage activities will enable the app to be useful without making it complex.

**Proposed change**
- Add `POST /activities` (protected): create a new activity (requires auth). The creator is saved.
- Add `PUT /activities/{id}` (protected, only creator or admin): update activity details.
- Add `DELETE /activities/{id}` (protected, only creator or admin): remove activity.
- Keep the existing signup/unregister endpoints working with the DB-backed data model.
- Update frontend to allow activity creation for authenticated users (a small form) and show edit/delete buttons for creators.

**Acceptance criteria**
- Authenticated users can create events via `POST /activities` and see them in `GET /activities`.
- Only the creator (or a simple admin flag) can edit or delete an activity.
- Frontend reflects create/update/delete flows (UI and API calls).

**Labels**: enhancement, backend, frontend

**Estimated effort**: small-to-moderate (2–3 days)
