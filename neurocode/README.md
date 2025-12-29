# NeuroCode - ADHD-Focused Python Tutor

An adaptive Python programming tutor designed for middle schoolers (grades 6-8) with ADHD. Built using FastAPI and Google's Gemini API.

## 🚀 Quick Start

### Prerequisites
- Python 3.11+ installed
- Google Gemini API key

### Installation

1. **Navigate to the backend folder:**
   ```powershell
   cd d:\RespectResearch\neurocode\backend
   ```

2. **Install dependencies:**
   ```powershell
   pip install -e ".[dev]"
   ```

3. **Verify your `.env` file has your Gemini API key:**
   ```
   GEMINI_API_KEY=your_api_key_here
   ```

4. **Start the server:**
   ```powershell
   uvicorn app.main:app --reload
   ```

5. **Open API Documentation:**
   - **Swagger UI:** http://localhost:8000/docs
   - **Health Check:** http://localhost:8000/health

### Seed Sample Exercises

After starting the server, run this to add sample exercises:
```powershell
Invoke-WebRequest -Uri "http://localhost:8000/api/admin/seed-exercises" -Method POST
```

Or using curl:
```bash
curl -X POST http://localhost:8000/api/admin/seed-exercises
```

---

## 📁 Project Structure

```
neurocode/
├── backend/
│   ├── app/
│   │   ├── main.py           # FastAPI entry point
│   │   ├── config.py         # Environment settings
│   │   ├── database.py       # SQLite/SQLAlchemy setup
│   │   ├── models/           # Database models
│   │   ├── schemas/          # Pydantic validation
│   │   ├── services/         # Business logic
│   │   │   ├── gemini_service.py
│   │   │   ├── task_decomposer.py
│   │   │   └── hint_generator.py
│   │   ├── prompts/          # LLM system prompts
│   │   ├── routers/          # API endpoints
│   │   └── utils/            # Helpers
│   ├── tests/                # Pytest tests
│   ├── pyproject.toml        # Dependencies
│   └── .env                  # Environment variables
└── README.md
```

---

## 🔌 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/auth/register` | POST | Register new student |
| `/api/auth/login` | POST | Login and get JWT token |
| `/api/auth/me` | GET | Get current user profile |
| `/api/tutor/message` | POST | Send message to AI tutor |
| `/api/tutor/hint` | POST | Get hint (levels 1-4) |
| `/api/tutor/decompose` | POST | Break task into micro-steps |
| `/api/exercises/` | GET | List all exercises |
| `/api/exercises/{id}/run` | POST | Run student code |
| `/api/exercises/{id}/test` | POST | Run code against tests |
| `/api/progress/summary` | GET | Get student progress |
| `/api/admin/seed-exercises` | POST | Add sample exercises |

---

## 🧪 Running Tests

```powershell
cd d:\RespectResearch\neurocode\backend
python -m pytest tests/ -v
```

### Test Coverage
- **179 tests total** (95% passing)
- Unit tests for all services
- Human-perspective tests (typos, ADHD patterns)
- Edge case and security tests

---

## 🧠 ADHD-Specific Features

- **Micro-task decomposition:** Problems broken into 3-5 small steps
- **4-level hint escalation:** From gentle nudge → full solution
- **Frustration detection:** Auto-escalates when student struggles
- **20-minute break reminders:** Configurable per user
- **Reduced animations by default:** Less visual distraction
- **Gamification:** Points and streaks for motivation

---

## 🔒 COPPA Compliance

- Users under 13 require parental consent
- Minimal PII collected (username only)
- Parent email verification flow
- Research consent separate from platform consent

---

## 🛠️ Technology Stack

- **Backend:** Python 3.11+, FastAPI, SQLAlchemy 2.0
- **Database:** SQLite (dev) / PostgreSQL (prod)
- **AI:** Google Gemini API (gemini-2.0-flash)
- **Auth:** JWT tokens with pbkdf2 password hashing
