from __future__ import annotations


class SemanticEnrichmentEngine:
    """Apply semantic corrections and direct enrichments to a dataset."""

    def enrich(self, df, semantic_map):
        enriched = df.copy()
        for canonical_name, alias_key in semantic_map.items():
            if alias_key in enriched.columns:
                enriched[canonical_name] = enriched[alias_key]
        return enriched
