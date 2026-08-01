from pathlib import Path

import pandas as pd


class SchemaAgent:
    def __init__(self, file_path):
        self.file_path = self._resolve_file_path(file_path)

    @staticmethod
    def _resolve_file_path(file_path):
        path = Path(file_path)
        if path.is_absolute():
            return path

        candidates = [
            Path.cwd() / path,
            Path(__file__).resolve().parents[2] / path,
            Path(__file__).resolve().parents[2] / "sample_data" / path.name,
        ]

        for candidate in candidates:
            if candidate.exists():
                return candidate

        return path

    def detect_schema(self):
        if not self.file_path.exists():
            raise FileNotFoundError(f"File not found: {self.file_path}")

        if self.file_path.suffix.lower() == ".csv":
            df = pd.read_csv(self.file_path)
        else:
            df = pd.read_excel(self.file_path)

        print("=" * 60)
        print("AI Analytics Operating System")
        print("Schema Detection Agent")
        print("=" * 60)

        print(f"\nDataset : {self.file_path.name}")
        print(f"Rows    : {len(df)}")
        print(f"Columns : {len(df.columns)}")

        print("\nDetected Columns")
        print("-" * 60)

        for col in df.columns:
            dtype = str(df[col].dtype)

            if "datetime" in dtype:
                data_type = "Date"
            elif "int" in dtype or "float" in dtype:
                data_type = "Numeric"
            else:
                data_type = "Text"

            print(f"{col:30} --> {data_type}")

        return df


if __name__ == "__main__":
    default_file = Path(__file__).resolve().parents[2] / "sample_data" / "sap_incident_data_100_rows.xlsx"
    agent = SchemaAgent(str(default_file))
    agent.detect_schema()