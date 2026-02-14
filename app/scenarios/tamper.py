import json
import time
import jwt
from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")

SECRET = "jwt-playground-secret"
ALG = "HS256"


@router.get("/", response_class=HTMLResponse)
async def show_form(request: Request):
    """Show a form with a starter payload that can be tampered with."""
    now = int(time.time())
    starter_payload = {
        "sub": "alice",
        "role": "user",
        "iat": now,
        "exp": now + 600,
    }
    return templates.TemplateResponse(
        "scenario_tamper.html",
        {
            "request": request,
            "original": starter_payload,
            "token_result": None,
            "error": None,
        },
    )


@router.post("/experiment", response_class=HTMLResponse)
async def tamper_token(
    request: Request,
    payload_json: str = Form(...),
    resign: str | None = Form(None),
):
    """Accept a JSON payload, optionally re-sign it, and show the outcome.

    - If `resign` is provided, we sign the tampered payload with the lab secret.
    - Otherwise we pretend the attacker just pasted a forged token string,
      and show that verification fails.
    """
    error: str | None = None
    token_result: dict | None = None
    now = int(time.time())

    try:
        payload = json.loads(payload_json)
    except json.JSONDecodeError as exc:  # type: ignore[unreachable]
        error = f"Invalid JSON: {exc}"
        payload = {}

    if not error:
        # Ensure some sensible defaults so the UI stays readable.
        payload.setdefault("iat", now)
        payload.setdefault("exp", now + 600)

        if resign:
            # This simulates an attacker who *can* sign tokens (e.g. key leak).
            token = jwt.encode(payload, SECRET, algorithm=ALG)
            try:
                verified = jwt.decode(token, SECRET, algorithms=[ALG])
                token_result = {
                    "mode": "resigned",
                    "token": token,
                    "verified_payload": verified,
                }
            except jwt.PyJWTError as exc:  # pragma: no cover - defensive
                error = f"Verification failed after resigning: {exc}"
        else:
            # In a real setting this would be a token string; here we just
            # show that without the correct key, verification fails.
            # We deliberately do *not* sign it.
            try:
                jwt.decode("forged-token", SECRET, algorithms=[ALG])
            except jwt.PyJWTError as exc:
                error = (
                    "Unsigned / forged token cannot be verified: "
                    f"{exc.__class__.__name__}"
                )

    return templates.TemplateResponse(
        "scenario_tamper.html",
        {
            "request": request,
            "original": payload if payload else None,
            "token_result": token_result,
            "error": error,
        },
    )
