from fastapi import APIRouter, Depends, HTTPException
from app.middleware.auth_middleware import get_current_user
from app.database import get_connection

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.get("/stats")
def get_admin_stats(current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Only admin allowed")

    conn = get_connection()
    cursor = conn.cursor()

    stats = {}

    cursor.execute("SELECT COUNT(*) FROM users WHERE role='patient'")
    stats["total_patients"] = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM hospitals")
    stats["total_hospitals"] = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM blood_banks")
    stats["total_bloodbanks"] = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM patient_requests")
    stats["total_requests"] = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM patient_requests WHERE status='pending'")
    stats["pending_requests"] = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM patient_requests WHERE status='approved'")
    stats["approved_requests"] = cursor.fetchone()[0]

    conn.close()

    return stats