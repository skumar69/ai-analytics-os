import pandas as pd
from services.data_mapper import normalize, get_mapped_columns, FIELD_MAP


def _make_sap_df(**kwargs):
    base = {
        "Equipment": ["PUMP-101", "MOTOR-204"],
        "Plant": ["1000", "1100"],
        "Order": ["WO001", "WO002"],
        "Priority": ["Critical", "High"],
        "System Status": ["Open", "Completed"],
    }
    base.update(kwargs)
    return pd.DataFrame(base)


def test_normalize_returns_all_standard_fields():
    df = _make_sap_df()
    result = normalize(df)
    for field in FIELD_MAP:
        assert field in result.columns, f"Missing field: {field}"


def test_normalize_maps_equipment_column():
    df = _make_sap_df()
    result = normalize(df)
    assert list(result["equipment"]) == ["PUMP-101", "MOTOR-204"]


def test_normalize_maps_alternate_column_names():
    df = pd.DataFrame({"Equip No": ["E-001"], "Maintenance Plant": ["2000"]})
    result = normalize(df)
    assert result["equipment"].iloc[0] == "E-001"
    assert result["plant"].iloc[0] == "2000"


def test_normalize_fills_missing_fields_with_empty_string():
    df = pd.DataFrame({"Equipment": ["PUMP-101"]})
    result = normalize(df)
    assert result["plant"].iloc[0] == ""
    assert result["priority"].iloc[0] == ""


def test_normalize_preserves_extra_columns_with_raw_prefix():
    df = _make_sap_df(**{"SomeCustomField": ["val1", "val2"]})
    result = normalize(df)
    assert "_raw_SomeCustomField" in result.columns


def test_get_mapped_columns_returns_correct_source():
    df = _make_sap_df()
    mapping = get_mapped_columns(df)
    assert mapping["equipment"] == "Equipment"
    assert mapping["plant"] == "Plant"
    assert mapping["work_order"] == "Order"
    assert mapping["status"] == "System Status"


def test_get_mapped_columns_returns_none_for_missing():
    df = pd.DataFrame({"Equipment": ["X"]})
    mapping = get_mapped_columns(df)
    assert mapping["notification"] is None
    assert mapping["completed_on"] is None
