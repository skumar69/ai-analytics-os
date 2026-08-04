from typing import Optional
import pandas as pd
from services.data_mapper import normalize, get_mapped_columns

_uploaded_df: Optional[pd.DataFrame] = None
_normalized_df: Optional[pd.DataFrame] = None
_column_map: dict = {}


def set_dataframe(df: pd.DataFrame):
    global _uploaded_df, _normalized_df, _column_map
    _uploaded_df = df.copy()
    _normalized_df = normalize(df)
    _column_map = get_mapped_columns(df)


def get_dataframe() -> Optional[pd.DataFrame]:
    return _uploaded_df


def get_normalized_dataframe() -> Optional[pd.DataFrame]:
    """Return the upload normalized to VisionIQ standard column names."""
    return _normalized_df


def get_column_map() -> dict:
    """Return which source column each VisionIQ field resolved to."""
    return _column_map


def get_filtered_dataframe(
    plant: str | None = None,
    priority: str | None = None,
    status: str | None = None,
    planner_group: str | None = None,
    date_from: str | None = None,
    date_to: str | None = None,
) -> Optional[pd.DataFrame]:
    """Return normalized DataFrame with optional filters applied."""
    df = _normalized_df
    if df is None:
        return None

    df = df.copy()

    if plant:
        df = df[df["plant"].str.strip().str.lower() == plant.strip().lower()]
    if priority:
        df = df[df["priority"].str.strip().str.lower() == priority.strip().lower()]
    if status:
        df = df[df["status"].str.strip().str.lower() == status.strip().lower()]
    if planner_group:
        df = df[df["planner_group"].str.strip().str.lower() == planner_group.strip().lower()]
    if date_from:
        df = df[pd.to_datetime(df["created_on"], errors="coerce") >= pd.to_datetime(date_from, errors="coerce")]
    if date_to:
        df = df[pd.to_datetime(df["created_on"], errors="coerce") <= pd.to_datetime(date_to, errors="coerce")]

    return df


def get_filter_options() -> dict:
    """Return unique values for each filterable field."""
    if _normalized_df is None:
        return {}
    df = _normalized_df
    return {
        "plants":         sorted(df["plant"].dropna().unique().tolist()),
        "priorities":     sorted(df["priority"].dropna().unique().tolist()),
        "statuses":       sorted(df["status"].dropna().unique().tolist()),
        "planner_groups": sorted(df["planner_group"].dropna().unique().tolist()),
    }


def has_data() -> bool:
    return _uploaded_df is not None


def row_count() -> int:
    return 0 if _uploaded_df is None else len(_uploaded_df)


def column_count() -> int:
    return 0 if _uploaded_df is None else len(_uploaded_df.columns)


def columns() -> list:
    return [] if _uploaded_df is None else list(_uploaded_df.columns)
