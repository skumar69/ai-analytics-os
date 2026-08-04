from fastapi import APIRouter
from services.ai_engine import generate_ai_insights

router = APIRouter(tags=["AI"])


@router.get("/ai-insights")
def ai_insights():
    return generate_ai_insights()
