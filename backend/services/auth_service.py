from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext

# In production, load SECRET_KEY from environment variable
SECRET_KEY = "visioniq-secret-key-change-in-production-2024"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 480  # 8 hours

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

# ---------------------------------------------------------------------------
# In-memory user store (replace with DB in Sprint 4)
# ---------------------------------------------------------------------------
# Passwords are bcrypt hashes — generate with: pwd_context.hash("password")
_USERS = {
    "admin": {
        "username": "admin",
        "full_name": "VisionIQ Admin",
        "email": "admin@visioniq.com",
        "hashed_password": pwd_context.hash("admin123"),
        "role": "Admin",
        "disabled": False,
    },
    "manager": {
        "username": "manager",
        "full_name": "Plant Manager",
        "email": "manager@visioniq.com",
        "hashed_password": pwd_context.hash("manager123"),
        "role": "Manager",
        "disabled": False,
    },
    "planner": {
        "username": "planner",
        "full_name": "Maintenance Planner",
        "email": "planner@visioniq.com",
        "hashed_password": pwd_context.hash("planner123"),
        "role": "Planner",
        "disabled": False,
    },
    "technician": {
        "username": "technician",
        "full_name": "Field Technician",
        "email": "tech@visioniq.com",
        "hashed_password": pwd_context.hash("tech123"),
        "role": "Technician",
        "disabled": False,
    },
    "executive": {
        "username": "executive",
        "full_name": "Executive",
        "email": "exec@visioniq.com",
        "hashed_password": pwd_context.hash("exec123"),
        "role": "Executive",
        "disabled": False,
    },
}

# Role → pages/features they can access
ROLE_PERMISSIONS = {
    "Admin":      ["dashboard", "reliability", "executive", "predictive", "ai", "settings", "upload", "users"],
    "Manager":    ["dashboard", "reliability", "executive", "predictive", "ai"],
    "Planner":    ["dashboard", "reliability", "upload"],
    "Technician": ["dashboard"],
    "Executive":  ["dashboard", "executive", "ai"],
}


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


def get_user(username: str) -> Optional[dict]:
    return _USERS.get(username)


def authenticate_user(username: str, password: str) -> Optional[dict]:
    user = get_user(username)
    if not user or user["disabled"]:
        return None
    if not verify_password(password, user["hashed_password"]):
        return None
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str) -> Optional[dict]:
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        return None
