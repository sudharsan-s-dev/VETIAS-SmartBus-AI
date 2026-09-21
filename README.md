# 🚌 VETIAS COLLEGE BUS MANAGEMENT SYSTEM

![Version](https://img.shields.io/badge/version-3.2-blue.svg)
![Python](https://img.shields.io/badge/python-3.9+-yellow.svg)
![Flask](https://img.shields.io/badge/framework-Flask-lightgrey.svg)
![Database](https://img.shields.io/badge/database-SQLite%20%7C%20PostgreSQL-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-Active-success.svg)

A secure and intelligent transportation management platform developed for **VET Institute of Arts and Science**.
The system modernizes traditional bus attendance systems by integrating **dynamic QR authentication, GPS tracking, device binding security, and geofenced attendance verification**.

It ensures:

* Student safety
* Operational transparency
* Real-time monitoring
* Proxy-proof attendance

---

## 🎯 PROJECT OBJECTIVE

The goal of this system is to **digitize and automate student bus attendance and transport monitoring** in educational institutions.

Traditional bus attendance systems rely on **manual registers or driver memory**, which leads to:

* Human errors
* Proxy attendance
* Lack of real-time monitoring
* Poor accountability

The **VETIAS Bus Management System** solves these issues by combining **QR authentication, GPS validation, and device-level security**, ensuring accurate and secure transport management.

---

## 🏗 SYSTEM ARCHITECTURE

```
Student Mobile Browser
        │
        │ QR Scan + GPS Location
        ▼
Flask Web Server (Backend API)
        │
        │ Authentication & Validation
        ▼
Database (SQLite / PostgreSQL)
        │
        │ Data Processing
        ▼
Admin Dashboard
        │
        ▼
Driver GPS Broadcasting
```

---

## 🌟 CORE FEATURES

### 👨‍🎓 STUDENT PORTAL

| Feature                | Description                              |
| ---------------------- | ---------------------------------------- |
| 🔐 Secure Login        | Role-based authentication system         |
| 📷 QR Boarding         | Scan dynamic QR code to mark attendance  |
| 📍 Geofence Validation | Attendance allowed only near the bus     |
| 📱 Device Binding      | One account linked to one device         |
| 📜 Boarding History    | View complete boarding logs              |
| 📩 Complaint System    | Report issues directly to administration |

---

### 🚍 DRIVER MODULE

| Feature                   | Description                           |
| ------------------------- | ------------------------------------- |
| 📡 Live GPS Tracking      | Driver device broadcasts bus location |
| 👥 Passenger Manifest     | Real-time list of students on board   |
| ✅ Smart Boarding Feedback | Instant success/failure message       |
| 🚏 Geofence Alerts        | Alerts when bus reaches a stop        |
| 📊 Trip Monitoring        | Track boarding activity during trip   |

---

### 🛡 ADMIN CONSOLE

| Feature                    | Description                             |
| -------------------------- | --------------------------------------- |
| 👨‍💼 Student Management   | Add, update, or remove students         |
| 🚌 Route Management        | Assign buses and transport routes       |
| 💰 Fee Monitoring          | Track transport fee payment status      |
| 📧 Automated Notifications | SMS / Email alerts for pending payments |
| 🔒 Security Control        | Reset device bindings remotely          |
| 📊 Data Analytics          | Attendance trends and bus occupancy     |

---

## 🛠 TECHNOLOGY STACK

### Backend

* Python
* Flask Framework
* SQLAlchemy ORM

### Frontend

* HTML5
* Tailwind CSS
* JavaScript (ES6+)

### Database

* SQLite (Local Development)
* PostgreSQL (Production Ready)

### Security & Validation

* Device Fingerprinting
* SHA-256 Password Hashing
* Geofencing (Haversine Formula)

### APIs Used

* HTML5 Geolocation API
* Html5-QRCode Scanner

---

## 🔒 SECURITY INFRASTRUCTURE

The system implements a **multi-layered security architecture** to ensure reliable and tamper-proof attendance.

### 1️⃣ Device Fingerprinting

Each student account is **bound to a specific device**, preventing credential sharing.

### 2️⃣ GPS Geofencing

Attendance can only be marked if the student's device is **within 100 meters of the bus location**.

### 3️⃣ Secure Session Management

Administrative actions use **protected server-side sessions** to prevent unauthorized access.

### 4️⃣ Encrypted Credentials

User passwords are securely stored using **SHA-256 hashing**.

---

## 🔒 PRIVACY & BIOMETRIC DATA CONSENT POLICY

Enrolled students' facial embeddings (1404-dimensional landmark geometry vectors) are stored strictly for transport attendance verification matching. Raw ERP enrollment photos and flagged unrecognized-face security snapshots are stored locally and access-restricted exclusively to authorized administrators. This system is implemented as a prototype/demo platform and does not constitute a commercial biometric database. Production institutional deployment would require explicit student/parent consent and a formalized institutional data-retention policy.

---

## 🚀 QUICK START GUIDE

### 1️⃣ Prerequisites

Install the following:

* Python **3.9+**
* Pip Package Manager
* Git

---

### 2️⃣ Installation

```bash
# Clone repository
git clone https://github.com/your-username/VETIAS-Bus-System.git

# Enter project directory
cd VETIAS-Bus-System

# Create virtual environment
python -m venv .venv

# Activate environment
source .venv/bin/activate
# Windows:
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

---

### 3️⃣ Environment Setup

Create a `.env` file:

```
SECRET_KEY=your_secret_key
SMTP_EMAIL=your_email
SMTP_PASSWORD=your_password
```

---

### 4️⃣ Initialize Database

```
python init_db_manual.py
```

---

### 5️⃣ Run the Application

```
python app.py
```

Open your browser:

```
http://127.0.0.1:5000
```

---

## 📊 FUTURE ENHANCEMENTS

Possible improvements for future versions:

* 📱 Dedicated **Android / iOS mobile app**
* 🔔 **Push notifications for parents**
* 🛰 **Live bus tracking map**
* 🤖 **AI route optimization**
* 📈 **Advanced analytics dashboard**

---

## 📷 SYSTEM SCREENSHOTS

*(You can add screenshots here later)*

```
screenshots/
│
├── login_page.png
├── admin_dashboard.png
├── qr_scan_page.png
└── driver_panel.png
```

---

## 🤝 CONTRIBUTING

Contributions are welcome.

Steps:

1. Fork the repository
2. Create a new branch
3. Commit your changes
4. Push the branch
5. Submit a Pull Request

---

## 📄 LICENSE

This project is licensed under the **MIT License**.

See the `LICENSE` file for details.

---

## 👨‍💻 DEVELOPER

**Sudharsan S**
Full Stack Developer

Developed for
**VET Institute of Arts and Science – Transport Division**
