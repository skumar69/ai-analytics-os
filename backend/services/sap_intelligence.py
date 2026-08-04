"""
SAP PM Intelligence Engine — Sprint 5
Composite Asset Health Score + real maintenance KPIs.
"""

from datetime import datetime
from typing import Optional
import pandas as pd
from services.data_service import get_normalized_dataframe, has_data
from services.pm_analytics import (
    calculate_failure_frequency,
    calculate_mttr,
    calculate_mtbf,
    _is_completed,
    _is_open,
    _parse_dates,
    _OPEN_STATUSES,
)

# ---------------------------------------------------------------------------
# Asset Health Score (signature feature)
# ---------------------------------------------------------------------------

HEALTH_WEIGHTS = {
    "failure_frequency": 0.30,   # how often it fails
    "mttr_ratio":        0.20,   # repair speed vs fleet average
    "mtbf_ratio":        0.20,   # time between failures vs fleet average
    "open_orders":       0.15,   # unresolved work orders
    "pm_compliance":     0.15,   # preventive maintenance ratio
}


def calculate_asset_health_scores(df: Optional[pd.DataFrame] = None) -> list:
    """
    Composite 0–100 health score per equipment.
    Combines: failure frequency, MTTR ratio, MTBF ratio, open orders, PM rate.
    Returns list sorted by health_score ascending (worst first).
    """
    if not has_data() and df is None:
        return [
            {"equipment": "PUMP-101",   "health_score": 38, "risk_level": "Red",   "details": {}},
            {"equipment": "MOTOR-204",  "health_score": 55, "risk_level": "Amber", "details": {}},
            {"equipment": "BOILER-009", "health_score": 72, "risk_level": "Green", "details": {}},
        ]

    source = df if df is not None else get_normalized_dataframe()
    if source is None or source.empty:
        return []

    equipments = source[source["equipment"].str.strip() != ""]["equipment"].unique()
    if len(equipments) == 0:
        return []

    # Fleet-level baselines
    fleet_mttr = calculate_mttr(source).get("mttr_days") or 5
    fleet_mtbf = calculate_mtbf(source).get("mtbf_days") or 30
    total_orders = len(source)

    results = []
    for eq in equipments:
        eq_df = source[source["equipment"].str.strip() == eq.strip()]

        # --- failure frequency score (0–100, higher = fewer failures)
        eq_count   = len(eq_df)
        max_count  = len(source[source["equipment"].str.strip() != ""].groupby("equipment").size())
        freq_score = max(0, 100 - (eq_count / max(total_orders, 1)) * 100 * 3)

        # --- MTTR ratio score (lower MTTR = higher score)
        eq_mttr_r = calculate_mttr(eq_df)
        eq_mttr   = eq_mttr_r.get("mttr_days") or fleet_mttr
        mttr_score = max(0, min(100, 100 - ((eq_mttr / max(fleet_mttr, 0.1) - 1) * 50)))

        # --- MTBF ratio score (higher MTBF = higher score)
        eq_mtbf_r = calculate_mtbf(eq_df)
        eq_mtbf   = eq_mtbf_r.get("mtbf_days") or fleet_mtbf
        mtbf_score = min(100, max(0, (eq_mtbf / max(fleet_mtbf, 0.1)) * 100 * 0.5))

        # --- open order score (fewer open = higher score)
        open_count  = int(eq_df["status"].apply(_is_open).sum())
        open_score  = max(0, 100 - (open_count / max(eq_count, 1)) * 100)

        # --- PM compliance score (more completed = higher score)
        completed   = int(eq_df["status"].apply(_is_completed).sum())
        pm_score    = round((completed / max(eq_count, 1)) * 100)

        composite = (
            freq_score  * HEALTH_WEIGHTS["failure_frequency"] +
            mttr_score  * HEALTH_WEIGHTS["mttr_ratio"] +
            mtbf_score  * HEALTH_WEIGHTS["mtbf_ratio"] +
            open_score  * HEALTH_WEIGHTS["open_orders"] +
            pm_score    * HEALTH_WEIGHTS["pm_compliance"]
        )
        composite = round(max(0, min(100, composite)))

        risk_level = "Red" if composite < 40 else "Amber" if composite < 70 else "Green"

        results.append({
            "equipment":    eq,
            "health_score": composite,
            "risk_level":   risk_level,
            "details": {
                "failure_count":  eq_count,
                "open_orders":    open_count,
                "completed":      completed,
                "mttr_days":      round(eq_mttr, 1) if eq_mttr else None,
                "mtbf_days":      round(eq_mtbf, 1) if eq_mtbf else None,
                "pm_compliance":  pm_score,
            },
        })

    return sorted(results, key=lambda x: x["health_score"])


