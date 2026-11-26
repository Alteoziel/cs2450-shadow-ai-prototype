from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from app.proxy.prompt import flagged_report
from app.proxy.providers.keys import COMPANIES, clear_key, key_status, save_keys
from app.security.auth.session import admin_cookie, admin_password, is_admin, password_matches

router = APIRouter()


def _unauthorized():
    return JSONResponse({"ok": False, "message": "Admin login required."}, status_code=401)


@router.post("/login")
async def login(request: Request):
    try:
        body = await request.json()
    except Exception:
        body = {}
    if not admin_password():
        return JSONResponse(
            {"ok": False, "message": "Set ADMIN_PASSWORD in .env and restart the app."},
            status_code=400,
        )
    if not password_matches(body.get("password") or ""):
        return JSONResponse(
            {"ok": False, "message": "That password is not the admin password."},
            status_code=401,
        )
    response = JSONResponse({"ok": True})
    response.set_cookie(
        "shadow_admin",
        admin_cookie(),
        httponly=True,
        samesite="lax",
        path="/",
    )
    return response


@router.post("/logout")
def logout():
    response = JSONResponse({"ok": True})
    response.delete_cookie("shadow_admin", path="/")
    return response


@router.get("/session")
def session(request: Request):
    return {"ok": is_admin(request)}


@router.get("/log")
def log(request: Request, model: str | None = None, blocked: bool = False):
    if not is_admin(request):
        return _unauthorized()
    return flagged_report(model=model, blocked_only=blocked)


@router.get("/keys")
def keys(request: Request):
    if not is_admin(request):
        return _unauthorized()
    return {"ok": True, **key_status()}


@router.post("/keys")
async def set_keys(request: Request):
    if not is_admin(request):
        return _unauthorized()
    try:
        body = await request.json()
    except Exception:
        body = {}
    save_keys(
        body.get("openai") or "",
        body.get("anthropic") or "",
        body.get("gemini") or "",
    )
    return {"ok": True, **key_status()}


@router.post("/keys/clear")
async def remove_key(request: Request):
    if not is_admin(request):
        return _unauthorized()
    try:
        body = await request.json()
    except Exception:
        body = {}
    company = body.get("company") or ""
    if company not in COMPANIES:
        return JSONResponse(
            {"ok": False, "message": "Choose OpenAI, Anthropic, or Gemini."},
            status_code=400,
        )
    clear_key(company)
    return {"ok": True, **key_status()}
