from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from app.middleware.auth_middleware import get_current_user
from app.database import get_connection
from app.services.matching_service import find_matching_donors

router = APIRouter(prefix="/requests", tags=["Requests"])


class BloodRequest(BaseModel):
    blood_group: str
    units_required: int
    request_type: str  # immediate / scheduled
    scheduled_date: str | None = None
    latitude: float
    longitude: float


@router.post("/create")
def create_blood_request(
    request: BloodRequest,
    current_user: dict = Depends(get_current_user)
):
    if current_user["role"] != "patient":
        raise HTTPException(status_code=403, detail="Only patients can create requests")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO patient_requests 
        (patient_id, blood_group, units_required, request_type, scheduled_date)
        VALUES (?, ?, ?, ?, ?)
    """, (
        current_user["user_id"],
        request.blood_group,
        request.units_required,
        request.request_type,
        request.scheduled_date
    ))

    conn.commit()
    conn.close()

    # Smart Matching
    matched_donors = find_matching_donors(
        request.blood_group,
        request.latitude,
        request.longitude
    )

    return {
        "message": "Blood request created successfully",
        "matched_donors": matched_donors
    }