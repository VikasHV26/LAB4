from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from app.middleware.auth_middleware import get_current_user
from app.database import get_connection
from app.services.matching_service import find_matching_donors
from app.services.notification_service import send_notification, send_whatsapp

router = APIRouter(prefix="/emergency", tags=["Emergency"])


class EmergencyRequest(BaseModel):
    blood_group: str
    units_required: int
    latitude: float
    longitude: float


@router.post("/create")
def create_emergency(
    request: EmergencyRequest,
    current_user: dict = Depends(get_current_user)
):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Only hospital/admin can create emergency")

    conn = get_connection()
    cursor = conn.cursor()

    # Save emergency request
    cursor.execute("""
        INSERT INTO emergency_requests (hospital_id, blood_group, units_required, latitude, longitude)
        VALUES (?, ?, ?, ?, ?)
    """, (
        1,  # Hackathon: fixed hospital id
        request.blood_group,
        request.units_required,
        request.latitude,
        request.longitude
    ))

    emergency_id = cursor.lastrowid
    conn.commit()
    conn.close()

    # Smart matching
    matched_donors = find_matching_donors(
        request.blood_group,
        request.latitude,
        request.longitude
    )

    # Send notifications
    for donor in matched_donors:
        message = f"🚨 Emergency! {request.blood_group} blood needed urgently."
        send_notification(donor["id"], message)
        send_whatsapp(donor["phone"], message)

    return {
        "message": "Emergency created and donors notified",
        "matched_donors_count": len(matched_donors)
    }