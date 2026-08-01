from backend.semantic.dictionary import SEMANTIC_DICTIONARY
from backend.engines.semantic_engine import SemanticEngine


def test_semantic_engine_detects_known_terms():
    columns = ["Opened", "Priority", "Assignment Group", "NS Manager"]
    result = SemanticEngine().detect(columns)

    assert result["opened"] == "incident_open_date"
    assert result["priority"] == "priority"
    assert result["assignment group"] == "assignment_group"
    assert result["ns manager"] == "manager"
    assert "opened" in SEMANTIC_DICTIONARY["incident_open_date"]
