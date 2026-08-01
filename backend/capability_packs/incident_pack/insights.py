from __future__ import annotations


def generate_incident_insights(df):
    """Return a basic insight list for incident data."""
    if df is None or df.empty:
        return ["No incident data available."]

    insights = [f"Total incidents analyzed: {len(df)}"]
    if "priority" in df.columns:
        top_priority = df["priority"].astype(str).mode().iloc[0] if not df["priority"].empty else "unknown"
        insights.append(f"Most common priority: {top_priority}")
    return insights
