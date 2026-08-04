import io
import pandas as pd
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def _upload(data: dict):
    buf = io.BytesIO()
    pd.DataFrame(data).to_excel(buf, index=False)
    buf.seek(0)
    client.post(
        "/upload",
        files={"file": ("data.xlsx", buf.read(), "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")},
    )


def test_analytics_dashboard_returns_all_keys():
    res = client.get("/analytics/dashboard")
    assert res.status_code == 200
    data = res.json()
    expected = ["mttr", "mtbf", "pm_compliance", "breakdown_percentage",
                "backlog", "work_order_age", "top_failures", "health_scores", "asset_criticality"]
    for key in expected:
        assert key in data, f"Missing key: {key}"


def test_analytics_summary_returns_all_keys():
    res = client.get("/analytics/summary")
    assert res.status_code == 200
    data = res.json()
    for key in ["mttr", "mtbf", "pm_compliance", "breakdown_percentage", "backlog", "work_order_age"]:
        assert key in data


def test_filter_options_empty_before_upload():
    from services import data_service
    data_service._uploaded_df = None
    data_service._normalized_df = None
    res = client.get("/analytics/filter-options")
    assert res.status_code == 200
    assert res.json() == {}


def test_filter_options_after_upload():
    _upload({
        "Equipment": ["PUMP-101", "MOTOR-204"],
        "Plant": ["1000", "1100"],
        "Priority": ["Critical", "High"],
        "System Status": ["Open", "Completed"],
    })
    res = client.get("/analytics/filter-options")
    assert res.status_code == 200
    opts = res.json()
    assert "plants" in opts
    assert "1000" in opts["plants"]


def test_filter_by_plant_reduces_results():
    _upload({
        "Equipment": ["PUMP-101", "PUMP-101", "MOTOR-204"],
        "Plant": ["1000", "1000", "1100"],
        "System Status": ["Open", "Open", "Open"],
    })
    all_failures = client.get("/analytics/failure-frequency").json()
    plant_failures = client.get("/analytics/failure-frequency?plant=1000").json()
    total_all   = sum(r["failures"] for r in all_failures)
    total_plant = sum(r["failures"] for r in plant_failures)
    assert total_plant < total_all


def test_filter_by_priority():
    _upload({
        "Equipment": ["PUMP-101", "PUMP-101", "MOTOR-204"],
        "Plant": ["1000", "1000", "1100"],
        "Priority": ["Critical", "Critical", "High"],
        "System Status": ["Open", "Open", "Open"],
    })
    res = client.get("/analytics/failure-frequency?priority=High")
    data = res.json()
    assert all(r["equipment"] != "PUMP-101" for r in data), "PUMP-101 should be filtered out"


def test_equipment_detail_endpoint():
    _upload({
        "Equipment": ["PUMP-101", "PUMP-101", "MOTOR-204"],
        "Plant": ["1000", "1000", "1100"],
        "System Status": ["Open", "Completed", "Open"],
    })
    res = client.get("/analytics/equipment/PUMP-101")
    assert res.status_code == 200
    data = res.json()
    assert data["total"] == 2
    assert data["equipment"] == "PUMP-101"


def test_export_returns_excel_file():
    _upload({"Equipment": ["PUMP-101"], "Plant": ["1000"]})
    res = client.get("/analytics/export")
    assert res.status_code == 200
    assert "spreadsheetml" in res.headers.get("content-type", "")


def test_health_score_sorted_ascending():
    _upload({
        "Equipment": ["A"] * 5 + ["B"] * 2 + ["C"] * 1,
        "Plant": ["1000"] * 8,
    })
    health = client.get("/analytics/health-score").json()
    scores = [r["health_score"] for r in health]
    assert scores == sorted(scores)


def test_backlog_total_matches_open_orders():
    _upload({
        "Equipment": ["E1", "E2", "E3", "E4"],
        "Plant": ["1000"] * 4,
        "System Status": ["Open", "In Progress", "Completed", "Closed"],
    })
    res = client.get("/analytics/backlog").json()
    # Open + In Progress = 2  (Completed and Closed are not backlog)
    assert res["total_backlog"] == 2
