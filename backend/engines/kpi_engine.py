from __future__ import annotations

import pandas as pd


class KPIEngine:
    """Generate KPI summaries and recommendation payloads for the enriched dataset."""

    def calculate(self, df):
        kpis = {}
        if df is None or df.empty:
            return kpis

        kpis["row_count"] = len(df)

        if "state" in df.columns:
            kpis["open_incidents"] = int((df["state"].astype(str).str.lower() == "open").sum())
            kpis["closed_incidents"] = int((df["state"].astype(str).str.lower() == "closed").sum())

        if "resolution_days" in df.columns:
            kpis["average_resolution_days"] = round(df["resolution_days"].fillna(0).mean(), 2)

        if "priority" in df.columns:
            kpis["critical_tickets"] = int((df["priority"].astype(str).str.lower() == "critical").sum())
            kpis["priority_distribution"] = df["priority"].value_counts().to_dict()

        if "assignment_group" in df.columns:
            kpis["top_assignment_groups"] = df["assignment_group"].value_counts().head(5).to_dict()

        if "incident_open_date" in df.columns:
            kpis["monthly_trend"] = df["incident_open_date"].dt.to_period("M").value_counts().sort_index().to_dict()

        if "priority" in df.columns:
            kpis["sla_percent"] = round(
                (df["priority"].astype(str).str.lower().ne("critical").mean() * 100), 2
            ) if len(df) else 0.0

        kpis["network_health"] = "Stable" if kpis.get("open_incidents", 0) < max(1, len(df) * 0.25) else "Watchlist"

        kpis["recommended_charts"] = [
            "Line Chart",
            "Bar Chart",
            "Heat Map",
            "Treemap",
            "Pie",
            "Donut",
            "Gauge",
            "Waterfall",
            "Calendar Heatmap",
        ]

        kpis["recommended_filters"] = [
            "Year",
            "Quarter",
            "Month",
            "Week",
            "Priority",
            "Assignment Group",
            "Manager",
            "Business Unit",
            "Technology",
            "State",
        ]

        return kpis
