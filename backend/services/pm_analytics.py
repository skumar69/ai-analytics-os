from datetime import datetime
from typing import Optional
import pandas as pd
from services.data_service import get_normalized_dataframe, has_data

_COMPLETED_STATUSES = {"completed", "closed", "clsd", "teco", "technically completed"}
_OPEN_STATUSES = {"open", "in progress", "created", "released", "partially released"}
_BREAKDOWN_TYPES = {"breakdown", "corrective", "cm", "zm01", "zm02", "reactive"}


def _parse_dates(series: pd.Series) -> pd.Series:
    return pd.to_datetime(series, errors="coerce", dayfirst=False)


def _is_completed(status: str) -> bool:
    return status.strip().lower() in _COMPLETED_STATUSES


def _is_open(status: str) -> bool:
    return status.strip().lower() in _OPEN_STATUSES or (
        status.strip() != "" and not _is_completed(status)
    )


def _resolve(df: Optional[pd.DataFrame]) -> Optional[pd.DataFrame]:
    """Return the provided df, or fall back to the global normalized dataframe."""
    return df if df is not None else get_normalized_dataframe()


def calculate_mttr(df: Optional[pd.DataFrame] = None) -> dict:
    if df is None and not has_data():
        return {"mttr_days": 3.2, "sample_size": 0, "source": "demo"}

    df = _resolve(df)[df["status"].apply(_is_completed)].copy() if _resolve(df) is not None else pd.DataFrame()
    df["_start"] = _parse_dates(df["created_on"])
    df["_end"]   = _parse_dates(df["completed_on"])
    df = df.dropna(subset=["_start", "_end"])
    df = df[df["_end"] >= df["_start"]]

    if df.empty:
        return {"mttr_days": None, "sample_size": 0, "source": "uploaded", "note": "No date pairs found"}

    df["_days"] = (df["_end"] - df["_start"]).dt.days
    return {"mttr_days": round(df["_days"].mean(), 1), "sample_size": len(df), "source": "uploaded"}


def calculate_mtbf(df: Optional[pd.DataFrame] = None) -> dict:
    if df is None and not has_data():
        return {"mtbf_days": 45.0, "sample_size": 0, "source": "demo"}

    df = _resolve(df).copy()
    df["_date"] = _parse_dates(df["created_on"])
    df = df.dropna(subset=["_date"]).loc[df["equipment"].str.strip() != ""]

    gaps = []
    for _, grp in df.groupby("equipment"):
        dates = grp["_date"].sort_values()
        if len(dates) > 1:
            gaps.extend(dates.diff().dropna().dt.days.tolist())

    if not gaps:
        return {"mtbf_days": None, "sample_size": 0, "source": "uploaded", "note": "Insufficient failure history"}

    return {"mtbf_days": round(sum(gaps) / len(gaps), 1), "sample_size": len(gaps), "source": "uploaded"}


def calculate_pm_compliance(df: Optional[pd.DataFrame] = None) -> dict:
    if df is None and not has_data():
        return {"compliance_pct": 78.0, "completed": 0, "total": 0, "source": "demo"}

    df = _resolve(df)
    total = len(df)
    if total == 0:
        return {"compliance_pct": 0, "completed": 0, "total": 0, "source": "uploaded"}

    completed = int(df["status"].apply(_is_completed).sum())
    return {
        "compliance_pct": round((completed / total) * 100, 1),
        "completed": completed,
        "total": total,
        "source": "uploaded",
    }


def calculate_breakdown_percentage(df: Optional[pd.DataFrame] = None) -> dict:
    if df is None and not has_data():
        return {"breakdown_pct": 22.0, "breakdown_count": 0, "total": 0, "source": "demo"}

    df = _resolve(df)
    total = len(df)
    if total == 0:
        return {"breakdown_pct": 0, "breakdown_count": 0, "total": 0, "source": "uploaded"}

    is_bd = df["maintenance_type"].str.lower().str.strip().isin(_BREAKDOWN_TYPES)
    if is_bd.sum() == 0:
        is_bd = df["priority"].str.strip().str.lower() == "critical"

    count = int(is_bd.sum())
    return {
        "breakdown_pct": round((count / total) * 100, 1),
        "breakdown_count": count,
        "total": total,
        "source": "uploaded",
    }


def calculate_backlog(df: Optional[pd.DataFrame] = None) -> dict:
    if df is None and not has_data():
        return {"total_backlog": 58, "by_plant": [], "by_planner_group": [], "source": "demo"}

    df = _resolve(df)
    open_df = df[df["status"].apply(_is_open)]

    by_plant = (
        open_df.groupby("plant").size().reset_index(name="count")
        .sort_values("count", ascending=False).to_dict(orient="records")
    )
    by_planner = (
        open_df[open_df["planner_group"].str.strip() != ""]
        .groupby("planner_group").size().reset_index(name="count")
        .sort_values("count", ascending=False).to_dict(orient="records")
    )
    return {
        "total_backlog": len(open_df),
        "by_plant": by_plant,
        "by_planner_group": by_planner,
        "source": "uploaded",
    }


