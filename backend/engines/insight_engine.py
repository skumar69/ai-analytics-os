from __future__ import annotations


class InsightEngine:
    """Create human-readable insights from a dataset summary."""

    def generate(self, df, kpis):
        insights = []
        if df is None or df.empty:
            return ["No data available for insights."]

        insights.append(f"Dataset contains {len(df)} records.")
        if kpis:
            insights.append("KPI summary generated successfully.")
        return insights
