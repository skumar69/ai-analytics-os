from __future__ import annotations


class KPIGenerationEngine:
    """Generate core KPIs from a semantic dataset."""

    def generate(self, df):
        result = {}
        if df is None or df.empty:
            return result

        if "priority" in df.columns:
            result["priority_distribution"] = df["priority"].value_counts().to_dict()
        if "incident_open_date" in df.columns:
            result["record_count"] = len(df)
        return result
