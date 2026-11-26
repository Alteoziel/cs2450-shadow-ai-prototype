from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import FileResponse

from app.api.v1.admin import router as admin_router
from app.api.v1.chat import router

load_dotenv()

app = FastAPI(title="Shadow-AI Gateway")
app.include_router(router, prefix="/api/v1")
app.include_router(admin_router, prefix="/api/v1/admin")

_ROOT = Path(__file__).resolve().parents[1]
_DASHBOARD = _ROOT / "dashboard" / "index.html"
_ADMIN = _ROOT / "dashboard" / "admin.html"


@app.get("/")
def employee_chat():
    return FileResponse(_DASHBOARD)


@app.get("/admin")
def admin_page():
    return FileResponse(_ADMIN)