def calculate_work_order_age(df: Optional[pd.DataFrame] = None) -> dict:
    if df is None and not has_data():
        return {"avg_age_days": 12.0, "max_age_days": 45, "buckets": [], "source": "demo"}

    df = _resolve(df)
    open_df = df[df["status"].apply(_is_open)].copy()
    open_df["_start"] = _parse_dates(open_df["created_on"])
    open_df = open_df.dropna(subset=["_start"])

    today = pd.Timestamp(datetime.today().date())
    open_df["_age"] = (today - open_df["_start"]).dt.days
    open_df = open_df[open_df["_age"] >= 0]

    if open_df.empty:
        return {"avg_age_days": None, "max_age_days": None, "buckets": [], "source": "uploaded"}

    a = open_df["_age"]
    return {
        "avg_age_days": round(float(a.mean()), 1),
        "max_age_days": int(a.max()),
        "buckets": [
            {"range": "0–7 days",   "count": int((a <= 7).sum())},
            {"range": "8–30 days",  "count": int(((a > 7) & (a <= 30)).sum())},
            {"range": "31–90 days", "count": int(((a > 30) & (a <= 90)).sum())},
            {"range": "90+ days",   "count": int((a > 90).sum())},
        ],
        "source": "uploaded",
    }


def calculate_failure_frequency(df: Optional[pd.DataFrame] = None) -> list:
    if df is None and not has_data():
        return [
            {"equipment": "Pump-101",  "failures": 12},
            {"equipment": "Motor-204", "failures": 9},
            {"equipment": "Boiler-009","failures": 7},
        ]

    df = _resolve(df)
    df = df[df["equipment"].str.strip() != ""]
    counts = df.groupby("equipment").size().reset_index(name="failures")
    return counts.sort_values("failures", ascending=False).to_dict(orient="records")


def calculate_top_failed_equipment(n: int = 10, df: Optional[pd.DataFrame] = None) -> list:
    return calculate_failure_frequency(df)[:n]


def calculate_equipment_health(df: Optional[pd.DataFrame] = None) -> list:
    if df is None and not has_data():
        return [
            {"equipment": "Pump-101",  "health_score": 42, "risk": "Critical"},
            {"equipment": "Motor-204", "health_score": 58, "risk": "High"},
            {"equipment": "Boiler-009","health_score": 39, "risk": "Critical"},
        ]

    failures = calculate_failure_frequency(df)
    if not failures:
        return []

    max_f = max(r["failures"] for r in failures) or 1
    result = []
    for row in failures:
        score = max(0, round(100 - (row["failures"] / max_f) * 100))
        risk = "Critical" if score < 40 else "High" if score < 60 else "Medium" if score < 80 else "Low"
        result.append({"equipment": row["equipment"], "health_score": score, "risk": risk})

    return sorted(result, key=lambda x: x["health_score"])


def calculate_asset_criticality(df: Optional[pd.DataFrame] = None) -> list:
    PRIORITY_WEIGHT = {"critical": 4, "high": 3, "medium": 2, "low": 1}

    if df is None and not has_data():
        return [
            {"equipment": "Pump-101",  "criticality_score": 92.0, "failure_count": 12},
            {"equipment": "Motor-204", "criticality_score": 74.0, "failure_count": 9},
            {"equipment": "Boiler-009","criticality_score": 68.0, "failure_count": 7},
        ]

    df = _resolve(df)
    df = df[df["equipment"].str.strip() != ""].copy()
    df["_pw"] = df["priority"].str.lower().str.strip().map(PRIORITY_WEIGHT).fillna(1)

    scored = (
        df.groupby("equipment")
        .agg(failure_count=("equipment", "count"), avg_weight=("_pw", "mean"))
        .reset_index()
    )
    max_fc = scored["failure_count"].max() or 1
    scored["criticality_score"] = (
        (scored["failure_count"] / max_fc * 60) + (scored["avg_weight"] / 4 * 40)
    ).round(1)
    return (
        scored.sort_values("criticality_score", ascending=False)
        [["equipment", "criticality_score", "failure_count"]]
        .to_dict(orient="records")
    )


def get_equipment_detail(equipment: str) -> dict:
    """Return all work orders for a specific equipment (for drill-down)."""
    if not has_data():
        return {"equipment": equipment, "work_orders": []}

    df = get_normalized_dataframe()
    rows = df[df["equipment"].str.strip().str.lower() == equipment.strip().lower()]
    work_orders = rows[["work_order", "status", "priority", "created_on", "completed_on", "description"]].copy()
    work_orders = work_orders.replace("", None)
    return {
        "equipment": equipment,
        "total": len(rows),
        "work_orders": work_orders.to_dict(orient="records"),
    }

