import io
import pandas as pd
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def _make_excel(data: dict) -> bytes:
    buf = io.BytesIO()
    pd.DataFrame(data).to_excel(buf, index=False)
    buf.seek(0)
    return buf.read()


def test_upload_valid_excel():
    xlsx = _make_excel({
        "Equipment": ["PUMP-101", "MOTOR-204"],
        "Plant": ["1000", "1100"],
        "Priority": ["Critical", "High"],
        "System Status": ["Open", "Completed"],
    })
    res = client.post(
        "/upload",
        files={"file": ("test.xlsx", xlsx, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")},
    )
    assert res.status_code == 200
    data = res.json()
    assert data["success"] is True
    assert data["rows"] == 2
    assert "Equipment" in data["columns"]


def test_upload_rejects_non_excel():
    res = client.post(
        "/upload",
        files={"file": ("data.csv", b"col1,col2\nval1,val2", "text/csv")},
    )
    assert res.status_code == 400


def test_upload_then_stats_reflects_data():
    xlsx = _make_excel({
        "Equipment": [f"EQ-{i}" for i in range(20)],
        "Plant": ["1000"] * 20,
    })
    client.post(
        "/upload",
        files={"file": ("data.xlsx", xlsx, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")},
    )
    stats = client.get("/stats").json()
    assert stats["work_orders"] == 20


def test_upload_then_analytics_uses_data():
    xlsx = _make_excel({
        "Equipment": ["PUMP-101"] * 5 + ["MOTOR-204"] * 3,
        "Plant": ["1000"] * 8,
        "System Status": ["Open"] * 8,
    })
    client.post(
        "/upload",
        files={"file": ("data.xlsx", xlsx, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")},
    )
    failures = client.get("/analytics/top-failures").json()
    assert failures[0]["equipment"] == "PUMP-101"
    assert failures[0]["failures"] == 5
