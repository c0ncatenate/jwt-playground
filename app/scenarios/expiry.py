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
    return templates.TemplateResponse(
        "scenario_expiry.html",
        {"request": request, "result": None, "error": None},
    )


@router.post("/issue", response_class=HTMLResponse)
async def issue_with_lifetime(
    request: Request,
    username: str = Form("alice"),
    lifetime_seconds: int = Form(60),
    backdated_seconds: int = Form(0),
):
    now = int(time.time())
    iat = now - backdated_seconds
    exp = iat + lifetime_seconds

    payload = {
        "sub": username,
        "role": "user",
        "iat": iat,
        "exp": exp,
    }

    token = jwt.encode(payload, SECRET, algorithm=ALG)

    # Try verifying as the server would.
    try:
        verified = jwt.decode(token, SECRET, algorithms=[ALG])
        error = None
    except jwt.ExpiredSignatureError as exc:
        verified = None
        error = f"Token expired: {exc.__class__.__name__}"
    except jwt.PyJWTError as exc:  # pragma: no cover - defensive
        verified = None
        error = f"Verification error: {exc.__class__.__name__}"

    result = {
        "token": token,
        "payload": payload,
        "verified": verified,
    }

    return templates.TemplateResponse(
        "scenario_expiry.html",
        {"request": request, "result": result, "error": error},
    )
