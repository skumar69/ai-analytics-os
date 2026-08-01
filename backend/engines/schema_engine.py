from __future__ import annotations


class SchemaEngine:
    """Summarize the raw dataset schema."""

    def detect(self, df):
        return {
            "rows": len(df),
            "columns": len(df.columns),
            "column_names": list(df.columns),
            "dtypes": {str(col): str(dtype) for col, dtype in df.dtypes.items()},
        }
