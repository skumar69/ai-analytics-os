import pandas as pd

from backend.engines.enrichment_engine import EnrichmentEngine
from backend.engines.kpi_engine import KPIEngine


def test_enrichment_engine_generates_semantic_business_fields():
    df = pd.DataFrame(
        {
            "Incident Number": ["INC-100", "INC-101", "INC-102"],
            "Opened": ["2024-01-15", "2024-02-03", "2024-03-07"],
            "Resolved": ["2024-01-17", "2024-02-10", "2024-03-12"],
            "Priority": ["Critical", "High", "Medium"],
            "State": ["Open", "Closed", "Closed"],
            "Assignment Group": ["Network", "Database", "Network"],
            "Manager": ["A. Singh", "N. Patel", "K. Gomez"],
        }
    )

    result = EnrichmentEngine().enrich(
        df,
        {
            "opened": "incident_open_date",
            "resolved": "incident_close_date",
            "priority": "priority",
            "state": "state",
            "assignment group": "assignment_group",
            "manager": "manager",
        },
    )

    assert "incident_open_date" in result.columns
    assert "incident_close_date" in result.columns
    assert "trend_month" in result.columns
    assert "trend_year" in result.columns
    assert "resolution_days" in result.columns
    assert "priority_bucket" in result.columns
    assert "critical_flag" in result.columns


def test_kpi_engine_recommends_business_metrics_and_charts():
    df = pd.DataFrame(
        {
            "incident_open_date": pd.to_datetime(["2024-01-01", "2024-01-15", "2024-02-10"]),
            "incident_close_date": pd.to_datetime(["2024-01-04", "2024-01-18", "2024-02-19"]),
            "priority": ["Critical", "High", "Medium"],
            "assignment_group": ["Network", "Network", "Database"],
            "state": ["Open", "Closed", "Closed"],
        }
    )

    report = KPIEngine().calculate(df)

    assert "open_incidents" in report
    assert "average_resolution_days" in report
    assert "critical_tickets" in report
    assert "recommended_charts" in report
    assert "recommended_filters" in report
    assert isinstance(report["recommended_charts"], list)
    assert isinstance(report["recommended_filters"], list)
