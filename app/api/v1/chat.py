from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from app.models.chat_request import ChatRequest
from app.proxy.prompt import begin_prompt, confirm_prompt
from app.proxy.providers.gateway import available_models

router = APIRouter()


@router.post("/chat/scan")
async def scan(request: Request):
    try:
        body = await request.json()
    except Exception:
        body = {}
    result = begin_prompt(ChatRequest.from_dict(body))
    return JSONResponse(result)


@router.post("/chat/confirm")
async def confirm(request: Request):
    try:
        body = await request.json()
    except Exception:
        body = {}
    result = confirm_prompt(
        body.get("promptId") or "",
        body.get("choice") or "",
        body.get("model"),
    )
    return JSONResponse(result)


@router.get("/models")
def models():
    return {"models": available_models()}
