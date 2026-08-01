from __future__ import annotations

import sys
from pathlib import Path

if __package__ in (None, ""):
    project_root = Path(__file__).resolve().parents[3]
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))

from backend.semantic.dictionary import SEMANTIC_DICTIONARY


def map_semantic_columns(columns):
    """Map a list of raw column names to canonical semantic names when possible."""
    mapped = {}
    normalized_columns = [str(column).strip().lower() for column in columns]

    for canonical_name, aliases in SEMANTIC_DICTIONARY.items():
        alias_set = {alias.lower() for alias in aliases}
        for raw_name in normalized_columns:
            if raw_name in alias_set:
                mapped[raw_name] = canonical_name
                break

    return mapped


if __name__ == "__main__":
    sample_columns = ["Opened", "Priority", "Assignment Group", "NS Manager"]
    print(map_semantic_columns(sample_columns))
