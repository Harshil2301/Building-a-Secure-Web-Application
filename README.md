# 🔐 Secure Web Application (OWASP-Aligned)

A portfolio-ready Flask application demonstrating the **identification, exploitation, and mitigation of common web security vulnerabilities**, aligned with OWASP Top 10 principles.

---

## 📌 Overview

This project was initially designed with intentionally vulnerable components to simulate real-world security flaws. These vulnerabilities were then systematically mitigated using secure coding practices and validated through controlled attack simulations.

---

## 🚨 Vulnerability Demonstration

### 🔴 Before (Vulnerable System)

* Plaintext password storage
* No authentication enforcement on protected routes
* Susceptible to SQL Injection attacks

### 🔴 Attack Simulation

* SQL Injection payload: `admin' OR '1'='1`
* Unauthorized direct access to `/dashboard` endpoint

---

## 🛡️ Security Implementation

* **SQL Injection Protection**
  Leveraged Flask-SQLAlchemy ORM to enforce parameterized queries, eliminating injection risks.

* **Secure Authentication (JWT)**
  Implemented token-based authentication using Flask-JWT-Extended to prevent unauthorized access.

* **Password Security (scrypt hashing)**
  Used `werkzeug.security` to hash passwords before storage, ensuring irreversible credential protection.

* **Access Control Enforcement**
  Restricted protected endpoints using authentication checks and token validation.

---

## 🧪 Security Testing (OWASP-Inspired)

| Test Case             | Description                                  | Result       |
| --------------------- | -------------------------------------------- | ------------ |
| SQL Injection         | Login bypass attempt using injection payload | ❌ Blocked    |
| Broken Authentication | Direct access to protected route             | ❌ Blocked    |
| Password Exposure     | Database inspection for plaintext passwords  | ❌ Eliminated |

---

## 🎨 UI Features

* Modern Glassmorphism design
* Clean and responsive authentication interface
* Lightweight frontend (pure HTML/CSS, no heavy frameworks)

---

## 🛠️ Tech Stack

* Python (Flask)
* Flask-SQLAlchemy
* Flask-JWT-Extended
* SQLite
* HTML, CSS

---

## 🚀 Setup & Installation

```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name

# Create virtual environment
python -m venv .venv

# Activate
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run application
python app.py
```

The application will start at:
👉 http://127.0.0.1:5000

---

## 🔍 Security Testing Guide

### 🔴 SQL Injection Test

Try the following payload in the login form:

```
admin' OR '1'='1
```

👉 Result: Authentication is securely rejected.

---

### 🔴 Unauthorized Access Test

Visit:

```
http://127.0.0.1:5000/dashboard
```

without logging in.

👉 Result: Access denied due to missing/invalid JWT token.

---

## 📊 Key Takeaways

* Demonstrates real-world vulnerability exploitation and mitigation
* Highlights importance of secure authentication and input handling
* Validates defenses through practical attack simulation

---

## 👨‍💻 Author

Harshil Parmar
