# Security & Data Governance Policy

## 1. Authentication & Session Security
- **Password Hashing**: Native Bcrypt with adaptive salt generation and 72-byte truncation compliance.
- **JWT Cryptography**: Signed HS256 JWT tokens with distinct Access (1 day) and Refresh (7 days) lifetimes.
- **Token Invalidation**: Immediate local token removal upon logout and server-side user deactivation checks on every request.

## 2. Role-Based Access Control (RBAC)
- Strict dependency injection gates on FastAPI routes:
  - `get_current_user`: Base authentication.
  - `require_farmer`: Access to personal scans, farms, and fields.
  - `require_expert`: Access to agronomist review queues and prescription submission.
  - `require_admin`: Access to system analytics, model metrics, and user management.
- Strict resource ownership verification prevents cross-tenant data access (users cannot view/modify another farmer's farms or scans).

## 3. Upload & File Security
- Header validation (magic bytes verification via Pillow).
- MIME type and file extension allow-listing (`.jpg`, `.jpeg`, `.png`, `.webp`).
- Strict 15MB file size constraint and pixel dimension bounds (minimum 50x50, maximum 10000x10000).
- Filename sanitization with random UUID v4 strings to prevent directory traversal attacks.

## 4. Agronomic & Chemical Safety
- AI recommendations provide cultural and biological management steps.
- Explicit disclaimers warn farmers against applying unverified chemical dosages and instruct compliance with registered regional label regulations.
