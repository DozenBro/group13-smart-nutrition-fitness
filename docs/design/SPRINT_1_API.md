# Sprint 1 API Contract

**21 November 2026 · Implemented by S1-04 and S1-06**

[OpenAPI (Swagger UI)](http://127.0.0.1:8013/docs) when the backend is running · [Sprint 1 requirements](../sprints/SPRINT_1.md) · [Detailed ERD](SPRINT_1_ERD.md)

This document records the request/response contract for the account, profile, and measurement endpoints implemented in S1-04 and S1-06, plus the TDEE estimate endpoint. It supplements the food endpoints already documented in `SPRINT_1.md`. Fictional examples; no real user data.

## Conventions

- **Content type:** `application/json` for all request and response bodies.
- **Authentication:** `Authorization: Bearer <token>` header on protected endpoints. The token is returned once by `POST /api/auth/login` and is never recoverable from the server.
- **Session lifetime:** 7 days from login. Expired sessions are rejected with `401`.
- **Error shape:** all error responses use FastAPI's standard `{"detail": "<message>"}` body.
- **Status codes:** `401` = not authenticated (missing/invalid/expired/revoked token, or locked account on a protected request); `403` = authenticated but forbidden (only `POST /api/auth/login` on a locked account uses this); `409` = conflict (duplicate email); `422` = Pydantic validation failure.
- **Email normalization:** emails are lowercased and stripped before storage and lookup. `Alice@Example.COM` and `alice@example.com` are the same account.

## `POST /api/auth/register` — public

Creates a Member account. Does not create a session; the client must call `POST /api/auth/login` afterward.

**Request:**
```json
{ "email": "alice@example.com", "password": "AlicePass123!" }
```

| Field | Type | Rules |
| --- | --- | --- |
| `email` | string | Valid email; normalized (lowercase + strip) before storage |
| `password` | string | 8–128 characters |

Extra fields are rejected (`extra='forbid'`). In particular, `role` and `user_id` cannot be supplied by the client — this satisfies US-A01 AC4.

**Responses:**

- `201` — created:
  ```json
  { "id": 42, "email": "alice@example.com", "role": "member", "is_locked": false, "created_at": "2026-11-21T09:00:00Z" }
  ```
- `409` — email already registered (after normalization):
  ```json
  { "detail": "An account with this email already exists." }
  ```
- `422` — invalid email format, short password, or extra fields.

Passwords and password hashes never appear in any response.

## `POST /api/auth/login` — public

**Request:**
```json
{ "email": "alice@example.com", "password": "AlicePass123!" }
```

**Responses:**

- `200` — success:
  ```json
  {
    "token": "n3Xk9...",
    "expires_at": "2026-11-28T09:00:00Z",
    "user": { "id": 42, "email": "alice@example.com", "role": "member", "is_locked": false, "created_at": "2026-11-21T09:00:00Z" }
  }
  ```
- `401` — wrong email **or** wrong password, same message for both (per US-A02 AC2):
  ```json
  { "detail": "Invalid credentials." }
  ```
- `403` — account is locked (US-AD01 AC3):
  ```json
  { "detail": "Account is locked." }
  ```

The raw `token` is returned once. The server stores only `sha256(token)` in `sessions.token_hash` (per ERD §sessions). Multiple concurrent sessions per user are allowed; `logout` revokes only the current one.

## `POST /api/auth/logout` — requires auth

**Headers:** `Authorization: Bearer <token>`

**Responses:**

- `204` — current session revoked (`sessions.revoked_at` set). Other sessions for the same user remain valid.
- `401` — missing, invalid, expired, or already-revoked token.

## `GET /api/auth/me` — requires auth

**Headers:** `Authorization: Bearer <token>`

**Response `200`:**
```json
{ "id": 42, "email": "alice@example.com", "role": "member", "is_locked": false, "created_at": "2026-11-21T09:00:00Z" }
```

**Responses on failure:** `401` with `{"detail": "Invalid or expired session."}` for any of: missing token, unknown token hash, revoked session, expired session, or a locked account whose session somehow survives revocation. A locked account is treated as unauthenticated rather than returning `403`, because a locked user's sessions should already have been revoked by S1-09; revealing "account exists but is locked" to a stale-token holder is less safe than treating it as unauthenticated.

This endpoint is how the frontend determines login state after a page refresh (US-A02 AC1).

## `GET /api/profile` — requires auth

**Headers:** `Authorization: Bearer <token>`

**Response `200`** (profile set):
```json
{
  "user_id": 42,
  "age_years": 25,
  "sex_for_equation": "male",
  "activity_level": "moderately_active",
  "updated_at": "2026-11-21T09:05:00Z"
}
```

**Response `200`** (profile not yet set):
```json
{ "user_id": 42, "age_years": null, "sex_for_equation": null, "activity_level": null, "updated_at": null }
```

Returns `200` with nulls rather than `404` when the profile is empty, so the frontend can distinguish "not filled in yet" from "endpoint unreachable."

The `user_id` is always the authenticated user's ID. The client cannot request another user's profile — there is no ID in the path (US-H01 AC4).

## `PUT /api/profile` — requires auth

**Headers:** `Authorization: Bearer <token>`

**Request:**
```json
{ "age_years": 25, "sex_for_equation": "male", "activity_level": "moderately_active" }
```

| Field | Type | Rules |
| --- | --- | --- |
| `age_years` | integer | 19–78 inclusive |
| `sex_for_equation` | string | `"male"` or `"female"` |
| `activity_level` | string | one of `"sedentary"`, `"lightly_active"`, `"moderately_active"`, `"active"`, `"very_active"` |

All three fields are required together. Partial updates are not supported, because a partial profile cannot compute TDEE — there is no useful intermediate state. If Bảo later wants partial saves for UX reasons (save age first, return to fill the rest), that's a contract change for a follow-up.

**Responses:**

- `200` — updated; returns the same shape as `GET /api/profile` with `updated_at` refreshed.
- `422` — any field out of range, unknown code, or extra fields. **The stored profile is unchanged** (US-H01 AC3): the route only commits after validation succeeds.
- `401` — no/invalid session.

The database CHECK constraints from the S1-03 migration enforce the same limits at the DB level (defense in depth); the Pydantic validation is the primary gate and the source of the `422`.

## `GET /api/measurements` — requires auth

**Headers:** `Authorization: Bearer <token>`

Returns the authenticated user's measurements, newest first.

**Query:** `limit` from 1 to 100, default 30.

**Response `200`:**
```json
[
  { "id": 42, "weight_kg": 70.0, "height_cm": 175.0, "bmi": 22.86, "created_at": "2026-11-21T09:10:00Z" }
]
```

`bmi` is computed per row. The response never contains a stored TDEE — see `GET /api/health/estimate` for the current estimate.

**Responses on failure:** `401` (no/invalid/expired/revoked token) or `422` (`limit` out of range).

## `POST /api/measurements` — requires auth

**Headers:** `Authorization: Bearer <token>`

**Request:**
```json
{ "weight_kg": 70, "height_cm": 175 }
```

Extra fields are rejected (`extra='forbid'`); in particular, `user_id` cannot be supplied by the client — ownership comes from the token.

**Response `201`:**
```json
{ "id": 42, "weight_kg": 70.0, "height_cm": 175.0, "bmi": 22.86, "created_at": "2026-11-21T09:10:00Z" }
```

**Responses on failure:** `401` (no/invalid token) or `422` (out-of-range weight/height).

## `GET /api/health/estimate` — requires auth

**Headers:** `Authorization: Bearer <token>`

Returns the authenticated user's current health estimate, using their **most recent measurement** and their **current profile**. This is not a historical TDEE: the estimate reflects today's profile against today's measurement, per ERD §measurements.

**Response `200`** (profile complete):
```json
{
  "bmi": 22.86,
  "tdee": 2594.31,
  "tdee_missing_fields": [],
  "measurement_id": 42,
  "measurement_created_at": "2026-11-21T09:10:00Z",
  "profile_complete": true
}
```

**Response `200`** (profile incomplete):
```json
{
  "bmi": 22.86,
  "tdee": null,
  "tdee_missing_fields": ["age_years", "sex_for_equation", "activity_level"],
  "measurement_id": 42,
  "measurement_created_at": "2026-11-21T09:10:00Z",
  "profile_complete": false
}
```

**Response `200`** (no measurement yet):
```json
{
  "bmi": null,
  "tdee": null,
  "tdee_missing_fields": [],
  "measurement_id": null,
  "measurement_created_at": null,
  "profile_complete": false
}
```

The frontend should:
- Hide or disable the TDEE panel when `tdee` is `null`
- Show a "fill in your profile" prompt listing `tdee_missing_fields` when `profile_complete` is `false` but `bmi` is not `null`
- Show a "record your first measurement" prompt when `measurement_id` is `null`

The formula and inputs follow the S1-07 TDEE proposal; the result is `null` when the profile is incomplete, per US-H04 AC3.

**Responses on failure:** `401` (no/invalid/expired/revoked token).

## `GET /api/foods`, `POST /api/foods`, `DELETE /api/foods/{id}` — public (Sprint 3 prep)

These are documented in `SPRINT_1.md`; not repeated here. They do not participate in Sprint 1 auth.

Admin account management (S1-09: list, lock, unlock) will extend this document when implemented.

## Open decisions referenced by this contract

- **D-03:** Bearer-token transport, 7-day lifetime, sha256 token hash, lowercase+strip email, and min-8-character password are implemented per this contract. CSRF protection is not applicable to a Bearer-header design. Initial Admin provisioning is via `manage.py create-admin`. D-03 remains open for the group's formal confirmation.
- **D-02:** Profile field limits (age 19–78, the five activity codes) follow the S1-07 TDEE proposal. The `GET /api/health/estimate` endpoint uses the S1-07 proposed formula; if D-02 changes the equation or activity factors, that endpoint inherits the change. D-02 remains open for team confirmation.

## Related files

- `backend/auth.py`, `backend/profiles.py`, `backend/auth_schemas.py`, `backend/dependencies.py` — S1-04 auth and profile implementation.
- `backend/measurements.py`, `backend/measurement_schemas.py`, `backend/health_api.py` — S1-06 measurement ownership and TDEE estimate implementation.
- `tests/test_auth.py`, `tests/test_profiles.py` — 18 tests for the account and profile endpoints.
- `tests/test_measurements.py`, `tests/test_permissions.py` — measurement tests plus cross-account and estimate tests.
- `backend/models.py` §`User`, `Profile`, `Session`, `Measurement` — storage shapes.
- `migrations/versions/002_auth_and_ownership.py` — schema, constraints, and indexes for Sprint 1 accounts.
