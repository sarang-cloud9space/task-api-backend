
import os
from datetime import datetime, timedelta, timezone

import jwt
from dotenv import load_dotenv
from pathlib import Path

# Load settings from day-08/.env
env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(env_path)

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")

if not JWT_SECRET_KEY:
    raise ValueError("JWT_SECRET_KEY is missing from day-08/.env")

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(subject: str) -> str:
    """Create a signed JWT with an expiration time."""
    now = datetime.now(timezone.utc)

    payload = {
        "sub": subject,
        "iat": now,
        "exp": now + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    }

    return jwt.encode(payload, JWT_SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str) -> dict:
    """Verify a JWT's signature and expiration, then return its claims."""
    return jwt.decode(
        token,
        JWT_SECRET_KEY,
        algorithms=[ALGORITHM],
    )
