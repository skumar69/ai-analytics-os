from __future__ import annotations

from backend.semantic.dictionary import SEMANTIC_DICTIONARY


class SemanticEngine:
    """Map raw columns to canonical semantic names."""

    def detect(self, columns):
        matches = {}
        normalized = [str(column).strip().lower() for column in columns]

        for canonical_name, aliases in SEMANTIC_DICTIONARY.items():
            alias_set = {str(alias).strip().lower() for alias in aliases}
            for raw_name in normalized:
                if raw_name in alias_set:
                    matches[raw_name] = canonical_name
                    break
        return matches
