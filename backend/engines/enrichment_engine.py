from __future__ import annotations

import pandas as pd


class EnrichmentEngine:
    """Add semantic aliases or computed fields to the dataset."""

    def enrich(self, df, semantic_map):
        enriched = df.copy()

        for alias_name, canonical_name in semantic_map.items():
            normalized_alias = str(alias_name).strip().lower()
            if normalized_alias in {str(col).strip().lower() for col in enriched.columns}:
                original_name = next(
                    col for col in enriched.columns if str(col).strip().lower() == normalized_alias
                )
                enriched[canonical_name] = enriched[original_name]

        for column_name in [
            "incident_open_date",
            "incident_close_date",
            "opened",
            "resolved",
            "closed",
            "created",
        ]:
            if column_name in enriched.columns:
                enriched[column_name] = pd.to_datetime(enriched[column_name], errors="coerce")

        open_col = None
        close_col = None
        for candidate in ["incident_open_date", "opened", "created"]:
            if candidate in enriched.columns:
                open_col = candidate
                break
        for candidate in ["incident_close_date", "resolved", "closed"]:
            if candidate in enriched.columns:
                close_col = candidate
                break

        if open_col and close_col:
            enriched["trend_month"] = enriched[open_col].dt.to_period("M").astype(str)
            enriched["trend_year"] = enriched[open_col].dt.year.astype(int)
            enriched["month_name"] = enriched[open_col].dt.strftime("%B")
            enriched["open_incident_month"] = enriched[open_col].dt.to_period("M").astype(str)
            enriched["open_incident_year"] = enriched[open_col].dt.year.astype(int)
            enriched["qtr"] = enriched[open_col].dt.quarter.astype(int)
            enriched["financial_quarter"] = enriched["qtr"].astype(str)
            enriched["financial_year"] = enriched[open_col].dt.year.astype(int)
            enriched["weekend"] = enriched[open_col].dt.dayofweek.isin([5, 6]).astype(int)
            enriched["business_day"] = (~enriched[open_col].dt.dayofweek.isin([5, 6])).astype(int)
            enriched["resolution_days"] = (
                (pd.to_datetime(enriched[close_col], errors="coerce") - pd.to_datetime(enriched[open_col], errors="coerce")).dt.days
            )
            enriched["resolution_hours"] = (
                (pd.to_datetime(enriched[close_col], errors="coerce") - pd.to_datetime(enriched[open_col], errors="coerce")).dt.total_seconds() / 3600
            )
            enriched["incident_age"] = (
                pd.Timestamp.now().tz_localize(None) - pd.to_datetime(enriched[open_col], errors="coerce")
            ).dt.days
            enriched["network_age"] = enriched["incident_age"].fillna(0)

        if "priority" in enriched.columns:
            priority_map = {
                "critical": 4,
                "high": 3,
                "medium": 2,
                "low": 1,
            }
            enriched["priority_rank"] = enriched["priority"].str.lower().map(priority_map).fillna(0)
            enriched["priority_weight"] = enriched["priority_rank"]
            enriched["priority_bucket"] = enriched["priority"].str.lower().map(
                {"critical": "Critical", "high": "High", "medium": "Medium", "low": "Low"}
            )
            enriched["critical_flag"] = enriched["priority"].str.lower().eq("critical").astype(int)

        if "state" in enriched.columns:
            enriched["sla_bucket"] = enriched["state"].fillna("Unknown")
            enriched["over_sla"] = enriched["state"].str.lower().eq("open").astype(int)
            enriched["within_sla"] = (~enriched["state"].str.lower().eq("open")).astype(int)

        return enriched
