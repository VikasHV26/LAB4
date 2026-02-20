from fastapi import APIRouter, Depends, HTTPException
from app.middleware.auth_middleware import get_current_user
from app.database import get_connection

router = APIRouter(prefix="/patient", tags=["Patient"])


@router.get("/requests")
def get_my_requests(current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "patient":
        raise HTTPException(status_code=403, detail="Only patients allowed")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id,
               blood_group,
               units_required,
               request_type,
               status,
               created_at
        FROM patient_requests
        WHERE patient_id = ?
        ORDER BY created_at DESC
    """, (current_user["user_id"],))

    rows = cursor.fetchall()
    conn.close()

    return [dict(row) for row in rows]