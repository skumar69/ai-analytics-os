from __future__ import annotations

MANIFEST = {
    "name": "incident_pack",
    "description": "Incident analytics and operational monitoring pack",
    "features": [
        "schema_detection",
        "semantic_mapping",
        "incident_kpis",
        "risk_dashboard",
        "insight_generation",
    ],
}


def get_manifest():
    return MANIFEST.copy()