# ---------------------------------------------------------------------------
# PM Compliance by Plant
# ---------------------------------------------------------------------------

def pm_compliance_by_plant(df: Optional[pd.DataFrame] = None) -> list:
    """PM completion rate per plant, sorted by compliance ascending (worst first)."""
    if not has_data() and df is None:
        return [
            {"plant": "1000", "compliance_pct": 82, "completed": 45, "total": 55},
            {"plant": "1100", "compliance_pct": 74, "completed": 30, "total": 41},
            {"plant": "1200", "compliance_pct": 68, "completed": 17, "total": 25},
        ]

    source = df if df is not None else get_normalized_dataframe()
    if source is None or source.empty:
        return []

    result = []
    for plant, grp in source.groupby("plant"):
        if not plant.strip():
            continue
        total     = len(grp)
        completed = int(grp["status"].apply(_is_completed).sum())
        result.append({
            "plant":          plant,
            "compliance_pct": round((completed / total) * 100, 1),
            "completed":      completed,
            "total":          total,
        })
    return sorted(result, key=lambda x: x["compliance_pct"])


# ---------------------------------------------------------------------------
# Planner Group Performance
# ---------------------------------------------------------------------------

def planner_group_performance(df: Optional[pd.DataFrame] = None) -> list:
    """Backlog count and compliance rate per planner group."""
    if not has_data() and df is None:
        return [
            {"planner_group": "ME1", "total": 40, "completed": 30, "backlog": 10, "compliance_pct": 75},
            {"planner_group": "ME2", "total": 35, "completed": 22, "backlog": 13, "compliance_pct": 63},
        ]

    source = df if df is not None else get_normalized_dataframe()
    if source is None or source.empty:
        return []

    result = []
    for pg, grp in source[source["planner_group"].str.strip() != ""].groupby("planner_group"):
        total     = len(grp)
        completed = int(grp["status"].apply(_is_completed).sum())
        backlog   = int(grp["status"].apply(_is_open).sum())
        result.append({
            "planner_group":  pg,
            "total":          total,
            "completed":      completed,
            "backlog":        backlog,
            "compliance_pct": round((completed / total) * 100, 1),
        })
    return sorted(result, key=lambda x: x["compliance_pct"])


# ---------------------------------------------------------------------------
# Work Order SLA (overdue analysis)
# ---------------------------------------------------------------------------

def work_order_sla(sla_days: int = 30, df: Optional[pd.DataFrame] = None) -> dict:
    """Count open orders past SLA threshold and breakdown by priority."""
    if not has_data() and df is None:
        return {"sla_days": sla_days, "overdue_count": 14, "on_time_count": 44, "overdue_by_priority": [], "source": "demo"}

    source = df if df is not None else get_normalized_dataframe()
    if source is None or source.empty:
        return {"sla_days": sla_days, "overdue_count": 0, "on_time_count": 0, "overdue_by_priority": [], "source": "uploaded"}

    open_df = source[source["status"].apply(_is_open)].copy()
    open_df["_start"] = _parse_dates(open_df["created_on"])
    open_df = open_df.dropna(subset=["_start"])
    today = pd.Timestamp(datetime.today().date())
    open_df["_age"] = (today - open_df["_start"]).dt.days.fillna(0)

    overdue    = open_df[open_df["_age"] > sla_days]
    on_time    = open_df[open_df["_age"] <= sla_days]

    by_priority = (
        overdue.groupby("priority").size().reset_index(name="count")
        .sort_values("count", ascending=False)
        .to_dict(orient="records")
    ) if not overdue.empty else []

    return {
        "sla_days":           sla_days,
        "overdue_count":      len(overdue),
        "on_time_count":      len(on_time),
        "overdue_by_priority": by_priority,
        "source":             "uploaded",
    }


