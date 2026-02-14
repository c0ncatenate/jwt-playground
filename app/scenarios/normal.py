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
        "scenario_normal.html",
        {"request": request, "result": None},
    )


@router.post("/issue", response_class=HTMLResponse)
async def issue_token(request: Request, username: str = Form("alice")):
    now = int(time.time())
    payload = {
        "sub": username,
        "role": "user",
        "iat": now,
        "exp": now + 600,
    }
    token = jwt.encode(payload, SECRET, algorithm=ALG)

    header = jwt.get_unverified_header(token)
    decoded_payload = jwt.decode(token, options={"verify_signature": False})

    context = {
        "request": request,
        "result": {
            "token": token,
            "header": header,
            "payload": decoded_payload,
        },
    }
    return templates.TemplateResponse("scenario_normal.html", context)
