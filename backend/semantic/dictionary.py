from __future__ import annotations

from pathlib import Path

SEMANTIC_DICTIONARY = {
    "incident_open_date": [
        "opened",
        "open date",
        "created",
        "creation date",
        "incident opened",
    ],
    "incident_close_date": [
        "resolved",
        "closed",
        "resolution date",
        "closed date",
    ],
    "priority": [
        "priority",
        "severity",
        "impact",
    ],
    "assignment_group": [
        "assignment group",
        "support group",
    ],
    "manager": [
        "manager",
        "ns manager",
    ],
}


class SemanticDictionary:
    """Stores canonical field mappings and description metadata for business data."""

    def __init__(self, file_path: str | Path | None = None):
        self.file_path = Path(file_path) if file_path is not None else None
        self.dictionary = dict(SEMANTIC_DICTIONARY)

    def add_term(self, canonical_name: str, aliases: list[str]):
        self.dictionary[canonical_name] = aliases

    def get_aliases(self, canonical_name: str):
        return self.dictionary.get(canonical_name, [])

    def get_all(self):
        return dict(self.dictionary)

    def save_to_file(self, output_path: str | Path):
        out_path = Path(output_path)
        out_path.parent.mkdir(parents=True, exist_ok=True)

        with out_path.open("w", encoding="utf-8") as handle:
            for canonical_name, aliases in self.dictionary.items():
                handle.write(f"{canonical_name}: {', '.join(aliases)}\n")

    def load_from_file(self, input_path: str | Path):
        in_path = Path(input_path)
        if not in_path.exists():
            raise FileNotFoundError(f"Dictionary file not found: {in_path}")

        self.dictionary = {}
        with in_path.open("r", encoding="utf-8") as handle:
            for line in handle:
                line = line.strip()
                if not line or ":" not in line:
                    continue
                canonical_name, aliases = line.split(":", 1)
                self.dictionary[canonical_name.strip()] = [
                    alias.strip() for alias in aliases.split(",") if alias.strip()
                ]


if __name__ == "__main__":
    dictionary = SemanticDictionary()
    print(dictionary.get_all())
