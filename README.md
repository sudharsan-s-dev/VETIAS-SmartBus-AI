# 🚌 VETIAS COLLEGE BUS MANAGEMENT SYSTEM & AI FLEET PLATFORM

![Version](https://img.shields.io/badge/version-3.2-blue.svg)
![Python](https://img.shields.io/badge/python-3.9+-yellow.svg)
![Flask](https://img.shields.io/badge/framework-Flask-lightgrey.svg)
![Database](https://img.shields.io/badge/database-SQLite%20%7C%20PostgreSQL-blue.svg)
![AI Vision](https://img.shields.io/badge/vision-MediaPipe%20%7C%20ONNX-orange.svg)
![Maps](https://img.shields.io/badge/maps-Leaflet.js-green.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-Active-success.svg)

An enterprise-grade, multi-portal transportation management and fleet intelligence platform developed for **VET Institute of Arts and Science**. The platform modernizes institutional bus operations by combining **Dual-Mode Attendance Authentication** (Dynamic QR Codes with Haversine GPS Geofencing and Face AI Recognition), **Hardware Device Binding**, **Live GPS Fleet Map Tracking (Leaflet.js)**, **Real-Time Occupancy Gauges**, **Per-Bus Admin Drill-Down Operations**, **Gated Staff Registration**, and **Automated Parent Email Notifications**.

---

## 🏗 SYSTEM ARCHITECTURE

```
                      ┌─────────────────────────────────────────┐
                      │    VETIAS SmartBus AI Platform (V3.2)   │
                      └────────────────────┬────────────────────┘
                                           │
         ┌──────────────────┬──────────────┴───────┬──────────────────┐
         ▼                  ▼                     ▼                  ▼
  👨‍🎓 Student Portal    🚍 Driver Portal     🛡 Admin Portal    🤖 IoT Kiosk
  (QR Scan & GPS)     (Live GPS & QR)     (Fleet Control)    (Face AI Cam)
         │                  │                     │                  │
         └──────────────────┴──────────────┬──────┴──────────────────┘
                                           ▼
                            ┌─────────────────────────────┐
                            │    Flask API Server Core    │
                            ├─────────────────────────────┤
                            │ • MediaPipe + ONNX Face AI  │
                            │ • Haversine Geofence Engine │
                            │ • Device Binding Security   │
                            │ • Async SMTP Email Worker   │
                            │ • Multi-Bus Sim Engine      │
                            └──────────────┬──────────────┘
                                           ▼
                            ┌─────────────────────────────┐
                            │   Database (SQLite / PG)    │
                            └─────────────────────────────┘
```

---

## 🌟 CORE FEATURES BY PORTAL

### 👨‍🎓 1. Student Portal (`/student`, `/login`, `/register`)
* **Role-Based Authentication**: Secure registration, Werkzeug PBKDF2-SHA256 password hashing, and session protection.
* **Dynamic QR Boarding**: Scan auto-refreshing QR codes displayed on driver devices or kiosk screens to mark attendance.
* **Geofenced GPS Proximity Verification**: Enforces a configurable 100-meter Haversine distance check between student mobile GPS and live bus coordinates during QR scanning.
* **Hardware Device Binding**: Automatically binds each student account to a unique browser/device fingerprint (`device_id`), preventing proxy attendance and account sharing.
* **Boarding History**: Complete personal log showing date, timestamp, bus route, and verification method.
* **Support & Complaints System**: Direct feedback interface to log transport grievances with administration.

---

### 🚍 2. Driver Module (`/driver`)
* **Driver Command Dashboard**: Route overview, assigned vehicle status, and live trip status.
* **Live GPS Broadcasting**: Driver device broadcasts real-time GPS coordinates to server cache and database.
* **Interactive Dynamic QR Generator**: Generates dynamic boarding QR codes with auto-refreshing security tokens.
* **Passenger Manifest**: Real-time manifest updating immediately as students board the bus.
* **Trip Reset / Empty Bus Protocol**: One-click counter reset at the start of new route legs.

---

### 🛡 3. Admin Control Portal (`/admin`)
* **Executive Summary Dashboard**: Real-time system cards for student enrollment, daily check-ins, bus occupancy, and open feedback alerts.
* **Fleet Operations Command Center (`Fleet Operations` Tab)**:
  * **Live Fleet GPS Map**: Interactive Leaflet.js map tracking all active fleet buses (`Bus-10`, `Bus-06`, `Bus-01`) moving smoothly along interpolated route waypoints, complete with route-matching badge colors and custom stop markers.
  * **GPS Simulation Engine Controls**: Start/pause multi-bus GPS route movement with 1.9s linear CSS position transitions.
  * **Active Fleet Buses Grid**: Clickable bus selector cards with live progress bars (`X / 40 seats`) and status badges.
  * **Per-Bus Inspection Panel**: Assigned driver profile, single-bus Leaflet route map, bus-filtered today's boardings table, and bus-filtered security alert logs.
* **Student Registry Management**: Searchable registry table, fee payment status toggles, remote device binding resets, and account deletion.
* **Face AI Vector Enrollment**: Enroll student face vectors directly via webcam capture or official ERP passport photo upload.

---

### 🤖 4. IoT Entrance Kiosk Simulator (`/kiosk`)
* **Single-Screen Bus Entrance Kiosk**: Designed for mounted tablet/camera hardware at bus entry doors.
* **Live Face AI Recognition**: Continuously inspects video frames using MediaPipe Tasks FaceLandmarker.
* **512-D Deep Feature Embedding**: Performs 5-point affine facial alignment and extracts deep feature vectors via InsightFace MobileFaceNet ONNX runtime.
* **Liveness Blink Verification**: Computes Eye Aspect Ratio (EAR) across frame sequences to require a live human eye blink before approving boarding, preventing static photo proxy attacks.
* **Visual & Audio Feedback**: Real-time passenger count, percentage fill bar, status indicator (Available / Filling Up / Full), and chime audio feedback.

---

### 🔑 5. Gated Staff Registration (`/register/driver`, `/register/admin`)
* **Staff Passcode Security Gate**: Hidden link at the bottom of the student registration page triggers a passcode verification modal requiring environment-configured authorization codes (`DRIVER_REGISTER_CODE` / `ADMIN_REGISTER_CODE`).
* **Driver Sign-Up (`/register/driver`)**: Collects Full Name, Phone, Employee ID, Assigned Bus Route, and Password.
* **Admin Sign-Up (`/register/admin`)**: Collects Full Name, Official Email Address, and Password.

---

### ✉️ 6. Parent Email Notification Layer
* **Asynchronous Email Dispatch**: Background worker sends HTML email confirmations via Python `smtplib` to parent email addresses upon verified boarding.

---

## 🛠 TECHNOLOGY STACK

### Backend Core
* **Python 3.9+**
* **Flask Framework**
* **Flask-SQLAlchemy** (ORM & Database Layer)
* **Flask-Session** (Filesystem session management)
* **Werkzeug** (Security & Password Hashing)
* **Gunicorn** (Production WSGI Server)

### AI Vision & Biometrics
* **MediaPipe Tasks / FaceMesh**: 478-point 3D facial landmark detection, bounding box extraction, and EAR blink calculation.
* **ONNX Runtime (`mobilefacenet.onnx`)**: InsightFace MobileFaceNet model for 512-dimensional L2-normalized deep face embeddings.
* **OpenCV (`opencv-python`) & NumPy**: Image decoding, BGR-to-RGB conversion, 5-point affine alignment, frame analysis, and alert snapshot generation.

### Frontend & Mapping
* **HTML5 & Tailwind CSS**
* **JavaScript (ES6+)**
* **Leaflet.js (CDN)**: OpenStreetMap tile rendering for multi-bus fleet maps and single-bus route drill-downs.
* **Custom DivIcons**: Dynamic CSS badge pills (`.map-badge-pill`, `.custom-bus-icon`) with 1.9s linear CSS position transitions.

### Security & Utilities
* **Haversine Formula**: Mathematical great-circle distance calculation for student-vs-bus proximity.
* **PyQRCode & Pillow**: Dynamic QR code generation.
* **python-dotenv**: Environment configuration management.

---

## 🔒 SECURITY & PRIVACY ARCHITECTURE

1. **Hardware Device Fingerprinting**: Each student account is bound to a single device ID (`device_id`). Device resets require administrator override.
2. **GPS Geofence Validation**: QR scanning enforces a 100-meter proximity limit between the student device and the live bus position.
3. **Liveness Blink Check**: Face AI recognition requires active eye blinking (EAR detection) to prevent spoofing with static photos.
4. **Biometric Privacy Consent Policy**: Facial embedding vectors (512-D float arrays) are stored strictly for transport attendance matching. Raw enrollment photos and unrecognized security snapshots are access-restricted to authorized administrators.

---

## 🚀 QUICK START GUIDE

### 1️⃣ Prerequisites
* Python **3.9+**
* Pip Package Manager
* Git

---

### 2️⃣ Installation

```bash
# Clone repository
git clone https://github.com/sudharsan-s-dev/VETIAS-SmartBus-AI.git

# Enter project directory
cd VETIAS-SmartBus-AI

# Create virtual environment
python -m venv .venv

# Activate environment
# On Windows:
.venv\Scripts\activate
# On Linux/macOS:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

---

### 3️⃣ Environment Setup

Create a `.env` file in the root project directory:

```ini
# Flask Core Configuration
SECRET_KEY=your_random_secret_key_here
FLASK_DEBUG=False
PORT=5000

# Security & Geofence Settings
SKIP_DEVICE_CHECK=False
GEOFENCE_LIMIT=100

# SMTP Parent Email Notification Service
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_institution_email@gmail.com
SMTP_PASSWORD=your_app_specific_password_here
EMAIL_MODE=True

# Staff Portal Passcode Access Gate (Required)
DRIVER_REGISTER_CODE=your_secret_driver_code_here
ADMIN_REGISTER_CODE=your_secret_admin_code_here
```

---

### 4️⃣ Database Initialization & Server Startup

The database tables are automatically verified and initialized on app context launch.

```bash
# Run the application
python app.py
```

---

### 5️⃣ Access Portal URLs

| Portal | URL / Access Path | Description |
| :--- | :--- | :--- |
| **Main Portal** | `http://127.0.0.1:5000/` | Public landing page |
| **Login Page** | `http://127.0.0.1:5000/login` | Student / Driver / Admin login |
| **Student Registration** | `http://127.0.0.1:5000/register` | Student sign-up with hidden staff access link |
| **Driver Registration** | Accessible via Staff Gate Modal on `/register` | Passcode-gated driver account creation |
| **Admin Registration** | Accessible via Staff Gate Modal on `/register` | Passcode-gated admin account creation |
| **Student Dashboard** | `http://127.0.0.1:5000/student` | Student QR boarding & history |
| **Driver Dashboard** | `http://127.0.0.1:5000/driver` | Driver QR generator & live GPS broadcast |
| **Admin Control Portal** | `http://127.0.0.1:5000/admin` | System overview & Fleet Operations map |
| **IoT Kiosk Simulator** | `http://127.0.0.1:5000/kiosk?bus_no=Bus-10` | Entrance kiosk face AI recognition camera |

---

## ⚠️ KNOWN LIMITATIONS (PROTOTYPE SCOPE)

* **Mock ERP Data Integration**: Student profiles and fee statuses are stored in a local SQLite database (`instance/smart_bus.db`) rather than live institutional ERP API webhooks.
* **Webcam Demo Environment**: The entrance kiosk (`/kiosk`) operates via browser webcam feeds (`getUserMedia`) rather than dedicated edge AI hardware (e.g., NVIDIA Jetson or industrial IP camera units).
* **Simulated GPS Fleet Movement**: Fleet bus locations on Leaflet maps run on an interpolated waypoint simulation engine (`simulation_loop`) for demonstration rather than vehicle-mounted OBD-II GPS hardware.
* **Shared Passcode Access Gate**: Staff registration uses a shared passcode gate (`DRIVER_REGISTER_CODE` / `ADMIN_REGISTER_CODE` configured in `.env`) appropriate for prototype evaluation, rather than centralized single-use admin invitation tokens.
* **Local SQLite Storage**: Uses local SQLite database storage and filesystem session caching, suitable for prototype testing but requiring PostgreSQL and Redis for multi-worker production scale.

---

## 📊 FUTURE ENHANCEMENTS

* 📱 Dedicated **Android / iOS Native App** (Flutter / React Native)
* 📲 **Push Notifications** (Firebase Cloud Messaging & WhatsApp Business API)
* 🎟️ **Admin-Issued Single-Use Staff Invitation Tokens** with Multi-Factor Authentication (MFA)
* 🛰️ **OBD-II Hardware GPS Tracker Integration**
* 🤖 **Predictive Route Optimization & AI Passenger Demand Forecasting**
* 📈 **Automated Reports Export** (PDF / Excel Attendance Audits)

---

## 📄 LICENSE

This project is licensed under the **MIT License**. See the `LICENSE` file for details.

---

## 👨‍💻 DEVELOPER CREDIT

**Sudharsan S**  
*Full Stack Developer & AI Systems Engineer*  

Developed for:  
**VET Institute of Arts and Science – Transport Division**
