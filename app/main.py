from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .scenarios import normal, tamper, expiry, bad_practices, aud_iss

app = FastAPI(title="JWT Playground", description="Interactive JWT scenarios for learning.")

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/lesson", response_class=HTMLResponse)
async def lesson(request: Request):
    """Guided entry point that strings together all scenarios."""
    return templates.TemplateResponse("lesson_mode.html", {"request": request})


app.include_router(normal.router, prefix="/normal", tags=["normal"])
app.include_router(tamper.router, prefix="/tamper", tags=["tamper"])
app.include_router(expiry.router, prefix="/expiry", tags=["expiry"])
app.include_router(bad_practices.router, prefix="/bad", tags=["bad-practices"])
app.include_router(aud_iss.router, prefix="/aud-iss", tags=["aud-iss"])
