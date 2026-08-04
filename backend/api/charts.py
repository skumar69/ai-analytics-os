from fastapi import APIRouter

router = APIRouter(tags=["Charts"])


@router.get("/workorder-trend")
def workorder_trend():
    return [
        {"month": "Jan", "orders": 22},
        {"month": "Feb", "orders": 31},
        {"month": "Mar", "orders": 27},
        {"month": "Apr", "orders": 45},
        {"month": "May", "orders": 41},
        {"month": "Jun", "orders": 52},
        {"month": "Jul", "orders": 60},
        {"month": "Aug", "orders": 58},
        {"month": "Sep", "orders": 65},
        {"month": "Oct", "orders": 71},
        {"month": "Nov", "orders": 68},
        {"month": "Dec", "orders": 75},
    ]


@router.get("/priority-chart")
def priority_chart():
    return [
        {"name": "Critical", "value": 18},
        {"name": "High", "value": 45},
        {"name": "Medium", "value": 82},
        {"name": "Low", "value": 26},
    ]


@router.get("/plant-chart")
def plant_chart():
    return [
        {"plant": "1000", "count": 35},
        {"plant": "1100", "count": 52},
        {"plant": "1200", "count": 24},
        {"plant": "1300", "count": 41},
    ]


@router.get("/status-chart")
def status_chart():
    return [
        {"status": "Open", "count": 54},
        {"status": "Closed", "count": 312},
        {"status": "Pending", "count": 24},
        {"status": "Resolved", "count": 110},
    ]