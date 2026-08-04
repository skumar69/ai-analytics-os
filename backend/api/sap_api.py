from fastapi import APIRouter, Query
from services.data_service import get_filtered_dataframe
from services.sap_intelligence import (
    calculate_asset_health_scores,
    pm_compliance_by_plant,
    planner_group_performance,
    work_order_sla,
    repeat_failure_analysis,
    mttr_trend,
    equipment_reliability_index,
)

router = APIRouter(prefix="/sap", tags=["SAP Intelligence"])


def _df(plant, priority, status, planner_group, date_from, date_to):
    if any([plant, priority, status, planner_group, date_from, date_to]):
        return get_filtered_dataframe(plant, priority, status, planner_group, date_from, date_to)
    return None


@router.get("/asset-health")
def asset_health(
    plant:         str | None = Query(None),
    priority:      str | None = Query(None),
    status:        str | None = Query(None),
    planner_group: str | None = Query(None),
    date_from:     str | None = Query(None),
    date_to:       str | None = Query(None),
):
    return calculate_asset_health_scores(_df(plant, priority, status, planner_group, date_from, date_to))


@router.get("/pm-compliance-by-plant")
def pm_by_plant(
    priority:      str | None = Query(None),
    status:        str | None = Query(None),
    planner_group: str | None = Query(None),
    date_from:     str | None = Query(None),
    date_to:       str | None = Query(None),
):
    return pm_compliance_by_plant(_df(None, priority, status, planner_group, date_from, date_to))


@router.get("/planner-performance")
def planner_performance(
    plant:     str | None = Query(None),
    priority:  str | None = Query(None),
    date_from: str | None = Query(None),
    date_to:   str | None = Query(None),
):
    return planner_group_performance(_df(plant, priority, None, None, date_from, date_to))


@router.get("/work-order-sla")
def wo_sla(
    sla_days:      int       = Query(30, description="SLA threshold in days"),
    plant:         str | None = Query(None),
    priority:      str | None = Query(None),
    planner_group: str | None = Query(None),
    date_from:     str | None = Query(None),
    date_to:       str | None = Query(None),
):
    return work_order_sla(sla_days, _df(plant, priority, None, planner_group, date_from, date_to))


@router.get("/repeat-failures")
def repeat_failures(
    min_failures:  int       = Query(3, description="Minimum failure count to flag"),
    plant:         str | None = Query(None),
    priority:      str | None = Query(None),
    date_from:     str | None = Query(None),
    date_to:       str | None = Query(None),
):
    return repeat_failure_analysis(min_failures, _df(plant, priority, None, None, date_from, date_to))


@router.get("/mttr-trend")
def mttr_trend_endpoint(
    plant:     str | None = Query(None),
    priority:  str | None = Query(None),
    date_from: str | None = Query(None),
    date_to:   str | None = Query(None),
):
    return mttr_trend(_df(plant, priority, None, None, date_from, date_to))


@router.get("/reliability-index")
def reliability_index(
    plant:     str | None = Query(None),
    priority:  str | None = Query(None),
    date_from: str | None = Query(None),
    date_to:   str | None = Query(None),
):
    return equipment_reliability_index(_df(plant, priority, None, None, date_from, date_to))


@router.get("/intelligence-summary")
def intelligence_summary(
    plant:         str | None = Query(None),
    priority:      str | None = Query(None),
    planner_group: str | None = Query(None),
    date_from:     str | None = Query(None),
    date_to:       str | None = Query(None),
):
    """Single aggregated payload for the Executive Dashboard."""
    df = _df(plant, priority, None, planner_group, date_from, date_to)
    health = calculate_asset_health_scores(df)
    return {
        "asset_health":        health,
        "red_count":           sum(1 for h in health if h["risk_level"] == "Red"),
        "amber_count":         sum(1 for h in health if h["risk_level"] == "Amber"),
        "green_count":         sum(1 for h in health if h["risk_level"] == "Green"),
        "fleet_health_avg":    round(sum(h["health_score"] for h in health) / len(health), 1) if health else None,
        "pm_by_plant":         pm_compliance_by_plant(df),
        "planner_performance": planner_group_performance(df),
        "work_order_sla":      work_order_sla(30, df),
        "repeat_failures":     repeat_failure_analysis(3, df),
        "mttr_trend":          mttr_trend(df),
        "reliability_index":   equipment_reliability_index(df),
    }
