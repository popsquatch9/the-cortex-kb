from __future__ import annotations

import os
import time
from functools import lru_cache
from typing import Any

import requests
from authlib.integrations.starlette_client import OAuth
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware

from cortex import Cortex

APP_TITLE = "The Cortex Dashboard"
GHOSTLINE_BASE_URL = os.getenv("GHOSTLINE_BASE_URL", "http://ghostline.boo")
EMAIL_DOMAIN = "ghostline.boo"
DASHBOARD_PASSWORD = os.getenv("CORTEX_DASHBOARD_PASSWORD", "")
SECRET_KEY = os.getenv("CORTEX_DASH_SECRET", "dev-secret-change-me")
SESSION_HTTPS_ONLY = os.getenv("CORTEX_DASH_HTTPS_ONLY", "false").lower() in {"1", "true", "yes"}
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID", "")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET", "")
GOOGLE_REDIRECT_URI = os.getenv("CORTEX_OAUTH_REDIRECT_URI", "")
SSO_STRICT_MODE = os.getenv("CORTEX_SSO_STRICT", "false").lower() in {"1", "true", "yes"}

app = FastAPI(title=APP_TITLE)
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY, https_only=SESSION_HTTPS_ONLY)
app.mount("/static", StaticFiles(directory="web/static"), name="static")
templates = Jinja2Templates(directory="web/templates")

oauth = None
if GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET:
    oauth = OAuth()
    oauth.register(
        name="google",
        client_id=GOOGLE_CLIENT_ID,
        client_secret=GOOGLE_CLIENT_SECRET,
        server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
        client_kwargs={"scope": "openid email profile"},
    )

if SSO_STRICT_MODE and oauth is None:
    raise RuntimeError(
        "CORTEX_SSO_STRICT=true requires GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET. "
        "Dashboard startup aborted due to auth misconfiguration."
    )


@lru_cache(maxsize=1)
def get_cortex() -> Cortex:
    return Cortex()


def is_allowed_email(email: str) -> bool:
    email = (email or "").strip().lower()
    return email.endswith(f"@{EMAIL_DOMAIN}") and len(email.split("@")[0]) > 0


def is_authenticated(request: Request) -> bool:
    email = request.session.get("email", "")
    return is_allowed_email(email)


def oauth_enabled() -> bool:
    return oauth is not None


def local_login_enabled() -> bool:
    return not (SSO_STRICT_MODE and oauth_enabled())


def sso_misconfigured() -> bool:
    return SSO_STRICT_MODE and not oauth_enabled()


def ping_ghostline(base_url: str = GHOSTLINE_BASE_URL) -> dict[str, Any]:
    started = time.perf_counter()
    try:
        resp = requests.get(base_url, timeout=5)
        elapsed_ms = round((time.perf_counter() - started) * 1000, 1)
        return {
            "ok": 200 <= resp.status_code < 500,
            "status_code": resp.status_code,
            "latency_ms": elapsed_ms,
            "base_url": base_url,
        }
    except Exception as exc:
        elapsed_ms = round((time.perf_counter() - started) * 1000, 1)
        return {
            "ok": False,
            "status_code": None,
            "latency_ms": elapsed_ms,
            "base_url": base_url,
            "error": str(exc),
        }


def require_auth(request: Request):
    if not is_authenticated(request):
        return RedirectResponse(url="/login", status_code=303)
    return None


@app.get("/", response_class=HTMLResponse)
def dashboard(request: Request, q: str = ""):
    denied = require_auth(request)
    if denied:
        return denied

    cortex = get_cortex()
    stats = cortex.get_stats()
    tag_map = cortex.get_tags()
    top_tags = list(tag_map.items())[:16]

    results = []
    if q.strip():
        results = cortex.search(q.strip(), top_k=10)

    recent_rows = cortex.db.execute(
        "SELECT id, title, quality, created_at, source_type FROM entries ORDER BY created_at DESC LIMIT 12"
    ).fetchall()
    recent_entries = [dict(r) for r in recent_rows]

    ghostline_status = ping_ghostline()

    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "email": request.session.get("email"),
            "stats": stats,
            "top_tags": top_tags,
            "results": results,
            "q": q,
            "recent_entries": recent_entries,
            "ghostline": ghostline_status,
        },
    )


@app.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    if is_authenticated(request):
        return RedirectResponse(url="/", status_code=303)
    return templates.TemplateResponse(
        "login.html",
        {
            "request": request,
            "error": "",
            "ghostline_base_url": GHOSTLINE_BASE_URL,
            "email_domain": EMAIL_DOMAIN,
            "oauth_enabled": oauth_enabled(),
            "local_login_enabled": local_login_enabled(),
            "sso_misconfigured": sso_misconfigured(),
        },
    )


