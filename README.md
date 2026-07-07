<div align="center">

# 🔥 Resume Roaster

**An AI-powered resume analysis platform that roasts your resume, scores your job readiness, and tells you exactly what's missing — built to understand how real GenAI SaaS products are architected, not just prompted.**

[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Groq](https://img.shields.io/badge/Groq-LLM-F55036?style=flat-square)](https://groq.com/)
[![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=flat-square&logo=mysql&logoColor=white)](https://www.mysql.com/)
[![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=docker&logoColor=white)](https://www.docker.com/)
[![eSewa](https://img.shields.io/badge/eSewa-ePay_v2-60BB46?style=flat-square)](https://developer.esewa.com.np/)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)](LICENSE)

</div>

---

## 💡 Why This Project

Most "AI resume tools" are a single prompt wrapped in a form. Resume Roaster was built to go deeper — a real full-stack SaaS with authentication, persistent history, rate-limited AI endpoints, and a CI/CD pipeline behind it. The goal wasn't just "call an LLM," it was to understand the engineering layer *around* the LLM call: auth flows, schema design, error handling, and deployment.

It analyzes an uploaded resume and returns:
- 🔥 A genuinely funny, honest **roast**
- 📊 A **job readiness score**
- 🧩 A **skill-gap analysis**
- ✍️ Concrete **improvement suggestions**

---

## ✨ Features

| Category | What it does |
|---|---|
| 🔐 **Authentication** | Signup/login, JWT-based sessions, bcrypt password hashing, protected routes |
| 📄 **Resume Analysis** | Upload PDF/TXT → text extraction → LLM-powered roast, gap analysis, readiness score, suggestions |
| 🤖 **AI Integration** | Groq API (OpenAI-compatible), custom prompt engineering tuned for career feedback |
| 🗂️ **History** | Every analysis saved per-user, viewable on a dashboard |
| 💳 **Payments** | eSewa ePay v2 integration — HMAC-SHA256 signed payloads, Base64 callback decoding, server-side verification |
| 🛡️ **Security** | JWT auth, environment-based secrets, rate limiting, structured error handling |
| ⚙️ **DevOps** | Dockerized backend + DB, GitHub Actions CI/CD |

---

## 🏗 Architecture

```
                ┌──────────────────────┐
                │   Frontend (HTML/JS) │
                │  index · signup · login · dashboard
                └──────────┬───────────┘
                           │  REST (fetch)
                           ▼
                ┌──────────────────────┐
                │     FastAPI Backend   │
                │                        │
                │  ┌──────────────────┐  │
                │  │  Auth (JWT)       │  │
                │  ├──────────────────┤  │
                │  │  Resume Pipeline  │──┼──▶  Groq LLM API
                │  ├──────────────────┤  │
                │  │  Payment (eSewa)  │──┼──▶  eSewa ePay v2
                │  ├──────────────────┤  │
                │  │  Rate Limiting    │  │
                │  └──────────────────┘  │
                └──────────┬───────────┘
                           │  SQLAlchemy ORM
                           ▼
                ┌──────────────────────┐
                │     MySQL Database    │
                └──────────────────────┘
```

---

## 🛠 Tech Stack

<table>
<tr>
<td valign="top" width="33%">

**Frontend**
- HTML / CSS / JS


</td>
<td valign="top" width="33%">

**Backend**
- Python + FastAPI
- SQLAlchemy ORM
- MySQL
- JWT + Passlib + bcrypt

</td>
<td valign="top" width="33%">

**AI / DevOps / Payments**
- Groq LLM API
- eSewa ePay v2
- Docker + Docker Compose
- GitHub Actions CI/CD
  

</td>
</tr>
</table>

---

## 📂 Project Structure

```
Resume-Roaster/
├── backend/
│   ├── app/
│   │   ├── main.py                 # FastAPI entry point
│   │   ├── routes/
│   │   │   ├── auth.py             # Signup/Login
│   │   │   ├── roast.py            # Resume upload + roast
│   │   │   └── llm_analyze.py      # LLM analysis endpoints
│   │   ├── database/
│   │   │   ├── db.py               # DB connection
│   │   │   ├── models.py           # SQLAlchemy models
│   │   │   └── dependencies.py     # Session dependency
│   │   ├── services/
│   │   │   └── llm_service.py      # Groq API integration
│   │   ├── utils/
│   │   │   ├── jwt.py              # JWT creation
│   │   │   ├── deps.py             # JWT verification
│   │   │   ├── rate_limit.py       # API rate limiting
│   │   │   └── errors.py           # Error handling
│   │   └── schemas/
│   │       └── auth.py             # Pydantic schemas
│   ├── tests/
│   │   └── test_main.py
│   ├── Dockerfile
│   ├── requirements.txt
│   └── .env
│
├── frontend/
│   ├── index.html
│   ├── signup.html
│   ├── login.html
│   ├── dashboard.html
│   ├── style.css
│   └── app.js
│
├── .github/workflows/backend.yml   # CI pipeline
├── docker-compose.yml              # Backend + MySQL
└── README.md
```

---

## ⚙️ Getting Started

### 1. Clone the repo
```bash
git clone <repo-url>
cd Resume-Roast
```

### 2. Backend setup
```bash
cd backend
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # macOS/Linux

pip install -r requirements.txt
```

Create a `.env` file in `backend/`:
```env
DATABASE_URL=mysql+pymysql://username:password@localhost/resume_roaster
SECRET_KEY=your_secret
ALGORITHM=HS256
GROQ_API_KEY=your_api_key
```

Run it:
```bash
uvicorn app.main:app --reload
```
- API → `http://127.0.0.1:8000`
- Interactive docs → `http://127.0.0.1:8000/docs`

### 3. Frontend setup
```bash
cd frontend
python -m http.server 5500
```
or simply open `index.html` in your browser.

### 4. Or just run it all with Docker 🐳
```bash
docker-compose up --build
```
This spins up the FastAPI backend **and** MySQL together — zero local setup needed.

---

## 🔐 API Reference

<details>
<summary><b>Authentication</b></summary>

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/auth/signup` | Register a new user |
| `POST` | `/auth/login` | Log in, returns a JWT |

</details>

<details>
<summary><b>Resume Analysis</b></summary>

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/llm_analyze/analyze` | Upload + analyze a resume (requires `Authorization: Bearer <token>`) |
| `GET` | `/llm_analyze/history` | Fetch the logged-in user's past analyses |

</details>

---

## 💳 eSewa Payment Integration

Resume Roaster uses **eSewa ePay v2** for one-time payments. Unlike typical REST APIs, eSewa uses a **client-side form-redirect model** — your backend builds a cryptographically signed payload, the frontend submits it as a form to eSewa, and eSewa redirects back with a Base64-encoded receipt.

### How it works

```
User clicks "Pay"
      │
      ▼
POST /payment/initiate  ──▶  FastAPI builds payload
                              + HMAC-SHA256 signature
      │
      ▼
Frontend auto-submits hidden form ──▶  eSewa Payment Page
                                              │
                                    User enters PIN + pays
                                              │
                                              ▼
                              eSewa redirects to /payment/success
                                    ?data=<Base64-encoded JSON>
                                              │
                                              ▼
                              FastAPI decodes Base64 receipt
                              Verifies HMAC signature
                              Marks payment COMPLETE in DB
```

### Sandbox credentials (for local testing)

| Field | Value |
|---|---|
| eSewa ID | `9806800001` – `9806800005` |
| Password | `Nepal@123` |
| MPIN | `1122` |
| OTP | `123456` |
| Product Code | `EPAYTEST` |
| Secret Key | `8gBm/:&EnhH.1/q` |
| Payment URL | `https://rc-epay.esewa.com.np/api/epay/main/v2/form` |
| Status Check | `https://rc.esewa.com.np/api/epay/transaction/status/` |

> ⚠️ Sandbox credentials only. For production, get your `product_code` and `secret_key` from the [eSewa Merchant Dashboard](https://merchant.esewa.com.np).


---

## 🔄 CI/CD Pipeline

```
Git Push ──▶ GitHub Actions ──▶ Install deps ──▶ Run tests ──▶ Validate backend
```

Every push to the backend is automatically installed, tested, and validated before it's considered deployable.

---

## 🗺 Roadmap

- [x] eSewa ePay v2 payment integration with HMAC-SHA256 verification
- [ ] Resume scoring against specific job descriptions (JD-matching)
- [ ] Export roast + feedback as a shareable PDF
- [ ] Support for `.docx` resume uploads

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

<div align="center">

Built with 🔥 by <a href="https://github.com/">Krishala</a>

</div>
