# JWT Playground

Interactive FastAPI app for learning how JSON Web Tokens (JWTs) are issued,
validated, and broken – safely, in a controlled lab.

The goal is to have something you can use to **teach** JWT concepts to
engineers and security folks, not just a code snippet that prints a token.

---

## Scenarios

All scenarios are available from the homepage once you start the app.

### 1. Signed JWT flow (`/normal`)

Issue a signed JWT for a user and inspect its header and payload.

- Form takes a username (default `alice`).
- Backend issues a HS256 token with `sub`, `role`, `iat`, and `exp`.
- UI shows:
  - the full JWT string,
  - decoded header JSON,
  - decoded payload (claims).

Use this as the "good path" before breaking anything.

### 2. Tampering with claims (`/tamper`)

Explore what happens when you edit the payload.

- Start from a JSON payload like:
  ```json
  {
    "sub": "alice",
    "role": "user",
    "iat": 1700000000,
    "exp": 1700000600
  }
  ```
- Modify it in the textarea (e.g. change `role` to `admin`).
- Buttons:
  - **Re-sign with lab key** – simulates an attacker who has the signing key
    (e.g. key leak).
  - **Send as forged token** – simulates a client that can only edit JSON,
    not sign tokens.

The app shows whether verification succeeds and what the verified payload
looks like in each case.

### 3. Expired tokens (`/expiry`)

Play with `iat` and `exp` to understand token lifetime.

- Choose:
  - `lifetime_seconds` – how long the token should be valid,
  - `backdated_seconds` – how far in the past to set `iat`.
- The lab issues a token and then immediately verifies it using the real key.
- UI shows:
  - payload JSON with `iat` and `exp`,
  - verification result (success vs `ExpiredSignatureError`).

This is useful for explaining why clock skew and token lifetime matter.

### 4. Bad practices (training only) (`/bad`)

This scenario is there to explain **what not to do** with JWTs.
Everything here is intentionally unsafe and exists purely for defensive
training.

Two main demonstrations:

- **Weak secret key** – issues a token with an obviously bad secret.
  This makes it clear how a leaked key lets attackers mint arbitrary roles
  and identities.

- **Skipping verification / alg=none mindset** – simulates a server that
  "just trusts" the token without checking a signature. The page explains
  why this effectively turns a JWT into an editable JSON blob.

---

## Running locally

```bash
./scripts/run.sh
```

Then open <http://localhost:8000/> in your browser.

The app will create a virtual environment, install dependencies, and run
`uvicorn` with hot reload.

---

## Safety notes

- Secrets, algorithms, lifetimes, and patterns in this lab are
  **deliberately simplified** and should never be copied into production.
- The "bad practices" scenario exists so you can have an honest
  conversation about historical JWT failures without repeating them.
- Only use this app on systems and networks you control.
