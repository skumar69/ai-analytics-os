# Changelog

All notable changes to VisionIQ are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

---

## [6.0.0] — 2026-08-04

### Added
- **AI Copilot** — rule-based NL analytics engine (`services/copilot_engine.py`)
  - 13 intent handlers: risk, health, failures, backlog, SLA, MTTR, MTBF, compliance, planner, KPI, trend, recommendations, help
  - Every answer backed by real analytics — no hallucinated maintenance facts
  - `POST /copilot/ask`, `GET /copilot/suggest`
- **Chat UI** (`pages/AICopilot.jsx`) — message history, markdown rendering, suggested questions, asset chips, copy button, recommended actions

### Fixed
- **Rules-of-Hooks violation** in `App.jsx` — `useState` was called after a conditional `return`
- **Blank page crash** — `theme.js` separate module import caused browser evaluation error; moved inline
- **Duplicate MUI imports** in `App.jsx`
- **Icon names** updated for MUI v9 (`ExitToApp`, `DeleteForever`)

---

## [5.1.0] — 2026-08-04

### Added
- **MUI Dark Theme** — brand colors, card hover effects, consistent borders, Inter font
- **EmptyState** component — icon + title + message + optional CTA
- **LoadingSkeletons** — `KPISkeletons`, `ChartSkeleton`, `TableSkeleton`
- **PageHeader** — breadcrumbs + title + subtitle + actions slot
- **ErrorBanner** — dismissable alert with retry button
- **KpiCard redesign** — color-coded top border, trend indicator, subtitle, built-in skeleton, hover lift

### Changed
- `ReliabilityDashboard` uses skeletons instead of spinner; added `PageHeader` and `ErrorBanner`
- `KPISection` accepts `loading` and `color` props

---

## [5.0.0] — 2026-08-04

### Added
- **SAP PM Intelligence Engine** (`services/sap_intelligence.py`)
  - `calculate_asset_health_scores` — composite 0–100 score (failure freq 30%, MTTR 20%, MTBF 20%, open orders 15%, PM rate 15%)
  - `pm_compliance_by_plant`, `planner_group_performance`, `work_order_sla`, `repeat_failure_analysis`, `mttr_trend`, `equipment_reliability_index`
- **SAP API** (`api/sap_api.py`) — `/sap/*` endpoints, all filter-aware
- **`/sap/intelligence-summary`** — single aggregated payload
- **Executive Dashboard** (`pages/ExecutiveDashboard.jsx`) — fleet health score, SLA card, asset grid, MTTR trend, planner performance, repeat failures
- **AssetHealthCard**, **MTTRTrendChart**, **PlannerPerformanceTable**, **RepeatFailureTable** components

---

## [4.0.0] — 2026-08-04

### Added
- **47 automated tests** across 5 test modules
  - `test_data_mapper.py` (7), `test_pm_analytics.py` (17), `test_auth.py` (11), `test_upload.py` (4), `test_analytics.py` (10)
- **JWT Authentication** — `services/auth_service.py`, `api/auth_api.py`
  - 5 roles: Admin, Manager, Planner, Technician, Executive
  - pbkdf2_sha256 password hashing
- **Docker** — `backend/Dockerfile`, `frontend-react/Dockerfile`, `docker-compose.yml`
- **GitHub Actions CI** — test + build + Docker check on every push/PR
- **Structured logging** — `utils/logger.py`, replaced all `print()` calls
- **Login page** with demo account quick-fill buttons

### Fixed
- `calculate_mttr` — variable shadowing NoneType subscript bug
- `get_equipment_detail` — NaN → null-safe JSON serialization
- `data_mapper` — `maintenance_type` added as self-mapping candidate

---

## [3.5.0] — 2026-08-04

### Added
- **Reliability Analytics Dashboard** — MTTR, MTBF, PM Compliance, Breakdown %, Equipment Health Gauge, Top Failure Table, Backlog Chart, Work Order Age
- **FilterBar** — Plant, Priority, Status, Planner Group, Date From/To with Apply/Clear
- **DrillDownDialog** — work order history per equipment (clickable)
- **`/analytics/dashboard`** — single aggregated endpoint (replaces 3 separate calls)
- **`/analytics/filter-options`** — populates filter dropdowns from uploaded data
- **`/analytics/equipment/{name}`** — drill-down detail
- **`/analytics/export`** — streams filtered data as Excel
- **React Router** — multi-page navigation with active-route sidebar highlight

---

## [3.0.0] — 2026-08-04

### Added
- **Modular API layer** — 7 FastAPI routers (all thin controllers)
- **Service layer** — `data_service`, `kpi_engine`, `risk_engine`, `ai_engine`, `analytics`
- **`data_service.py`** — single source of truth for uploaded data
- **`data_mapper.py`** — SAP column normalization (35+ known column variants → 13 standard fields)
- **`pm_analytics.py`** — MTTR, MTBF, PM compliance, backlog, health, criticality, failure frequency
- **React + Vite dashboard** — MUI 9, Recharts, all charts wired to live API
- **`/analytics/summary`** endpoint

