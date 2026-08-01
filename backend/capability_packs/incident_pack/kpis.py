from __future__ import annotations


def compute_incident_kpis(df):
    """Return a simple KPI summary for incident data."""
    if df is None or df.empty:
        return {
            "total_incidents": 0,
            "open_incidents": 0,
            "resolved_incidents": 0,
        }

    total_incidents = len(df)
    open_incidents = int((df["state"].astype(str).str.lower() == "open").sum()) if "state" in df.columns else 0
    resolved_incidents = int((df["state"].astype(str).str.lower() == "resolved").sum()) if "state" in df.columns else 0

    return {
        "total_incidents": total_incidents,
        "open_incidents": open_incidents,
        "resolved_incidents": resolved_incidents,
    }
