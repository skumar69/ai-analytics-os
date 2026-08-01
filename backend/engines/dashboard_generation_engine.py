from __future__ import annotations


class DashboardGenerationEngine:
    """Prepare data structures for dashboard rendering."""

    def generate(self, df, kpis):
        return {
            "rows": len(df) if df is not None else 0,
            "columns": list(df.columns) if df is not None else [],
            "kpis": kpis,
        }
