from __future__ import annotations


def build_incident_dashboard_summary(df):
    """Return a minimal dashboard-ready summary object."""
    if df is None:
        return {"status": "empty", "summary": {}}

    return {
        "status": "ok",
        "summary": {
            "rows": len(df),
            "columns": len(df.columns),
            "priority_breakdown": df["priority"].value_counts().to_dict() if "priority" in df.columns else {},
        },
    }
