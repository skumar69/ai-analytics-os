# VisionIQ Roadmap

## Current: v6.0.0 — Feature Complete

The core analytics platform is complete and stable.

---

## v7.0 — Database Persistence (Sprint 7)

**Goal:** Replace in-memory storage with SQLite, then PostgreSQL.

### What changes:
- `data_service.py` reads/writes to database instead of module-level variable
- Upload history maintained across server restarts
- Multiple snapshots per user (July, August, September)
- Saved filter configurations
- User preferences stored

### Schema:
```sql
uploads (id, filename, uploaded_at, row_count, column_count, user_id)
upload_data (id, upload_id, data JSONB)
users (id, username, role, hashed_password)
```

---

## v7.1 — Multi-Snapshot Comparison

**Goal:** Compare SAP PM performance across periods.

- Upload July + August → side-by-side MTTR comparison
- Month-over-month PM compliance trend
- Equipment that improved / deteriorated between periods

---

## v8.0 — SAP OData / S/4HANA Integration

**Goal:** Replace Excel uploads with live SAP data.

### Architecture:
```
SAP S/4HANA
    │
    ▼
OData Service (e.g., /sap/opu/odata/sap/PM_WORKORDER_SRV)
    │
    ▼
VisionIQ SAP Connector (new service)
    │
    ▼
data_service.py (same interface, different source)
    │
    ▼
All analytics unchanged
```

### SAP Services to integrate:
- `PM_WORKORDER_SRV` — Maintenance Orders
- `PM_NOTIFICATION_SRV` — Maintenance Notifications
- `PM_EQUIPMENT_SRV` — Equipment Master
- `PM_FUNCLOCTN_SRV` — Functional Locations

---

## v9.0 — Predictive Maintenance

**Goal:** Rule-based failure prediction using historical patterns.

```
Equipment History
    │
    ▼
Failure Pattern Analysis
    │
    ├── MTBF-based: if today > last_failure + MTBF → flag
    ├── Frequency trend: failure rate increasing → alert
    └── Health score trajectory: declining → predict failure
    │
    ▼
Risk Score (0–100) + Failure Probability (%) + Recommended PM Date
```

### New components:
- `services/predictive_engine.py`
- `api/predictive_api.py`
- `pages/PredictiveMaintenance.jsx`
  - Equipment Risk Matrix
  - Failure Timeline
  - PM Date Optimizer

---

## v9.1 — Remaining Useful Life (RUL)

Extends Predictive Maintenance:
- `RUL = estimated_MTBF - days_since_last_failure`
- Equipment aging curve
- Spare parts demand forecast

---

## v10.0 — LLM-Augmented AI Copilot

**Goal:** Enhance the rule-based copilot with an LLM for natural language fluency.

### Architecture (keeps analytics grounded):
```
User Question
    │
    ▼
Intent Detection (regex — existing)
    │
    ├── Known SAP KPI → Analytics Engine → structured data
    │                                           │
    └── General question                        │
                │                               │
                ▼                               ▼
           LLM (OpenAI / Azure OpenAI)  ←── context injection
                │
                ▼
        Grounded response
```

This prevents the LLM from inventing maintenance facts.

---

## v11.0 — Enterprise Features

- Multi-tenant support (multiple plants / companies)
- Role-based data access (Planner A sees only their plant)
- Report scheduler (weekly PDF report via email)
- Executive PowerPoint export
- Mobile-responsive layout

---

## Future: SAP Ecosystem Integrations

| Integration | Benefit |
|---|---|
| SAP PM OData | Live work order data |
| SAP S/4HANA BAPI | Master data sync |
| SAP Analytics Cloud | Embedded analytics |
| SAP Asset Intelligence Network | External benchmarking |
| IBM Maximo | Cross-platform reliability |
| ServiceNow | IT/OT convergence |

---

## Contribution Priorities

If you'd like to contribute, the highest-value areas are:

1. **Real SAP PM datasets** — testing with actual IW38/IW39 exports reveals mapping gaps
2. **data_mapper.py** — additional column name variants from different SAP versions
3. **pm_analytics.py** — more sophisticated MTBF calculation (Weibull distribution)
4. **Test coverage** — integration tests for the full upload → analytics flow
5. **copilot_engine.py** — additional intent handlers and better NL matching
