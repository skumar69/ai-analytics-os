from fastapi import APIRouter, Query
from fastapi.responses import StreamingResponse
import io
import pandas as pd

from services.data_service import get_filtered_dataframe, get_filter_options, has_data
from services.pm_analytics import (
    calculate_mttr,
    calculate_mtbf,
    calculate_pm_compliance,
    calculate_breakdown_percentage,
    calculate_backlog,
    calculate_work_order_age,
    calculate_equipment_health,
    calculate_asset_criticality,
    calculate_top_failed_equipment,
    calculate_failure_frequency,
    get_equipment_detail,
)

router = APIRouter(prefix="/analytics", tags=["Analytics"])


def _df(plant, priority, status, planner_group, date_from, date_to):
    """Return filtered df when any filter is active, else None (uses global normalized df)."""
    if any([plant, priority, status, planner_group, date_from, date_to]):
        return get_filtered_dataframe(plant, priority, status, planner_group, date_from, date_to)
    return None


@router.get("/filter-options")
def filter_options():
    return get_filter_options()


@router.get("/dashboard")
def analytics_dashboard(
    plant:         str | None = Query(None),
    priority:      str | None = Query(None),
    status:        str | None = Query(None),
    planner_group: str | None = Query(None),
    date_from:     str | None = Query(None),
    date_to:       str | None = Query(None),
):
    df = _df(plant, priority, status, planner_group, date_from, date_to)
    return {
        "mttr":                 calculate_mttr(df),
        "mtbf":                 calculate_mtbf(df),
        "pm_compliance":        calculate_pm_compliance(df),
        "breakdown_percentage": calculate_breakdown_percentage(df),
        "backlog":              calculate_backlog(df),
        "work_order_age":       calculate_work_order_age(df),
        "top_failures":         calculate_top_failed_equipment(10, df),
        "health_scores":        calculate_equipment_health(df),
        "asset_criticality":    calculate_asset_criticality(df),
    }


@router.get("/summary")
def analytics_summary(
    plant:         str | None = Query(None),
    priority:      str | None = Query(None),
    status:        str | None = Query(None),
    planner_group: str | None = Query(None),
    date_from:     str | None = Query(None),
    date_to:       str | None = Query(None),
):
    df = _df(plant, priority, status, planner_group, date_from, date_to)
    return {
        "mttr":                 calculate_mttr(df),
        "mtbf":                 calculate_mtbf(df),
        "pm_compliance":        calculate_pm_compliance(df),
        "breakdown_percentage": calculate_breakdown_percentage(df),
        "backlog":              calculate_backlog(df),
        "work_order_age":       calculate_work_order_age(df),
    }


@router.get("/mttr")
def mttr(plant: str | None = Query(None), priority: str | None = Query(None),
         status: str | None = Query(None), planner_group: str | None = Query(None),
         date_from: str | None = Query(None), date_to: str | None = Query(None)):
    return calculate_mttr(_df(plant, priority, status, planner_group, date_from, date_to))


@router.get("/mtbf")
def mtbf(plant: str | None = Query(None), priority: str | None = Query(None),
         status: str | None = Query(None), planner_group: str | None = Query(None),
         date_from: str | None = Query(None), date_to: str | None = Query(None)):
    return calculate_mtbf(_df(plant, priority, status, planner_group, date_from, date_to))


@router.get("/pm-compliance")
def pm_compliance(plant: str | None = Query(None), priority: str | None = Query(None),
                  status: str | None = Query(None), planner_group: str | None = Query(None),
                  date_from: str | None = Query(None), date_to: str | None = Query(None)):
    return calculate_pm_compliance(_df(plant, priority, status, planner_group, date_from, date_to))


@router.get("/breakdown-percentage")
def breakdown_percentage(plant: str | None = Query(None), priority: str | None = Query(None),
                         status: str | None = Query(None), planner_group: str | None = Query(None),
                         date_from: str | None = Query(None), date_to: str | None = Query(None)):
    return calculate_breakdown_percentage(_df(plant, priority, status, planner_group, date_from, date_to))


@router.get("/backlog")
def backlog(plant: str | None = Query(None), priority: str | None = Query(None),
            status: str | None = Query(None), planner_group: str | None = Query(None),
            date_from: str | None = Query(None), date_to: str | None = Query(None)):
    return calculate_backlog(_df(plant, priority, status, planner_group, date_from, date_to))


@router.get("/work-order-age")
def work_order_age(plant: str | None = Query(None), priority: str | None = Query(None),
                   status: str | None = Query(None), planner_group: str | None = Query(None),
                   date_from: str | None = Query(None), date_to: str | None = Query(None)):
    return calculate_work_order_age(_df(plant, priority, status, planner_group, date_from, date_to))


@router.get("/health-score")
def health_score(plant: str | None = Query(None), priority: str | None = Query(None),
                 status: str | None = Query(None), planner_group: str | None = Query(None),
                 date_from: str | None = Query(None), date_to: str | None = Query(None)):
    return calculate_equipment_health(_df(plant, priority, status, planner_group, date_from, date_to))


@router.get("/top-failures")
def top_failures(plant: str | None = Query(None), priority: str | None = Query(None),
                 status: str | None = Query(None), planner_group: str | None = Query(None),
                 date_from: str | None = Query(None), date_to: str | None = Query(None)):
    return calculate_top_failed_equipment(10, _df(plant, priority, status, planner_group, date_from, date_to))


@router.get("/failure-frequency")
def failure_frequency(plant: str | None = Query(None), priority: str | None = Query(None),
                      status: str | None = Query(None), planner_group: str | None = Query(None),
                      date_from: str | None = Query(None), date_to: str | None = Query(None)):
    return calculate_failure_frequency(_df(plant, priority, status, planner_group, date_from, date_to))


@router.get("/asset-criticality")
def asset_criticality(plant: str | None = Query(None), priority: str | None = Query(None),
                      status: str | None = Query(None), planner_group: str | None = Query(None),
                      date_from: str | None = Query(None), date_to: str | None = Query(None)):
    return calculate_asset_criticality(_df(plant, priority, status, planner_group, date_from, date_to))


@router.get("/equipment/{equipment_name}")
def equipment_detail(equipment_name: str):
    return get_equipment_detail(equipment_name)


@router.get("/export")
def export_analytics(
    plant:         str | None = Query(None),
    priority:      str | None = Query(None),
    status:        str | None = Query(None),
    planner_group: str | None = Query(None),
    date_from:     str | None = Query(None),
    date_to:       str | None = Query(None),
):
    if not has_data():
        return {"error": "No data uploaded"}

    df = get_filtered_dataframe(plant, priority, status, planner_group, date_from, date_to)
    if df is None or df.empty:
        return {"error": "No data matches the selected filters"}

    export_df = df[[c for c in df.columns if not c.startswith("_raw_")]]
    buf = io.BytesIO()
    with pd.ExcelWriter(buf, engine="openpyxl") as writer:
        export_df.to_excel(writer, index=False, sheet_name="VisionIQ Export")
    buf.seek(0)
    return StreamingResponse(
        buf,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=visioniq_export.xlsx"},
    )
