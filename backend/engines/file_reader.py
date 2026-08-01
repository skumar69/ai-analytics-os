from __future__ import annotations

from pathlib import Path

import pandas as pd


class FileReader:
    """Load supported file types into a DataFrame."""

    def read(self, file_path: str | Path):
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {path}")

        suffix = path.suffix.lower()
        if suffix == ".csv":
            return pd.read_csv(path)
        if suffix in {".xlsx", ".xls"}:
            return pd.read_excel(path)
        raise ValueError(f"Unsupported format: {suffix}")
