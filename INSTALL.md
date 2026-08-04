# VisionIQ Installation Guide

## Prerequisites

| Requirement | Minimum | Recommended |
|---|---|---|
| Python | 3.12 | 3.12+ |
| Node.js | 18 | 20 LTS |
| RAM | 2 GB | 4 GB |
| Disk | 500 MB | 1 GB |

---

## Option A: Local Development

### 1. Clone the repository

```bash
git clone https://github.com/skumar69/ai-analytics-os.git
cd ai-analytics-os
```

### 2. Backend setup

```bash
cd backend
python -m venv .venv

# macOS / Linux
source .venv/bin/activate

# Windows (PowerShell)
.\.venv\Scripts\Activate.ps1

pip install -r requirements.txt
```

### 3. Start the backend

```bash
uvicorn main:app --reload --port 8000
```

Verify: open http://127.0.0.1:8000/docs

### 4. Frontend setup

```bash
# From project root
cd frontend-react
npm install
npm run dev
```

Verify: open http://localhost:5173

---

## Option B: Docker Compose (Recommended)

### Requirements
- Docker Desktop 24+ or Docker Engine + Compose plugin

### Start everything

```bash
docker compose up --build
```

| Service | URL |
|---|---|
| Frontend | http://localhost |
| Backend API | http://localhost:8000 |
| API Docs | http://localhost:8000/docs |

### Stop

```bash
docker compose down
```

---

## Environment Variables

The backend uses these environment variables (all have defaults for local dev):

| Variable | Default | Description |
|---|---|---|
| `VISIONIQ_SECRET_KEY` | `visioniq-secret-key-...` | JWT signing key — **change in production** |
| `VISIONIQ_ENV` | `development` | Set to `production` in Docker |

To override, create `backend/.env`:
```
VISIONIQ_SECRET_KEY=your-very-long-random-secret-here
VISIONIQ_ENV=production
```

---

## Running Tests

```bash
cd backend
source .venv/bin/activate
pytest tests/ -v
```

Expected output: **47 passed, 0 failed**

---

## Supported SAP Excel Formats

Upload any of these SAP PM transaction exports (`.xlsx` or `.xls`):

- **IW38 / IW39** — Work Order List (most common)
- **IW28** — Notification List
- **IP24** — Preventive Maintenance Schedule
- **IE01 export** — Equipment Master data

VisionIQ auto-detects column names. No reformatting required.
