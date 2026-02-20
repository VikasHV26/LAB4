from app.database import get_connection


def send_notification(user_id: int, message: str, notif_type: str = "emergency"):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO notifications (user_id, message, type)
        VALUES (?, ?, ?)
    """, (user_id, message, notif_type))

    conn.commit()
    conn.close()


# Mock WhatsApp API
def send_whatsapp(phone: str, message: str):
    print(f"\n📲 WhatsApp Sent To {phone}")
    print(f"Message: {message}\n")