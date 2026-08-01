from __future__ import annotations


class ReportEngine:
    """Assemble the final analytics report."""

    def build(self, df, schema, semantic_map, kpis, dashboard, insights):
        return {
            "schema": schema,
            "semantic_map": semantic_map,
            "kpis": kpis,
            "dashboard": dashboard,
            "insights": insights,
            "record_count": len(df) if df is not None else 0,
        }