@app.post("/login", response_class=HTMLResponse)
def login_submit(request: Request, email: str = Form(...), password: str = Form("")):
    if not local_login_enabled():
        return templates.TemplateResponse(
            "login.html",
            {
                "request": request,
                "error": "Local login is disabled. Use Google SSO.",
                "ghostline_base_url": GHOSTLINE_BASE_URL,
                "email_domain": EMAIL_DOMAIN,
                "oauth_enabled": oauth_enabled(),
                "local_login_enabled": local_login_enabled(),
                "sso_misconfigured": sso_misconfigured(),
            },
            status_code=403,
        )

    if not is_allowed_email(email):
        return templates.TemplateResponse(
            "login.html",
            {
                "request": request,
                "error": f"Access restricted to @{EMAIL_DOMAIN} email addresses.",
                "ghostline_base_url": GHOSTLINE_BASE_URL,
                "email_domain": EMAIL_DOMAIN,
                "oauth_enabled": oauth_enabled(),
                "local_login_enabled": local_login_enabled(),
                "sso_misconfigured": sso_misconfigured(),
            },
            status_code=403,
        )

    if DASHBOARD_PASSWORD and password != DASHBOARD_PASSWORD:
        return templates.TemplateResponse(
            "login.html",
            {
                "request": request,
                "error": "Invalid dashboard password.",
                "ghostline_base_url": GHOSTLINE_BASE_URL,
                "email_domain": EMAIL_DOMAIN,
                "oauth_enabled": oauth_enabled(),
                "local_login_enabled": local_login_enabled(),
                "sso_misconfigured": sso_misconfigured(),
            },
            status_code=403,
        )

    request.session["email"] = email.strip().lower()
    request.session["auth_provider"] = "password"
    return RedirectResponse(url="/", status_code=303)


@app.get("/auth/google/login")
async def auth_google_login(request: Request):
    if not oauth_enabled():
        return RedirectResponse(url="/login", status_code=303)

    redirect_uri = GOOGLE_REDIRECT_URI or str(request.url_for("auth_google_callback"))
    return await oauth.google.authorize_redirect(request, redirect_uri)


@app.get("/auth/google/callback")
async def auth_google_callback(request: Request):
    if not oauth_enabled():
        return RedirectResponse(url="/login", status_code=303)

    try:
        token = await oauth.google.authorize_access_token(request)
        userinfo = token.get("userinfo")
        if not userinfo:
            userinfo = await oauth.google.userinfo(token=token)
    except Exception:
        return templates.TemplateResponse(
            "login.html",
            {
                "request": request,
                "error": "Google sign-in failed. Please try again.",
                "ghostline_base_url": GHOSTLINE_BASE_URL,
                "email_domain": EMAIL_DOMAIN,
                "oauth_enabled": oauth_enabled(),
                "local_login_enabled": local_login_enabled(),
                "sso_misconfigured": sso_misconfigured(),
            },
            status_code=403,
        )

    email = (userinfo.get("email") or "").strip().lower()
    email_verified = bool(userinfo.get("email_verified"))

    if not email_verified or not is_allowed_email(email):
        return templates.TemplateResponse(
            "login.html",
            {
                "request": request,
                "error": f"Access requires a verified @{EMAIL_DOMAIN} Google account.",
                "ghostline_base_url": GHOSTLINE_BASE_URL,
                "email_domain": EMAIL_DOMAIN,
                "oauth_enabled": oauth_enabled(),
                "local_login_enabled": local_login_enabled(),
                "sso_misconfigured": sso_misconfigured(),
            },
            status_code=403,
        )

    request.session["email"] = email
    request.session["auth_provider"] = "google"
    return RedirectResponse(url="/", status_code=303)


@app.post("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/login", status_code=303)


@app.get("/api/ghostline/ping")
def ghostline_ping(request: Request):
    denied = require_auth(request)
    if denied:
        return {"ok": False, "error": "unauthorized"}
    return ping_ghostline()


@app.get("/api/stats")
def api_stats(request: Request):
    denied = require_auth(request)
    if denied:
        return {"ok": False, "error": "unauthorized"}
    return get_cortex().get_stats()


if __name__ == "__main__":
    import 
uvicorn

    uvicorn.run("dashboard:app", host="0.0.0.0", port=8787, reload=True)
