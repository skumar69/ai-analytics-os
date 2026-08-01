from __future__ import annotations


class KPIEngine:
    """Generate KPI summaries for the enriched dataset."""

    def calculate(self, df):
        kpis = {}
        if df is None or df.empty:
            return kpis

        if "priority" in df.columns:
            kpis["priority_distribution"] = df["priority"].value_counts().to_dict()
        kpis["row_count"] = len(df)
        return kpis
