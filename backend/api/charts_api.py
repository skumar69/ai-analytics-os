from fastapi import APIRouter
from services.analytics import (
    get_workorder_trend,
    get_priority_chart,
    get_status_chart,
    get_plant_chart,
)

router = APIRouter(tags=["Charts"])


@router.get("/workorder-trend")
def workorder_trend():
    return get_workorder_trend()


@router.get("/priority-chart")
def priority_chart():
    return get_priority_chart()


@router.get("/status-chart")
def status_chart():
    return get_status_chart()


@router.get("/plant-chart")
def plant_chart():
    return get_plant_chart()
