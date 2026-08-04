from fastapi import APIRouter

router = APIRouter(tags=["Dashboard"])


@router.get("/stats")
def get_stats():
    return {
        "work_orders": 284,
        "notifications": 91,
        "asset_health": 98,
        "equipment": 56,
        "plants": 8,
    }