from __future__ import annotations


class ExecutionPlan:
    """Build an ordered execution plan from semantic matches and capability packs."""

    def __init__(self):
        self.steps = []

    def build(self, semantic_map, capability_packs=None):
        self.steps = [
            "excel_upload",
            "schema_engine",
            "semantic_engine",
            "execution_plan",
            "enrichment_engine",
            "enriched_dataset",
        ]

        if capability_packs:
            self.steps.insert(4, "capability_pack_resolver")
            for pack in capability_packs:
                self.steps.append(f"{pack}")

        if semantic_map:
            self.steps.append("semantic_mapping_applied")

        return list(self.steps)

    def describe(self, semantic_map, capability_packs=None):
        plan = self.build(semantic_map, capability_packs)
        return {
            "plan": plan,
            "semantic_map": semantic_map,
            "capability_packs": capability_packs or [],
        }


if __name__ == "__main__":
    plan = ExecutionPlan()
    print(plan.describe({"opened": "incident_open_date", "priority": "priority"}, ["incident_pack"]))
