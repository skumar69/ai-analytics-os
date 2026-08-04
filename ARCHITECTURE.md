# VisionIQ Architecture

## Overview

VisionIQ is structured as a three-tier application with a strict layered architecture:

```
┌──────────────────────────────────────────────────────────┐
│                     React Frontend                       │
│                                                          │
│  LoginPage │ Dashboard │ Reliability │ Executive │ AI   │
│                                                          │
│  Components: KpiCard, FilterBar, DrillDownDialog,       │
│  AssetHealthCard, EquipmentHealthGauge, AICopilot...    │
└────────────────────────┬─────────────────────────────────┘
                         │ HTTP REST
                         │ JWT Bearer Token
┌────────────────────────▼─────────────────────────────────┐
│                   FastAPI Backend                        │
│                                                          │
│  auth_api    analytics_api    sap_api    copilot_api     │
│  charts_api  dashboard_api   assets_api  notifications   │
│                                                          │
│  All routers are thin controllers — no business logic   │
└────────────────────────┬─────────────────────────────────┘
                         │
┌────────────────────────▼─────────────────────────────────┐
│                   Service Layer                          │
│                                                          │
│  copilot_engine    sap_intelligence    pm_analytics      │
│  kpi_engine        risk_engine         ai_engine         │
│  analytics         data_mapper                          │
│                                                          │
│  All business logic lives here. APIs only call services │
└────────────────────────┬─────────────────────────────────┘
                         │
┌────────────────────────▼─────────────────────────────────┐
│                   Data Service                           │
│                  data_service.py                         │
│                                                          │
│  set_dataframe()         → stores upload                 │
│  get_normalized_dataframe() → standard schema            │
│  get_filtered_dataframe()   → with filters applied       │
│  get_filter_options()       → unique values for dropdowns│
└────────────────────────┬─────────────────────────────────┘
                         │
                    SAP PM Excel
               (uploaded via /upload)
```

---

## Data Flow

```
User uploads Excel
       │
       ▼
upload_api.py
       │
       ▼
data_mapper.normalize(df)
  → maps 35+ SAP column names → 13 standard fields
  → preserves unmapped columns as _raw_*
       │
       ▼
data_service.set_dataframe(df)
  → stores raw df
  → stores normalized df
  → caches filter options
       │
       ▼
Any API call (with optional filters)
       │
       ▼
get_filtered_dataframe(plant, priority, status, ...)
       │
       ▼
pm_analytics / sap_intelligence / kpi_engine
       │
       ▼
JSON response to React frontend
```

---

## Standard Schema (data_mapper.py)

VisionIQ normalizes every upload to these 13 fields:

| Field | SAP Source Columns |
|---|---|
| `equipment` | Equipment, Equip No, Equipment Number |
| `plant` | Plant, Maintenance Plant |
| `notification` | Notification, Notification No |
| `work_order` | Order, Order Number, Work Order |
| `priority` | Priority |
| `status` | System Status, User Status, Status |
| `planner_group` | Planner Group, Planning Group |
| `functional_location` | Functional Location, Func. Loc., FLoc |
| `order_type` | Order Type, PM Order Type |
| `created_on` | Created On, Creation Date, Basic Start Date |
| `completed_on` | Basic Finish Date, Actual Finish |
| `description` | Description, Short Text |
| `maintenance_type` | Maintenance Activity Type, Activity Type |

---

## Analytics Engines

### pm_analytics.py
Core reliability calculations:
- `calculate_mttr(df)` — avg days created→completed for closed orders
- `calculate_mtbf(df)` — avg days between consecutive failures per equipment
- `calculate_pm_compliance(df)` — % of orders in completed status
- `calculate_breakdown_percentage(df)` — % classified as corrective
- `calculate_backlog(df)` — open orders by plant and planner
- `calculate_work_order_age(df)` — age buckets for open orders
- `calculate_failure_frequency(df)` — failure count per equipment
- `calculate_equipment_health(df)` — 0–100 score based on failure rate
- `calculate_asset_criticality(df)` — weighted score (frequency × priority)
- `get_equipment_detail(name)` — all work orders for drill-down

All functions accept an optional `df` parameter — pass a filtered frame or `None` to use the global upload.

### sap_intelligence.py
Enterprise-grade KPIs:
- `calculate_asset_health_scores()` — composite score with 5 weighted factors
- `pm_compliance_by_plant()` — compliance rate per plant
- `planner_group_performance()` — backlog + compliance per planner
- `work_order_sla(days)` — overdue analysis by priority
- `repeat_failure_analysis()` — chronic failure ranking
- `mttr_trend()` — monthly MTTR improvement tracking
- `equipment_reliability_index()` — MTBF/(MTBF+MTTR) × 100

### copilot_engine.py
Natural language intent matching:
- 13 intent patterns (regex-based)
- Each intent calls the appropriate analytics function
- Returns: `answer` (markdown), `related_assets`, `recommendations`, `intent`

---

## Authentication Flow

```
POST /auth/login  {username, password}
       │
       ▼
auth_service.authenticate_user()
  → pbkdf2_sha256 password verification
       │
       ▼
create_access_token()
  → JWT signed with SECRET_KEY
  → 8-hour expiry
  → payload: {sub: username, role: Role}
       │
       ▼
Response: {access_token, token_type, user: {username, role, permissions}}
       │
       ▼
React AuthContext stores token in localStorage
       │
       ▼
Subsequent requests: Authorization: Bearer <token>
```

---

## Frontend Component Map

```
App.jsx
├── AuthGate          (checks auth, shows LoginPage or AppShell)
│   └── ErrorBoundary (catches render crashes)
└── AppShell
    ├── Navbar         (brand + role chip + logout)
    ├── Sidebar        (navigation with active-route highlight)
    └── Routes
        ├── /              → Dashboard (KPIs, charts, upload)
        ├── /reliability   → ReliabilityDashboard
        ├── /executive     → ExecutiveDashboard
        ├── /ai            → AICopilot
        └── (future: /predictive, /settings)
```

---

## Deployment Architecture

### Docker Compose (development/staging)
```
docker-compose.yml
  backend  (Python 3.12, port 8000)
  frontend (Nginx, port 80, proxies /api/* → backend:8000)
```

### Production (recommended)
```
Vercel (frontend static)
  ↓
FastAPI on Render / Railway / Azure App Service
  ↓
PostgreSQL (Sprint 7 — not yet implemented)
  ↓
Azure Blob Storage (for Excel uploads)
```
