PRAGMA foreign_keys = ON;

-- =========================
-- USERS TABLE
-- =========================
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    google_id TEXT UNIQUE NOT NULL,
    role TEXT CHECK(role IN ('patient','hospital','bloodbank')) NOT NULL,
    name TEXT NOT NULL,
    age INTEGER,
    email TEXT UNIQUE NOT NULL,
    phone TEXT,
    blood_group TEXT,
    city TEXT,
    pincode TEXT,
    latitude REAL,
    longitude REAL,
    is_available BOOLEAN DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- =========================
-- HOSPITALS TABLE
-- =========================
CREATE TABLE IF NOT EXISTS hospitals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    license_number TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE,
    phone TEXT,
    city TEXT,
    latitude REAL,
    longitude REAL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- =========================
-- BLOOD BANKS TABLE
-- =========================
CREATE TABLE IF NOT EXISTS blood_banks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    government_id TEXT UNIQUE NOT NULL,
    certification_path TEXT,
    email TEXT UNIQUE,
    phone TEXT,
    city TEXT,
    latitude REAL,
    longitude REAL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- =========================
-- BLOOD INVENTORY TABLE
-- =========================
CREATE TABLE IF NOT EXISTS blood_inventory (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    blood_bank_id INTEGER NOT NULL,
    blood_group TEXT NOT NULL,
    units_available INTEGER DEFAULT 0,
    expiry_date DATE,
    FOREIGN KEY (blood_bank_id) REFERENCES blood_banks(id) ON DELETE CASCADE
);

-- =========================
-- PATIENT REQUESTS
-- =========================
CREATE TABLE IF NOT EXISTS patient_requests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER NOT NULL,
    hospital_id INTEGER,
    blood_group TEXT NOT NULL,
    units_required INTEGER NOT NULL,
    request_type TEXT CHECK(request_type IN ('immediate','scheduled')) NOT NULL,
    scheduled_date DATE,
    status TEXT DEFAULT 'pending',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (patient_id) REFERENCES users(id),
    FOREIGN KEY (hospital_id) REFERENCES hospitals(id)
);

-- =========================
-- EMERGENCY REQUESTS
-- =========================
CREATE TABLE IF NOT EXISTS emergency_requests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    hospital_id INTEGER NOT NULL,
    blood_group TEXT NOT NULL,
    units_required INTEGER NOT NULL,
    latitude REAL,
    longitude REAL,
    status TEXT DEFAULT 'active',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (hospital_id) REFERENCES hospitals(id)
);

-- =========================
-- NOTIFICATIONS
-- =========================
CREATE TABLE IF NOT EXISTS notifications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    message TEXT,
    type TEXT,
    is_read BOOLEAN DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- =========================
-- INDEXES (MUST BE LAST)
-- =========================

CREATE INDEX IF NOT EXISTS idx_users_blood_group ON users(blood_group);
CREATE INDEX IF NOT EXISTS idx_users_location ON users(latitude, longitude);
CREATE INDEX IF NOT EXISTS idx_inventory_group ON blood_inventory(blood_group);