# ---------------------------------------------------------------------------
# Repeat Failure Analysis
# ---------------------------------------------------------------------------

def repeat_failure_analysis(min_failures: int = 3, df: Optional[pd.DataFrame] = None) -> list:
    """Equipment with recurring failures — chronic issues indicator."""
    if not has_data() and df is None:
        return [
            {"equipment": "PUMP-101",  "failures": 12, "repeat_rate_pct": 80, "risk": "High"},
            {"equipment": "MOTOR-204", "failures": 9,  "repeat_rate_pct": 67, "risk": "Medium"},
        ]

    source = df if df is not None else get_normalized_dataframe()
    if source is None or source.empty:
        return []

    freq = (
        source[source["equipment"].str.strip() != ""]
        .groupby("equipment").size().reset_index(name="failures")
    )
    chronic = freq[freq["failures"] >= min_failures].sort_values("failures", ascending=False)

    max_f = chronic["failures"].max() if not chronic.empty else 1
    result = []
    for _, row in chronic.iterrows():
        rate = round((row["failures"] / max_f) * 100)
        risk = "Critical" if rate > 75 else "High" if rate > 50 else "Medium"
        result.append({
            "equipment":        row["equipment"],
            "failures":         int(row["failures"]),
            "repeat_rate_pct":  rate,
            "risk":             risk,
        })
    return result


# ---------------------------------------------------------------------------
# MTTR Trend (by month/period from created_on)
# ---------------------------------------------------------------------------

def mttr_trend(df: Optional[pd.DataFrame] = None) -> list:
    """Monthly MTTR trend — shows whether repair times are improving."""
    if not has_data() and df is None:
        months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
        values = [4.2, 3.8, 5.1, 3.5, 3.2, 2.9]
        return [{"period": m, "mttr_days": v} for m, v in zip(months, values)]

    source = df if df is not None else get_normalized_dataframe()
    if source is None or source.empty:
        return []

    closed = source[source["status"].apply(_is_completed)].copy()
    closed["_start"] = _parse_dates(closed["created_on"])
    closed["_end"]   = _parse_dates(closed["completed_on"])
    closed = closed.dropna(subset=["_start", "_end"])
    closed = closed[closed["_end"] >= closed["_start"]]

    if closed.empty:
        return []

    closed["_days"]   = (closed["_end"] - closed["_start"]).dt.days
    closed["_period"] = closed["_start"].dt.to_period("M").astype(str)

    trend = (
        closed.groupby("_period")["_days"].mean()
        .reset_index()
        .rename(columns={"_period": "period", "_days": "mttr_days"})
    )
    trend["mttr_days"] = trend["mttr_days"].round(1)
    return trend.sort_values("period").to_dict(orient="records")


# ---------------------------------------------------------------------------
# Equipment Reliability Index
# ---------------------------------------------------------------------------

def equipment_reliability_index(df: Optional[pd.DataFrame] = None) -> list:
    """
    Reliability Index = MTBF / (MTBF + MTTR) × 100
    Values near 100 indicate highly reliable equipment.
    """
    if not has_data() and df is None:
        return [
            {"equipment": "BOILER-009", "reliability_index": 93.1},
            {"equipment": "MOTOR-204",  "reliability_index": 85.7},
            {"equipment": "PUMP-101",   "reliability_index": 72.4},
        ]

    source = df if df is not None else get_normalized_dataframe()
    if source is None or source.empty:
        return []

    equip_df = source[source["equipment"].str.strip() != ""]
    result = []
    for eq, grp in equip_df.groupby("equipment"):
        mttr_r = calculate_mttr(grp)
        mtbf_r = calculate_mtbf(grp)
        mttr   = mttr_r.get("mttr_days") or 0
        mtbf   = mtbf_r.get("mtbf_days") or 0
        if mtbf + mttr > 0:
            ri = round((mtbf / (mtbf + mttr)) * 100, 1)
        else:
            ri = None
        result.append({"equipment": eq, "reliability_index": ri})

    return sorted(
        [r for r in result if r["reliability_index"] is not None],
        key=lambda x: x["reliability_index"],
        reverse=True,
    )
