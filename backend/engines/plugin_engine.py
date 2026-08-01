from __future__ import annotations

from abc import ABC, abstractmethod


class BasePlugin(ABC):
    """Base class for all semantic engine plugins."""

    name: str = "base_plugin"

    @abstractmethod
    def process(self, data):
        raise NotImplementedError


class SemanticEngine:
    """Container for executing semantic plugins."""

    def __init__(self):
        self.plugins = []

    def register(self, plugin: BasePlugin):
        self.plugins.append(plugin)

    def run(self, data):
        results = []
        for plugin in self.plugins:
            results.append(plugin.process(data))
        return results


class DatePlugin(BasePlugin):
    name = "Date Plugin"

    def process(self, data):
        return {"plugin": self.name, "status": "ready", "type": "date"}


class PriorityPlugin(BasePlugin):
    name = "Priority Plugin"

    def process(self, data):
        return {"plugin": self.name, "status": "ready", "type": "priority"}


class EmployeePlugin(BasePlugin):
    name = "Employee Plugin"

    def process(self, data):
        return {"plugin": self.name, "status": "ready", "type": "employee"}


class IncidentPlugin(BasePlugin):
    name = "Incident Plugin"

    def process(self, data):
        return {"plugin": self.name, "status": "ready", "type": "incident"}


class FinancePlugin(BasePlugin):
    name = "Finance Plugin"

    def process(self, data):
        return {"plugin": self.name, "status": "ready", "type": "finance"}


class SAPPMPlugin(BasePlugin):
    name = "SAP PM Plugin"

    def process(self, data):
        return {"plugin": self.name, "status": "ready", "type": "sap_pm"}


class AttendancePlugin(BasePlugin):
    name = "Attendance Plugin"

    def process(self, data):
        return {"plugin": self.name, "status": "ready", "type": "attendance"}


if __name__ == "__main__":
    engine = SemanticEngine()
    for plugin in [
        DatePlugin(),
        PriorityPlugin(),
        EmployeePlugin(),
        IncidentPlugin(),
        FinancePlugin(),
        SAPPMPlugin(),
        AttendancePlugin(),
    ]:
        engine.register(plugin)

    print(engine.run({"source": "demo"}))
