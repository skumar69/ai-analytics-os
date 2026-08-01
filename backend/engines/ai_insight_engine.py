from __future__ import annotations


class AIInsightEngine:
    """Produce simple AI-style insight summaries."""

    def generate(self, df, kpis):
        insights = []
        if df is None or df.empty:
            return ["No data available for insight generation."]

        insights.append(f"Analyzed {len(df)} records.")
        if kpis:
            insights.append("KPI summary generated successfully.")
        return insights
