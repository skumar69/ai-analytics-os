from fastapi import APIRouter
from services.risk_engine import get_high_risk_assets

router = APIRouter(tags=["Assets"])


@router.get("/high-risk-assets")
def high_risk_assets():
    return get_high_risk_assets()
