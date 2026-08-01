import pandas as pd

from backend.engines.schema_engine import SchemaEngine


def test_schema_engine_detects_rows_and_columns():
    df = pd.DataFrame({
        "opened": ["2024-01-01", "2024-01-02"],
        "priority": ["high", "medium"],
    })

    result = SchemaEngine().detect(df)

    assert result["rows"] == 2
    assert result["columns"] == 2
    assert "opened" in result["column_names"]
    assert "priority" in result["column_names"]
