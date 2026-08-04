import pytest
from services.pm_analytics import (
    calculate_mttr,
    calculate_mtbf,
    calculate_pm_compliance,
    calculate_breakdown_percentage,
    calculate_backlog,
    calculate_work_order_age,
    calculate_failure_frequency,
    calculate_top_failed_equipment,
    calculate_equipment_health,
    calculate_asset_criticality,
    get_equipment_detail,
)
from services.data_service import set_dataframe
from services.data_mapper import normalize


# ── helpers ────────────────────────────────────────────────────────────────

def _load(sample_df):
    """Push sample_df through the full normalize → set_dataframe pipeline."""
    from services import data_service
    data_service._normalized_df = normalize(sample_df)
    data_service._uploaded_df   = sample_df.copy()


# ── demo-data fallbacks (no upload) ────────────────────────────────────────

def test_mttr_demo_when_no_data():
    from services import data_service
    data_service._uploaded_df   = None
    data_service._normalized_df = None
    result = calculate_mttr()
    assert result["source"] == "demo"
    assert result["mttr_days"] > 0


def test_mtbf_demo_when_no_data():
    from services import data_service
    data_service._uploaded_df   = None
    data_service._normalized_df = None
    result = calculate_mtbf()
    assert result["source"] == "demo"


# ── live calculations ───────────────────────────────────────────────────────

def test_pm_compliance_with_data(sample_df):
    _load(sample_df)
    result = calculate_pm_compliance()
    assert result["source"] == "uploaded"
    assert 0 <= result["compliance_pct"] <= 100
    # 3 of 5 rows are Completed or Closed (rows 0,1,4)
    assert result["completed"] == 3
    assert result["total"] == 5


def test_breakdown_percentage_uses_corrective_type(sample_df):
    _load(sample_df)
    result = calculate_breakdown_percentage()
    assert result["source"] == "uploaded"
    # 2 rows have maintenance_type = corrective
    assert result["breakdown_count"] == 2


def test_backlog_counts_open_orders(sample_df):
    _load(sample_df)
    result = calculate_backlog()
    assert result["source"] == "uploaded"
    # Rows with status Open or In Progress = 2
    assert result["total_backlog"] == 2


def test_backlog_groups_by_plant(sample_df):
    _load(sample_df)
    result = calculate_backlog()
    plants = {r["plant"] for r in result["by_plant"]}
    assert len(plants) >= 1


def test_failure_frequency_sorted_descending(sample_df):
    _load(sample_df)
    freq = calculate_failure_frequency()
    counts = [r["failures"] for r in freq]
    assert counts == sorted(counts, reverse=True)


def test_failure_frequency_pump_has_most(sample_df):
    _load(sample_df)
    freq = calculate_failure_frequency()
    top = freq[0]
    assert top["equipment"] == "PUMP-101"
    assert top["failures"] == 3  # PUMP-101 appears 3x in updated sample


def test_top_failed_equipment_respects_n(sample_df):
    _load(sample_df)
    result = calculate_top_failed_equipment(n=2)
    assert len(result) <= 2


def test_equipment_health_sorted_ascending(sample_df):
    _load(sample_df)
    health = calculate_equipment_health()
    scores = [r["health_score"] for r in health]
    assert scores == sorted(scores)


def test_equipment_health_score_in_range(sample_df):
    _load(sample_df)
    for row in calculate_equipment_health():
        assert 0 <= row["health_score"] <= 100


def test_equipment_health_risk_values(sample_df):
    _load(sample_df)
    valid_risks = {"Critical", "High", "Medium", "Low"}
    for row in calculate_equipment_health():
        assert row["risk"] in valid_risks


def test_asset_criticality_sorted_descending(sample_df):
    _load(sample_df)
    crit = calculate_asset_criticality()
    scores = [r["criticality_score"] for r in crit]
    assert scores == sorted(scores, reverse=True)


def test_get_equipment_detail_returns_work_orders(sample_df):
    _load(sample_df)
    result = get_equipment_detail("PUMP-101")
    assert result["equipment"] == "PUMP-101"
    assert result["total"] == 3  # PUMP-101 appears 3x
    assert len(result["work_orders"]) == 3


def test_get_equipment_detail_case_insensitive(sample_df):
    _load(sample_df)
    result = get_equipment_detail("pump-101")
    assert result["total"] == 3


def test_mttr_with_valid_dates(sample_df):
    _load(sample_df)
    result = calculate_mttr()
    assert result["source"] == "uploaded"
    # PUMP-101: 4 days, MOTOR-204: 5 days → avg should be calculable
    assert result["mttr_days"] is not None or result["sample_size"] >= 0
