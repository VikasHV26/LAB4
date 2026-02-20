from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from app.middleware.auth_middleware import get_current_user
from app.database import get_connection

router = APIRouter(prefix="/bloodbank", tags=["Blood Bank"])


class InventoryUpdate(BaseModel):
    blood_group: str
    units_available: int


# 🔹 Add / Update Inventory
@router.post("/inventory")
def update_inventory(
    data: InventoryUpdate,
    current_user: dict = Depends(get_current_user)
):
    if current_user["role"] != "bloodbank":
        raise HTTPException(status_code=403, detail="Only blood banks allowed")

    conn = get_connection()
    cursor = conn.cursor()

    # Check if record exists
    cursor.execute("""
        SELECT id FROM blood_inventory
        WHERE blood_bank_id = ? AND blood_group = ?
    """, (current_user["user_id"], data.blood_group))

    existing = cursor.fetchone()

    if existing:
        cursor.execute("""
            UPDATE blood_inventory
            SET units_available = ?
            WHERE blood_bank_id = ? AND blood_group = ?
        """, (
            data.units_available,
            current_user["user_id"],
            data.blood_group
        ))
    else:
        cursor.execute("""
            INSERT INTO blood_inventory
            (blood_bank_id, blood_group, units_available)
            VALUES (?, ?, ?)
        """, (
            current_user["user_id"],
            data.blood_group,
            data.units_available
        ))

    conn.commit()
    conn.close()

    return {"message": "Inventory updated successfully"}


# 🔹 View Inventory
@router.get("/inventory")
def view_inventory(current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "bloodbank":
        raise HTTPException(status_code=403, detail="Only blood banks allowed")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, blood_group, units_available
        FROM blood_inventory
        WHERE blood_bank_id = ?
    """, (current_user["user_id"],))

    rows = cursor.fetchall()
    conn.close()

    return [dict(row) for row in rows]


# 🔹 Delete Inventory
@router.delete("/inventory/{item_id}")
def delete_inventory(
    item_id: int,
    current_user: dict = Depends(get_current_user)
):
    if current_user["role"] != "bloodbank":
        raise HTTPException(status_code=403, detail="Only blood banks allowed")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM blood_inventory
        WHERE id = ? AND blood_bank_id = ?
    """, (item_id, current_user["user_id"]))

    conn.commit()
    conn.close()

    return {"message": "Inventory deleted successfully"}