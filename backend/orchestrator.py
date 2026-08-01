from __future__ import annotations

from backend.engines.dashboard_engine import DashboardEngine
from backend.engines.enrichment_engine import EnrichmentEngine
from backend.engines.execution_plan import ExecutionPlan
from backend.engines.file_reader import FileReader
from backend.engines.insight_engine import InsightEngine
from backend.engines.kpi_engine import KPIEngine
from backend.engines.report_engine import ReportEngine
from backend.engines.schema_engine import SchemaEngine
from backend.engines.semantic_engine import SemanticEngine


class Orchestrator:
    """Coordinates the end-to-end analytics workflow."""

    def __init__(self):
        self.file_reader = FileReader()
        self.schema_engine = SchemaEngine()
        self.semantic_engine = SemanticEngine()
        self.execution_plan = ExecutionPlan()
        self.enrichment_engine = EnrichmentEngine()
        self.kpi_engine = KPIEngine()
        self.dashboard_engine = DashboardEngine()
        self.insight_engine = InsightEngine()
        self.report_engine = ReportEngine()

    def process(self, file_path):
        df = self.file_reader.read(file_path)
        schema = self.schema_engine.detect(df)
        semantic_map = self.semantic_engine.detect(df.columns)
        execution_plan = self.execution_plan.describe(semantic_map, ["incident_pack"])
        enriched = self.enrichment_engine.enrich(df, semantic_map)
        kpis = self.kpi_engine.calculate(enriched)
        dashboard = self.dashboard_engine.build(enriched, kpis)
        insights = self.insight_engine.generate(enriched, kpis)

        return {
            "schema": schema,
            "semantic_map": semantic_map,
            "execution_plan": execution_plan,
            "enriched_dataset": enriched,
            "kpis": kpis,
            "dashboard": dashboard,
            "insights": insights,
            "record_count": len(df),
        }


if __name__ == "__main__":
    orchestrator = Orchestrator()
    report = orchestrator.process("sample_data/sap_incident_data_100_rows.xlsx")
    print(report["record_count"])
    print(report["semantic_map"])
