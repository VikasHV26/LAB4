from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from app.database import get_connection
from pathlib import Path
from app.routers import admin
from app.routers import patient
from app.routers import bloodbank
from app.routers import auth, users, requests, emergency, hospital
app = FastAPI(title="BloodLink API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(requests.router)
app.include_router(emergency.router)
app.include_router(hospital.router)
app.include_router(bloodbank.router)
app.include_router(patient.router)
app.include_router(admin.router)
@app.on_event("startup")
def startup():
    conn = get_connection()
    cursor = conn.cursor()

    schema_path = Path("app/models/schema.sql")
    with open(schema_path, "r") as f:
        cursor.executescript(f.read())

    seed_path = Path("app/models/seed.sql")
    # with open(seed_path, "r") as f:
    #     cursor.executescript(f.read())

    conn.commit()
    conn.close()

@app.get("/")
def root():
    return {"message": "BloodLink API Running"}