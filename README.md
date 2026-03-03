<img width="1284" height="396" alt="GitHub Banners" src="https://github.com/user-attachments/assets/d8ecf2c2-a673-44d6-b4f7-6c0e260ff87f" />

</p>

![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)
![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![Dash](https://img.shields.io/badge/Dash-Framework-008DE4?logo=plotly)
![SQLite](https://img.shields.io/badge/SQLite-Database-003B57?logo=sqlite)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)

ThreatPulse is a local multi-protocol intelligent honeypot system that simulates SSH and HTTP services to capture attacker behavior, log credential attempts, detect brute-force activity, and visualize live attack telemetry through an interactive SOC-style dashboard.

The system records authentication attempts, command executions, and metadata into a centralized SQLite database, performs GeoIP enrichment, and generates real-time analytics using Dash and Plotly.

---

## 🚀 Features

- 🔐 SSH Honeypot (Paramiko-based)
- 🌐 HTTP Login Honeypot
- 📝 Credential Attempt Logging
- ⌨ SSH Command Capture
- 🌍 GeoIP-Based Attacker Country Detection
- ⚠ Brute-Force Detection (IP threshold-based)
- 📊 Real-Time SOC Dashboard (Dash + Plotly)
- 📈 Dynamic Risk Scoring
- 📁 Centralized SQLite Attack Database
- 🎨 Custom Frontend (HTML, CSS, JS)

---

## 🏗 Project Structure

```
ThreatPulse/
│
├── analytics/
│   ├── geoip.py
│   ├── parser.py
│   └── statistics.py
│
├── config/
│   └── settings.py
│
├── dashboard/
│   └── dashboard.py
│
├── data/
│   └── attackers.db
│
├── honeypots/
│   ├── http_honeypot.py
│   └── ssh_honeypot.py
│
├── web/
│   ├── static/
│   │   ├── style.css
│   │   ├── script.js
│   │   └── DetectFlow__HP_big.mp4
│   │
│   └── templates/
│       ├── index.html
│       ├── admin_dashboard.html
│       └── employee_dashboard.html
│
├── logs/
│   ├── http.log
│   └── ssh.log
│
├── app.py
├── requirements.txt
└── README.md
```

---

## ⚙ Installation

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/ThreatPulse.git
cd ThreatPulse
```

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv
```

### 3️⃣ Activate Virtual Environment

**Windows**
```bash
venv\Scripts\activate
```

**Linux / macOS**
```bash
source venv/bin/activate
```

### 4️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## ▶ Running the System

### Start Honeypots (SSH + HTTP)

```bash
python app.py
```

You will see:

```
SSH Honeypot  : ssh user@<local-ip> -p 2222
HTTP Honeypot : http://<local-ip>:8000
Dashboard     : http://<local-ip>:8050
```

---

### Start SOC Dashboard (Separate Terminal)

```bash
python -m dashboard.dashboard
```

Open in browser:

```
http://127.0.0.1:8050
```

---

## 🧪 Simulating Attacks

### 🔐 SSH Attack Simulation

```bash
ssh user@<local-ip> -p 2222
```

Enter any username and password.  
Failed authentication attempts are logged as attacks.  
SSH commands entered after login are captured and stored.

---

### 🌐 HTTP Attack Simulation

Open in browser:

```
http://<local-ip>:8000
```

Attempt login with incorrect credentials.  
Failed attempts are recorded as attacks.  
Successful logins are NOT counted as attacks.

---

## 📊 Dashboard Capabilities

The SOC Dashboard provides:

- Top Attacking IP visualization
- Protocol distribution analysis
- Hourly attack timeline
- Brute-force IP detection
- Dynamic risk scoring
- Live attack log feed
- GeoIP country enrichment

Dashboard refresh interval: **5 seconds**

---

## 🧠 Detection Logic

### 🔍 Brute-Force Detection
IPs exceeding a defined attempt threshold are automatically flagged as suspicious.

### 📈 Risk Score Calculation
Risk score scales dynamically based on total attack activity.

### 🌍 GeoIP Enrichment
Each attacker IP is enriched using a GeoIP API to determine country origin.

---

## 🗄 Database Schema

All attack telemetry is stored in a centralized SQLite database.

### Table: `attacks`

| Column    | Type     | Description                          |
|-----------|----------|--------------------------------------|
| id        | INTEGER  | Auto-increment primary key           |
| ip        | TEXT     | Attacker IP address                  |
| username  | TEXT     | Submitted username                   |
| password  | TEXT     | Submitted password                   |
| protocol  | TEXT     | HTTP / SSH / SSH_CMD                 |
| country   | TEXT     | GeoIP-detected country               |
| timestamp | TEXT     | ISO format timestamp                 |

---

## 🔒 Security Notice

ThreatPulse is designed strictly for:

- Local research
- Educational purposes
- Security experimentation
- Controlled lab environments

Do NOT deploy on public infrastructure without proper security controls.

---

## 🛠 Tech Stack

- Python 3.x
- Paramiko
- SQLite
- Dash
- Plotly
- Dash Bootstrap Components
- Pandas
- Requests
- HTML / CSS / JavaScript

---

## 👤 Author

Developed by **0xMalCore**

---

## 📜 License

This project is licensed under the Apache License 2.0.  
See the [LICENSE](LICENSE) file for full details.
