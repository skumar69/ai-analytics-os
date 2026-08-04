import pandas as pd

# Maps VisionIQ standard field → list of known SAP column variants (case-insensitive)
FIELD_MAP: dict[str, list[str]] = {
    "equipment":          ["equipment", "equip no", "equipment number", "equip_no"],
    "plant":              ["plant", "maintenance plant", "planning plant"],
    "notification":       ["notification", "notification no", "notification_no", "notif. no"],
    "work_order":         ["order", "order number", "work order", "order_no", "pm order"],
    "priority":           ["priority", "order priority"],
    "status":             ["system status", "user status", "status", "order status"],
    "planner_group":      ["planner group", "planner_group", "planning group"],
    "functional_location":["functional location", "func. loc.", "functional_location", "floc"],
    "order_type":         ["order type", "order_type", "pm order type"],
    "created_on":         ["created on", "created_on", "creation date", "basic start date"],
    "completed_on":       ["basic finish date", "actual finish", "actual finish date",
                           "completed on", "end date"],
    "description":        ["description", "short text", "order description", "notif. text"],
    "maintenance_type":   ["maintenance activity type", "activity type", "maint. act. type",
                           "maintenance_type", "maint type"],
}


def _find_column(df: pd.DataFrame, candidates: list[str]) -> str | None:
    """Return the first df column that matches any candidate (case-insensitive)."""
    lower_cols = {c.lower(): c for c in df.columns}
    for candidate in candidates:
        if candidate.lower() in lower_cols:
            return lower_cols[candidate.lower()]
    return None


def normalize(df: pd.DataFrame) -> pd.DataFrame:
    """
    Return a new DataFrame with standardized VisionIQ column names.
    Missing fields are added as empty strings so downstream engines
    can assume every standard field exists.
    """
    normalized = pd.DataFrame()

    for field, candidates in FIELD_MAP.items():
        source_col = _find_column(df, candidates)
        if source_col:
            normalized[field] = df[source_col].fillna("").astype(str)
        else:
            normalized[field] = ""

    # Preserve any extra columns not in the map (prefixed to avoid clashes)
    mapped_sources = {
        _find_column(df, candidates)
        for candidates in FIELD_MAP.values()
        if _find_column(df, candidates)
    }
    for col in df.columns:
        if col not in mapped_sources:
            normalized[f"_raw_{col}"] = df[col]

    return normalized


def get_mapped_columns(df: pd.DataFrame) -> dict[str, str | None]:
    """Return which source column each VisionIQ field resolved to (for debugging)."""
    return {
        field: _find_column(df, candidates)
        for field, candidates in FIELD_MAP.items()
    }
