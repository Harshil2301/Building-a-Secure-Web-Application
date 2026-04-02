# Secure Web Application

A portfolio-ready, fully secure Flask web application designed to demonstrate the mitigation of OWASP Top 10 vulnerabilities.

The system was initially designed with common vulnerabilities, which were then systematically mitigated using secure coding practices and verified through controlled attack simulations.

## Features

- **SQL Injection Defense**: Uses `Flask-SQLAlchemy` ORM to completely neutralize SQL injection payloads by ensuring all database queries are strictly parameterized.
- **Robust Authentication**: Employs `Flask-JWT-Extended` to issue and verify secure session tokens, blocking unauthorized or broken access attempts.
- **Cryptographic Hashing**: User credentials are not stored in plain text. Instead, strong `scrypt` hashing is applied via `werkzeug.security` before storing passwords in the database.
- **Modern UI Architecture**: A deeply custom "Glassmorphism" design using vanilla CSS, demonstrating premium frontend capability without reliance on heavy frameworks.

## Setup & Installation

**1. Clone the repository and navigate inside:**
```bash
git clone https://github.com/your-username/your-repo-name.git
cd "your-repo-name"
```

**2. Create and activate a Virtual Environment:**
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS/Linux
python3 -m venv .venv
source .venv/bin/activate
```

**3. Install Dependencies:**
```bash
pip install -r requirements.txt
```

**4. Run the Application:**
```bash
python app.py
```
> The application will automatically create the secure `instance/secure_app.db` local SQLite database and spin up on `http://127.0.0.1:5000`.

## Testing the Security

This project is built to defend against literal attacks. You can test these protections yourself:
- **SQLi Test:** On the login page, try using `admin' OR '1'='1` in the username to bypass authentication. It will securely reject it.
- **Broken Access Test:** Try to visit `http://127.0.0.1:5000/dashboard` directly without logging in. The server will reject the request due to missing JWT cookies.
