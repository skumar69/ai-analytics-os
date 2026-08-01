from __future__ import annotations


class CapabilityPackResolver:
    """Resolve the relevant capability packs for a dataset."""

    def __init__(self):
        self.pack_rules = {
            "incident_pack": ["incident", "opened", "resolved", "priority", "assignment group", "manager"],
            "finance_pack": ["cost", "revenue", "amount", "finance", "invoice"],
            "sap_pm_pack": ["equipment", "maintenance", "pm", "work order", "asset"],
            "attendance_pack": ["attendance", "employee", "hours", "shift", "absence"],
        }

    def resolve(self, semantic_map):
        matched = []
        normalized = {str(key).lower(): value for key, value in semantic_map.items()}

        for pack_name, keywords in self.pack_rules.items():
            keyword_set = {str(keyword).lower() for keyword in keywords}
            if any(keyword in normalized for keyword in keyword_set):
                matched.append(pack_name)

        return matched or ["incident_pack"]
