# Hands-On 9 — Authentication & Security: JWT, OAuth2 & OWASP

> Builds on the Hands-On 8 versioned FastAPI app.

## Setup
```bash
pip install -r requirements.txt
cd fastapi_coursemanager
uvicorn main:app --reload
```

## Test flow
```bash
# 1. Register
curl -X POST http://127.0.0.1:8000/api/v1/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"email":"prof@college.edu","password":"S3cure!Pass"}'
# -> 201; a second call with the same email -> 409 Conflict

# 2. Login
curl -X POST http://127.0.0.1:8000/api/v1/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"email":"prof@college.edu","password":"S3cure!Pass"}'
# -> {"access_token": "...", "token_type": "bearer"}

# 3. Unauthenticated write -> 401
curl -X POST http://127.0.0.1:8000/api/v1/courses/ \
  -H "Content-Type: application/json" \
  -d '{"name":"Databases","code":"CS201","credits":4}'

# 4. Authenticated write -> 201
curl -X POST http://127.0.0.1:8000/api/v1/courses/ \
  -H "Authorization: Bearer <paste access_token here>" \
  -H "Content-Type: application/json" \
  -d '{"name":"Databases","code":"CS201","credits":4}'

# 5. Reads remain public
curl http://127.0.0.1:8000/api/v1/courses/
```

## Files
- `security.py` — `get_password_hash()` / `verify_password()` (bcrypt via
  passlib), `create_access_token()` / `decode_access_token()` (JWT via
  python-jose), with a comment on why bcrypt beats MD5/SHA-256 for passwords
- `models.py` — adds the `User` model (email, hashed_password, is_active)
- `schemas.py` — adds `UserRegister`, `UserResponse`, `Token`, `LoginRequest`
- `auth.py` — `POST /api/v1/auth/register/` (409 on duplicate email),
  `POST /api/v1/auth/login/` (issues a 30-min JWT), and the
  `get_current_user()` dependency (401 on invalid/expired token), plus a
  comment contrasting the OAuth2 Authorization Code flow with this
  simple JWT login
- `main.py` — `CORSMiddleware` allowing `http://localhost:3000`;
  `POST`/`DELETE /api/v1/courses/` now require
  `Depends(get_current_user)`

## Expected Outcome
Registration stores only the bcrypt hash — never the plain-text password.
A duplicate registration returns 409. Login returns a valid JWT.
`GET /api/v1/courses/` works without auth; `POST /api/v1/courses/` returns
401 without a valid token and 201 with one. CORS allows `localhost:3000`.
