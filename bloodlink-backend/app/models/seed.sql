INSERT INTO users (google_id, role, name, age, email, blood_group, city, latitude, longitude)
VALUES 
('g1','donor','Rahul',25,'rahul@mail.com','O+','Bangalore',12.9716,77.5946),
('g2','donor','Amit',28,'amit@mail.com','A+','Bangalore',12.9616,77.5846),
('g3','patient','Riya',18,'riya@mail.com','B+','Bangalore',12.9516,77.5746);

INSERT INTO hospitals (name, license_number, city, latitude, longitude)
VALUES ('City Care Hospital','LIC123','Bangalore',12.9710,77.6000);

INSERT INTO blood_banks (name, government_id, city, latitude, longitude)
VALUES ('LifeSaver Blood Bank','GOV456','Bangalore',12.9720,77.5900);

INSERT INTO blood_inventory (blood_bank_id, blood_group, units_available, expiry_date)
VALUES (1,'O+',10,'2026-12-31'),
       (1,'A+',5,'2026-12-31');