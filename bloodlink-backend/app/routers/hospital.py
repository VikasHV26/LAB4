from fastapi import APIRouter, Depends, HTTPException
from app.middleware.auth_middleware import get_current_user
from app.database import get_connection
from app.services.whatsapp_service import send_emergency_whatsapp_alert
router = APIRouter(prefix="/hospital", tags=["Hospital"])


@router.get("/requests")
def get_all_requests(current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "hospital":
        raise HTTPException(status_code=403, detail="Only hospitals allowed")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT pr.id,
               u.name as patient_name,
               pr.blood_group,
               pr.units_required,
               pr.request_type,
               pr.status,
               pr.created_at
        FROM patient_requests pr
        JOIN users u ON pr.patient_id = u.id
        ORDER BY pr.created_at DESC
    """)

    rows = cursor.fetchall()
    conn.close()

    return [dict(row) for row in rows]



@router.put("/requests/{request_id}")
def update_request_status(
    request_id: int,
    status: str,
    current_user: dict = Depends(get_current_user)
):
    if current_user["role"] != "hospital":
        raise HTTPException(status_code=403, detail="Only hospitals allowed")

    conn = get_connection()
    cursor = conn.cursor()

    # Get request details
    cursor.execute("""
        SELECT blood_group, units_required
        FROM patient_requests
        WHERE id = ?
    """, (request_id,))

    request = cursor.fetchone()

    if not request:
        raise HTTPException(status_code=404, detail="Request not found")

    blood_group = request["blood_group"]
    units_required = request["units_required"]

    # Check inventory
    cursor.execute("""
        SELECT id, units_available
        FROM blood_inventory
        WHERE blood_group = ?
        ORDER BY units_available DESC
    """, (blood_group,))

    inventory = cursor.fetchone()

    # ❌ If NO inventory OR insufficient
    if not inventory or inventory["units_available"] < units_required:

        # 🔥 Find donors with same blood group
        cursor.execute("""
            SELECT name, phone, city
            FROM users
            WHERE blood_group = ?
            AND role = 'patient'
        """, (blood_group,))

        donors = cursor.fetchall()

        # 📲 Send WhatsApp alerts
        for donor in donors:
            send_emergency_whatsapp_alert(
                donor_phone=donor["phone"],
                donor_name=donor["name"],
                blood_group=blood_group,
                hospital_name="Emergency Hospital",
                distance="Nearby"
            )

        conn.close()

        return {
            "message": "No stock available. WhatsApp alerts sent to matching donors."
        }

    # ✅ If inventory is available
    new_units = inventory["units_available"] - units_required

    cursor.execute("""
        UPDATE blood_inventory
        SET units_available = ?
        WHERE id = ?
    """, (new_units, inventory["id"]))

    cursor.execute("""
        UPDATE patient_requests
        SET status = ?
        WHERE id = ?
    """, (status, request_id))

    conn.commit()
    conn.close()

    return {
        "message": "Request approved & inventory updated",
        "remaining_units": new_units
    }