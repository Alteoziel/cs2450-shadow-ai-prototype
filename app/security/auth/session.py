import hashlib
import hmac
import os

from fastapi import Request


def admin_password() -> str:
    return os.getenv("ADMIN_PASSWORD") or ""


def _signature(value: str) -> str:
    return hmac.new(admin_password().encode(), value.encode(), hashlib.sha256).hexdigest()


def admin_cookie() -> str:
    return f"ok.{_signature('ok')}"


def is_admin(request: Request) -> bool:
    if not admin_password():
        return False
    cookie = request.cookies.get("shadow_admin") or ""
    return hmac.compare_digest(cookie, admin_cookie())


def password_matches(password: str) -> bool:
    expected = admin_password()
    if not expected:
        return False
    return hmac.compare_digest(password, expected)
