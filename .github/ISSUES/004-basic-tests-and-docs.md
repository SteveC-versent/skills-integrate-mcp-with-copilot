# Add basic tests and update README with run instructions

**Problem / Motivation**
There's no automated test coverage or clear run instructions for development and the lightweight DB/auth changes. Adding basic tests and updating docs will make the repo contributor-friendly.

**Proposed change**
- Add unit tests for: persistence (create/read activities), signup/unregister behavior, and auth endpoints (register/login and protected create route).
- Use `pytest` and a test SQLite DB in-memory for speed (`sqlite:///:memory:`) during tests.
- Update `src/README.md` with clear setup and run instructions and document new endpoints and auth usage.

**Acceptance criteria**
- Minimal test suite runs with `pytest` and covers the core flows described above.
- README contains steps for local dev and how to run tests.

**Labels**: chore, tests, docs

**Estimated effort**: small (1 day)
