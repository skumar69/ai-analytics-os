import sys
from pathlib import Path
import pytest
import pandas as pd

# Ensure backend/ is on the path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))


@pytest.fixture
def sample_df():
    """Minimal normalized DataFrame for unit tests."""
    return pd.DataFrame({
        "equipment":           ["PUMP-101", "PUMP-101", "PUMP-101", "MOTOR-204", "BOILER-009"],
        "plant":               ["1000", "1000", "1000", "1100", "1200"],
        "notification":        ["N001", "N002", "N003", "N004", "N005"],
        "work_order":          ["WO001", "WO002", "WO003", "WO004", "WO005"],
        "priority":            ["Critical", "Critical", "High", "Critical", "Medium"],
        "status":              ["Completed", "Closed", "Open", "In Progress", "Completed"],
        "planner_group":       ["ME1", "ME1", "ME2", "ME1", "ME2"],
        "functional_location": ["FL-1", "FL-1", "FL-2", "FL-3", "FL-2"],
        "order_type":          ["PM01", "PM01", "CM01", "PM01", "CM01"],
        "created_on":          ["2024-01-10", "2024-02-15", "2024-03-01", "2024-04-05", "2024-05-10"],
        "completed_on":        ["2024-01-14", "2024-02-18", "", "2024-04-07", "2024-05-15"],
        "description":         ["Pump overhaul", "Bearing check", "Pump check", "Motor repair", "Boiler inspection"],
        "maintenance_type":    ["", "", "corrective", "", "corrective"],
    })
