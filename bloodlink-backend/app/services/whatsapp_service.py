import os
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_WHATSAPP_NUMBER = os.getenv("TWILIO_WHATSAPP_NUMBER")


def send_emergency_whatsapp_alert(
    donor_phone,
    donor_name,
    blood_group,
    hospital_name,
    distance
):
    try:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

        formatted_phone = f"whatsapp:{donor_phone}"

        message_body = (
            f"🚨 BLOODLINK EMERGENCY ALERT 🚨\n\n"
            f"Hello {donor_name},\n"
            f"Urgent {blood_group} blood needed!\n\n"
            f"🏥 Hospital: {hospital_name}\n"
            f"📍 Distance: {distance} km\n\n"
            f"Open BloodLink App immediately."
        )

        message = client.messages.create(
            from_=TWILIO_WHATSAPP_NUMBER,
            body=message_body,
            to=formatted_phone
        )

        return True

    except Exception as e:
        print("WhatsApp Error:", e)
        return False