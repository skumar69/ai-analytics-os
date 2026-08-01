from __future__ import annotations

import sys
from pathlib import Path

if __package__ in (None, ""):
    project_root = Path(__file__).resolve().parents[3]
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))

from backend.capability_packs.incident_pack.semantic_mapping import map_semantic_columns


def test_mapping_example():
    columns = ["Opened", "Priority", "Assignment Group", "NS Manager"]
    result = map_semantic_columns(columns)
    assert "opened" in result
    assert result["opened"] == "incident_open_date"
    assert result["priority"] == "priority"
    assert result["ns manager"] == "manager"


if __name__ == "__main__":
    test_mapping_example()
    print("semantic mapping tests passed")
