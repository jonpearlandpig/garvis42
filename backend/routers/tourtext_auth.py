"""
TourText Emergent — Authentication
Email/password signup and login with JWT bearer tokens.

Collections: tt_users, tt_user_sessions
"""
import logging
import os
from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr

from ..tourtext_utils import generate_uuid

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/tourtext/auth", tags=["TourText Auth"])

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
_SECRET = os.environ.get("TOURTEXT_JWT_SECRET", "tourtext-dev-secret-change-in-prod")
_ALGORITHM = "HS256"
_TOKEN_EXPIRE_DAYS = 30

pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")
bearer_scheme = HTTPBearer(auto_error=False)


# ---------------------------------------------------------------------------
# DB — shared via lazy import to avoid circular deps at module load time
# ---------------------------------------------------------------------------
def _db():
    from .tourtext import tt_db
    return tt_db


# ---------------------------------------------------------------------------
# Pydantic models
# ---------------------------------------------------------------------------
class SignupRequest(BaseModel):
    email: EmailStr
    password: str
    name: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class AuthResponse(BaseModel):
    token: str
    user_id: str
    email: str
    name: str


# ---------------------------------------------------------------------------
# JWT helpers
# ---------------------------------------------------------------------------
def _create_token(user_id: str, email: str) -> str:
    expires = datetime.now(timezone.utc) + timedelta(days=_TOKEN_EXPIRE_DAYS)
    return jwt.encode(
        {"sub": user_id, "email": email, "exp": expires},
        _SECRET,
        algorithm=_ALGORITHM,
    )


def _decode_token(token: str) -> dict:
    return jwt.decode(token, _SECRET, algorithms=[_ALGORITHM])


# ---------------------------------------------------------------------------
# Auth dependency — use in protected TourText routes
# ---------------------------------------------------------------------------
async def require_tt_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(bearer_scheme),
) -> dict:
    if not credentials:
        raise HTTPException(status_code=401, detail="Bearer token required")
    try:
        payload = _decode_token(credentials.credentials)
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    user = await _db().tt_users.find_one({"user_id": payload["sub"]}, {"_id": 0, "password_hash": 0})
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------
@router.post("/signup", response_model=AuthResponse, status_code=201)
async def signup(payload: SignupRequest):
    db = _db()
    existing = await db.tt_users.find_one({"email": payload.email.lower()})
    if existing:
        raise HTTPException(status_code=409, detail="Email already registered")

    user_id = generate_uuid()
    now = datetime.now(timezone.utc).isoformat()
    doc = {
        "user_id": user_id,
        "email": payload.email.lower(),
        "name": payload.name,
        "password_hash": pwd_ctx.hash(payload.password),
        "created_at": now,
    }
    await db.tt_users.insert_one(doc)

    token = _create_token(user_id, payload.email.lower())
    return AuthResponse(token=token, user_id=user_id, email=payload.email.lower(), name=payload.name)


@router.post("/login", response_model=AuthResponse)
async def login(payload: LoginRequest):
    db = _db()
    user = await db.tt_users.find_one({"email": payload.email.lower()})
    if not user or not pwd_ctx.verify(payload.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = _create_token(user["user_id"], user["email"])
    return AuthResponse(
        token=token,
        user_id=user["user_id"],
        email=user["email"],
        name=user["name"],
    )


@router.get("/me")
async def me(current_user: dict = Depends(require_tt_user)):
    return current_user
