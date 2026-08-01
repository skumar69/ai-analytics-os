from __future__ import annotations


class DashboardEngine:
    """Prepare dashboard payloads for downstream rendering."""

    def build(self, df, kpis):
        return {
            "rows": len(df) if df is not None else 0,
            "columns": list(df.columns) if df is not None else [],
            "kpis": kpis,
        }
