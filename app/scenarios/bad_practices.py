import time
import jwt
from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")

# NOTE: Everything in this file is intentionally wrong or unsafe.
# It exists purely to explain what *not* to do.

INSECURE_SECRET = "do-not-use-this-in-production"
ALG_INSECURE = "HS256"


@router.get("/", response_class=HTMLResponse)
async def show_form(request: Request):
    return templates.TemplateResponse(
        "scenario_bad.html",
        {"request": request, "issued": None, "verification": None},
    )


@router.post("/issue-hs256", response_class=HTMLResponse)
async def issue_hs256(request: Request, username: str = Form("alice")):
    """Issue a token with an obviously weak secret.

    This demonstrates how leaking the key gives an attacker full power
    to mint arbitrary roles and identities.
    """
    now = int(time.time())
    payload = {
        "sub": username,
        "role": "user",
        "iat": now,
        "exp": now + 600,
    }
    token = jwt.encode(payload, INSECURE_SECRET, algorithm=ALG_INSECURE)

    return templates.TemplateResponse(
        "scenario_bad.html",
        {
            "request": request,
            "issued": {
                "mode": "weak-secret",
                "token": token,
                "payload": payload,
            },
            "verification": None,
        },
    )


@router.post("/accept-alg-none", response_class=HTMLResponse)
async def accept_alg_none(request: Request, token: str = Form(...)):
    """Simulate a server that naively trusts alg=none.

    We do *not* implement a real alg=none parser here, but we explain the risk
    and show that turning off verification means trusting attacker-controlled data.
    """
    verification = {
        "mode": "alg-none",
        "warning": (
            "If a server accepts tokens with alg=none or skips verification, "
            "an attacker can forge any identity or role they want."
        ),
        "token_sample": token,
    }

    return templates.TemplateResponse(
        "scenario_bad.html",
        {"request": request, "issued": None, "verification": verification},
    )
