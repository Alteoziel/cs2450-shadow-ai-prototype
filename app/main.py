from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import FileResponse

from app.api.v1.chat import router

load_dotenv()

app = FastAPI(title="Shadow-AI Gateway")
app.include_router(router, prefix="/api/v1")

_DASHBOARD = Path(__file__).resolve().parents[1] / "dashboard" / "index.html"


@app.get("/")
def employee_chat():
    return FileResponse(_DASHBOARD)
