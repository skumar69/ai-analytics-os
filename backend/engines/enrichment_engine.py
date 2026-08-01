from __future__ import annotations


class EnrichmentEngine:
    """Add semantic aliases or computed fields to the dataset."""

    def enrich(self, df, semantic_map):
        enriched = df.copy()
        for alias_name, canonical_name in semantic_map.items():
            if alias_name in enriched.columns.map(str).str.lower().values:
                original_name = next(
                    col for col in enriched.columns if str(col).strip().lower() == alias_name
                )
                enriched[canonical_name] = enriched[original_name]
        return enriched
