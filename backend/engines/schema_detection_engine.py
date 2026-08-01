from __future__ import annotations


class SchemaDetectionEngine:
    """Inspect a data frame and summarize its schema."""

    def detect_schema(self, df):
        return {
            "row_count": len(df),
            "column_count": len(df.columns),
            "columns": list(df.columns),
            "dtypes": {str(column): str(dtype) for column, dtype in df.dtypes.items()},
        }
