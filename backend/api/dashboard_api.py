from fastapi import APIRouter
from services.kpi_engine import get_dashboard_kpis

router = APIRouter(tags=["Dashboard"])


@router.get("/stats")
def dashboard_stats():
    return get_dashboard_kpis()
