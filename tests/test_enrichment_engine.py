import pandas as pd

from backend.engines.enrichment_engine import EnrichmentEngine


def test_enrichment_engine_creates_canonical_fields():
    df = pd.DataFrame({
        "Opened": ["2024-01-01", "2024-01-02"],
        "Priority": ["high", "medium"],
    })

    semantic_map = {
        "opened": "incident_open_date",
        "priority": "priority",
    }

    result = EnrichmentEngine().enrich(df, semantic_map)

    assert "incident_open_date" in result.columns
    assert "priority" in result.columns
    assert result["incident_open_date"].tolist() == ["2024-01-01", "2024-01-02"]
