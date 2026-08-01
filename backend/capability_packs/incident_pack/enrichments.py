from __future__ import annotations


def enrich_incident_dataset(df):
    """Add common incident enrichment fields."""
    if df is None:
        return df
    if "priority" not in df.columns:
        df["priority"] = "medium"
    if "assignment_group" not in df.columns:
        df["assignment_group"] = "unassigned"
    return df
