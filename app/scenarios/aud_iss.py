from __future__ import annotations

import time
import jwt
from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.config import LAB_JWT

router = APIRouter()
templates = Jinja2Templates(directory="templates")


EXPECTED_ISSUER = "auth.jwt-playground.local"
EXPECTED_AUDIENCE = "service-a"


@router.get("/", response_class=HTMLResponse)
async def show_form(request: Request) -> HTMLResponse:
    """Show a form for playing with aud/iss verification.

    The idea is to simulate two services that should not accept each
    other's tokens if audience/issuer are checked correctly.
    """
    return templates.TemplateResponse(
        "scenario_aud_iss.html",
        {
            "request": request,
            "result": None,
            "error": None,
            "expected_issuer": EXPECTED_ISSUER,
            "expected_audience": EXPECTED_AUDIENCE,
        },
    )


@router.post("/issue", response_class=HTMLResponse)
async def issue_for_audience(
    request: Request,
    username: str = Form("alice"),
    audience: str = Form("service-a"),
    issuer: str = Form(EXPECTED_ISSUER),
) -> HTMLResponse:
    now = int(time.time())
    payload = {
        "sub": username,
        "role": "user",
        "iat": now,
        "exp": now + LAB_JWT.lifetime_seconds,
        "aud": audience,
        "iss": issuer,
    }

    token = jwt.encode(payload, LAB_JWT.secret, algorithm=LAB_JWT.algorithm)

    # Verify as if this were "service-a".
    try:
        verified_service_a = jwt.decode(
            token,
            LAB_JWT.secret,
            algorithms=[LAB_JWT.algorithm],
            audience=EXPECTED_AUDIENCE,
            issuer=EXPECTED_ISSUER,
        )
        service_a_error: str | None = None
    except jwt.PyJWTError as exc:  # pragma: no cover - defensive
        verified_service_a = None
        service_a_error = f"Rejected for service A: {exc.__class__.__name__}"

    # Verify as if this were "service-b" with a different audience.
    try:
        verified_service_b = jwt.decode(
            token,
            LAB_JWT.secret,
            algorithms=[LAB_JWT.algorithm],
            audience="service-b",
            issuer=EXPECTED_ISSUER,
        )
        service_b_error: str | None = None
    except jwt.PyJWTError as exc:
        verified_service_b = None
        service_b_error = f"Rejected for service B: {exc.__class__.__name__}"

    result = {
        "token": token,
        "payload": payload,
        "verified_service_a": verified_service_a,
        "verified_service_b": verified_service_b,
        "service_a_error": service_a_error,
        "service_b_error": service_b_error,
    }

    return templates.TemplateResponse(
        "scenario_aud_iss.html",
        {
            "request": request,
            "result": result,
            "error": None,
            "expected_issuer": EXPECTED_ISSUER,
            "expected_audience": EXPECTED_AUDIENCE,
        },
    )
