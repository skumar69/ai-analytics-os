# VisionIQ — Enterprise Asset Intelligence Platform

> **SAP PM / EAM Analytics, Reliability Engineering, and AI-powered Maintenance Intelligence**

[![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.141-009688?logo=fastapi)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-19-61DAFB?logo=react)](https://react.dev)
[![MUI](https://img.shields.io/badge/Material_UI-9-007FFF?logo=mui)](https://mui.com)
[![Docker](https://img.shields.io/badge/Docker-ready-2496ED?logo=docker)](https://docker.com)
[![CI](https://img.shields.io/badge/CI-GitHub_Actions-2088FF?logo=github-actions)](/.github/workflows/ci.yml)
[![Tests](https://img.shields.io/badge/Tests-47_passing-2e7d32?logo=pytest)](backend/tests/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![Version](https://img.shields.io/badge/Version-6.0.0-7c3aed)](CHANGELOG.md)

---

## Features

- AI KPI Engine
- Semantic AI Search
- Enrichment Engine
- VisionIQ Dashboard
- Interactive Analytics
- REST API Backend
- Modern Frontend
- Responsive Website

---

## Tech Stack

Python

FastAPI

JavaScript

HTML5

CSS3

GitHub

---

## Folder Structure

backend/
frontend/
website/
tests/

---

## Getting Started

Clone

```bash
git clone https://github.com/skumar69/ai-analytics-os.git
```

Install

```bash
pip install -r requirements.txt
```

Run

```bash
python app.py
```

---

## Vision

Building the next generation AI Analytics Platform.

Created by

**Sanjeev Kumar**

---

## What is VisionIQ?

VisionIQ transforms raw SAP PM / EAM Excel exports into a live enterprise analytics platform. Upload any standard SAP maintenance report (IW38, IW39, IW28, IP24) and instantly see:

- **MTTR / MTBF** — Mean Time To Repair and Between Failures
- **Asset Health Scores** — composite 0–100 risk index per equipment
- **PM Compliance** — by plant and planner group
- **Failure Pareto** — top failing equipment with repeat analysis
- **Work Order Backlog** — aged by plant, planner, and SLA
- **AI Copilot** — natural language answers grounded in real data

> *"Which equipment is at highest risk?"* → VisionIQ answers using your actual failure data.

---

## Architecture

```
┌─────────────────────────────────────────────┐
│                React Dashboard              │
│  Dashboard │ Reliability │ Executive │ AI   │
└──────────────────┬──────────────────────────┘
                   │  HTTP / REST
┌──────────────────▼──────────────────────────┐
│              FastAPI Backend                │
│  auth_api │ analytics_api │ sap_api         │
│  charts_api │ dashboard_api │ copilot_api   │
└──────────────────┬──────────────────────────┘
                   │
┌──────────────────▼──────────────────────────┐
│             Service Layer                   │
│  copilot_engine │ sap_intelligence          │
│  pm_analytics   │ kpi_engine                │
│  ai_engine      │ risk_engine               │
│  analytics      │ data_mapper               │
└──────────────────┬──────────────────────────┘
                   │
┌──────────────────▼──────────────────────────┐
│              Data Service                   │
│  data_service.py (single source of truth)  │
│  normalize → filter → analyze               │
└──────────────────┬──────────────────────────┘
                   │
             SAP PM Excel
          (IW38 / IW39 / IW28)
```

---

## Features

### Dashboard
- KPI cards: Work Orders, Notifications, Equipment, Plants, Asset Health, AI Score
- Monthly Work Order Trend (line chart)
- Priority Distribution (pie chart)
- Status Distribution (bar chart)
- Plant-wise Analysis
- High-Risk Asset table
- Notification log
- Excel upload with column auto-detection

### Reliability Analytics
- MTTR / MTBF cards with sample size
- PM Compliance gauge with progress bar
- Breakdown % indicator
- Equipment Health gauge (color-coded bars)
- Top Failure table (clickable drill-down)
- Work Order Age buckets
- Backlog by Plant
- Filter bar: Plant, Priority, Status, Planner Group, Date Range
- Export to Excel (filtered)

### Executive Dashboard
- Fleet Health Score (Red / Amber / Green)
- Work Order SLA violations
- PM Compliance by Plant
- MTTR Trend chart
- Planner Group Performance table
- Repeat Failure Analysis

### AI Copilot
- Natural language Q&A backed by real analytics
- 13 intent handlers (risk, health, MTTR, MTBF, backlog, SLA, compliance, planner, failures, trend, recommendations, KPI, help)
- Suggested questions
- Copy responses
- Asset chips and recommended actions on every answer

### Authentication
- JWT-based login (8-hour sessions)
- 5 roles: Admin, Manager, Planner, Technician, Executive
- Role-scoped page permissions
- Persistent sessions via localStorage

---

## Quick Start

### Prerequisites
- Python 3.12+
- Node.js 20+
- Git

### 1. Clone
```bash
git clone https://github.com/skumar69/ai-analytics-os.git
cd ai-analytics-os
```

### 2. Backend
```bash
cd backend
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```
Backend runs at **http://127.0.0.1:8000**

### 3. Frontend
```bash
cd frontend-react
npm install
npm run dev
```
Frontend runs at **http://localhost:5173**

### 4. Docker (one command)
```bash
docker compose up
```
- Frontend: http://localhost
- Backend: http://localhost:8000

---

## Demo Accounts

| Username | Password | Role | Access |
|---|---|---|---|
| `admin` | `admin123` | Admin | Everything |
| `manager` | `manager123` | Manager | Dashboard, Reliability, Executive, AI |
| `planner` | `planner123` | Planner | Dashboard, Reliability, Upload |
| `executive` | `exec123` | Executive | Dashboard, Executive, AI |
| `technician` | `tech123` | Technician | Dashboard only |

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/auth/login` | JWT authentication |
| GET | `/auth/me` | Current user profile |
| POST | `/upload` | Upload SAP PM Excel |
| GET | `/stats` | Dashboard KPIs |
| GET | `/analytics/dashboard` | Full analytics payload |
| GET | `/analytics/filter-options` | Available filter values |
| GET | `/analytics/equipment/{name}` | Equipment drill-down |
| GET | `/analytics/export` | Export filtered data as Excel |
| GET | `/sap/intelligence-summary` | SAP PM intelligence summary |
| GET | `/sap/asset-health` | Composite health scores |
| GET | `/sap/pm-compliance-by-plant` | PM compliance per plant |
| GET | `/sap/planner-performance` | Planner group metrics |
| POST | `/copilot/ask` | AI Copilot Q&A |
| GET | `/copilot/suggest` | Suggested questions |

All analytics endpoints accept: `?plant=&priority=&status=&planner_group=&date_from=&date_to=`

Interactive API docs: **http://127.0.0.1:8000/docs**

---

## Supported SAP Exports

VisionIQ auto-detects column names from these SAP PM reports:

| SAP Report | Transaction | Description |
|---|---|---|
| Work Order List | IW38 / IW39 | Maintenance orders with status, priority, dates |
| Notification List | IW28 | Maintenance notifications |
| PM Order History | IW37N | Historical order data |
| Preventive Maintenance | IP24 | PM task list and schedule |
| Equipment Master | IE01 | Equipment with plant and functional location |

Supported column variants: `Equipment`, `Equip No`, `Equipment Number`, `Plant`, `Maintenance Plant`, `System Status`, `User Status`, `Priority`, `Order`, `Order Number`, `Basic Finish Date`, `Actual Finish`, `Planner Group`, and more.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React 19, Vite 8, Material UI 9, Recharts, React Router |
| Backend | Python 3.12, FastAPI 0.141, Uvicorn |
| Analytics | Pandas 3, NumPy |
| Auth | JWT (python-jose), passlib (pbkdf2_sha256) |
| Testing | pytest, httpx (47 tests) |
| CI/CD | GitHub Actions (test + build + docker) |
| Container | Docker, Docker Compose, Nginx |

---

## Project Structure

```
ai-analytics-os/
├── backend/
│   ├── api/              # FastAPI routers (thin controllers)
│   │   ├── auth_api.py
│   │   ├── analytics_api.py
│   │   ├── charts_api.py
│   │   ├── dashboard_api.py
│   │   ├── sap_api.py
│   │   └── copilot_api.py
│   ├── services/         # Business logic
│   │   ├── data_service.py      # Single data source
│   │   ├── data_mapper.py       # SAP column normalization
│   │   ├── pm_analytics.py      # MTTR, MTBF, backlog, health
│   │   ├── sap_intelligence.py  # Asset health, PM compliance
│   │   ├── copilot_engine.py    # AI Copilot intent engine
│   │   ├── kpi_engine.py
│   │   ├── risk_engine.py
│   │   ├── ai_engine.py
│   │   └── analytics.py
│   ├── tests/            # 47 automated tests
│   ├── utils/
│   │   └── logger.py     # Structured logging
│   └── main.py
├── frontend-react/
│   ├── src/
│   │   ├── pages/        # Dashboard, Reliability, Executive, AI Copilot, Login
│   │   ├── components/   # 25+ reusable components
│   │   ├── context/      # AuthContext (JWT)
│   │   └── services/     # API client functions
│   └── Dockerfile
├── docker-compose.yml
├── .github/workflows/ci.yml
└── README.md
```

---

## Roadmap

| Version | Milestone | Status |
|---|---|---|
| v3.0 | Modular backend architecture | ✅ Complete |
| v3.5 | Reliability Analytics Dashboard | ✅ Complete |
| v4.0 | Authentication + Tests + Docker + CI | ✅ Complete |
| v5.0 | SAP PM Intelligence + Executive Dashboard | ✅ Complete |
| v5.1 | UI Polish (theme, skeletons, error handling) | ✅ Complete |
| v6.0 | AI Copilot (NL analytics engine) | ✅ Complete |
| v7.0 | Database persistence (SQLite → PostgreSQL) | 🔜 Planned |
| v7.1 | Upload history & multi-snapshot comparison | 🔜 Planned |
| v8.0 | SAP OData / S/4HANA live integration | 🔜 Planned |
| v9.0 | Predictive Maintenance (RUL, failure probability) | 🔜 Planned |
| v10.0 | LLM-augmented AI Copilot (grounded responses) | 🔜 Planned |

---

## License

MIT — see [LICENSE](LICENSE)

---

## Author

Built by **Sandeep Kumar** — SAP PM/EAM Analytics & AI Engineering

- GitHub: [@skumar69](https://github.com/skumar69)
- Website: [visioniqlabs.com](https://visioniqlabs.com)

