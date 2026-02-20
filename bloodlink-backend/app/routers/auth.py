from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from datetime import datetime, timedelta
from jose import jwt
from app.database import get_connection

SECRET_KEY = "bloodlink_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

router = APIRouter(prefix="/auth", tags=["Auth"])

# -----------------------------
# Request Models
# -----------------------------

class GoogleLogin(BaseModel):
    google_id: str
    name: str
    email: str
    role: str  # donor / patient


# -----------------------------
# Create JWT Token
# -----------------------------

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# -----------------------------
# Google Login (Hackathon Mock)
# -----------------------------

@router.post("/google-login")
def google_login(payload: GoogleLogin):
    conn = get_connection()
    cursor = conn.cursor()

    # Check if user already exists by google_id OR email
    cursor.execute(
        "SELECT * FROM users WHERE google_id = ? OR email = ?",
        (payload.google_id, payload.email)
    )
    user = cursor.fetchone()

    if not user:
        cursor.execute("""
            INSERT INTO users (google_id, role, name, email, blood_group, city)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            payload.google_id,
            payload.role,
            payload.name,
            payload.email,
            "O+",   # default
            "Unknown"
        ))
        conn.commit()

        cursor.execute(
            "SELECT * FROM users WHERE google_id = ?",
            (payload.google_id,)
        )
        user = cursor.fetchone()

    token = create_access_token({
        "user_id": user["id"],
        "role": user["role"]
    })

    conn.close()

    return {
        "access_token": token,
        "token_type": "bearer",
        "role": user["role"]
    }