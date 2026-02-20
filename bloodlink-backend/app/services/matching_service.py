import math
from app.database import get_connection

# -----------------------------
# Haversine Formula
# -----------------------------
def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371  # Earth radius in KM

    d_lat = math.radians(lat2 - lat1)
    d_lon = math.radians(lon2 - lon1)

    a = (
        math.sin(d_lat / 2) ** 2
        + math.cos(math.radians(lat1))
        * math.cos(math.radians(lat2))
        * math.sin(d_lon / 2) ** 2
    )

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


# -----------------------------
# Smart Matching Logic
# -----------------------------
def find_matching_donors(blood_group, patient_lat, patient_lon):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, name, phone, blood_group, latitude, longitude
        FROM users
        WHERE role = 'donor'
        AND blood_group = ?
        AND is_available = 1
    """, (blood_group,))

    donors = cursor.fetchall()
    conn.close()

    matched = []

    for donor in donors:
        if donor["latitude"] and donor["longitude"]:
            distance = calculate_distance(
                patient_lat,
                patient_lon,
                donor["latitude"],
                donor["longitude"]
            )

            if distance <= 150:
                matched.append({
                    "id": donor["id"],
                    "name": donor["name"],
                    "phone": donor["phone"],
                    "distance_km": round(distance, 2)
                })

    # Sort by nearest distance
    matched.sort(key=lambda x: x["distance_km"])

    return matched[:10]  # return top 10 nearest donors