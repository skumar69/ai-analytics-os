from typing import Optional
import pandas as pd

_uploaded_df: Optional[pd.DataFrame] = None


def set_dataframe(df: pd.DataFrame):
    global _uploaded_df
    _uploaded_df = df.copy()


def get_dataframe() -> Optional[pd.DataFrame]:
    return _uploaded_df


def has_data() -> bool:
    return _uploaded_df is not None


def row_count() -> int:
    return 0 if _uploaded_df is None else len(_uploaded_df)


def column_count() -> int:
    return 0 if _uploaded_df is None else len(_uploaded_df.columns)


def columns() -> list:
    return [] if _uploaded_df is None else list(_uploaded_df.columns)
