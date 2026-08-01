from __future__ import annotations


class ReportGenerator:
    """Generate final report payload from all engine outputs."""

    def generate(self, df, schema, semantic_map, packs, kpis, dashboard, insights):
        return {
            "schema": schema,
            "semantic_map": semantic_map,
            "capability_packs": packs,
            "kpis": kpis,
            "dashboard": dashboard,
            "insights": insights,
            "record_count": len(df) if df is not None else 0,
        }
