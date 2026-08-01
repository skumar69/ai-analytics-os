from __future__ import annotations

from pathlib import Path

import pandas as pd


class FileReaderEngine:
    """Load input files into a DataFrame."""

    def read_file(self, file_path: str | Path):
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Input file not found: {path}")

        suffix = path.suffix.lower()
        if suffix == ".csv":
            return pd.read_csv(path)
        if suffix in {".xlsx", ".xls"}:
            return pd.read_excel(path)
        raise ValueError(f"Unsupported file format: {suffix}")
