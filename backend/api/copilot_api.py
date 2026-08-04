from fastapi import APIRouter
from pydantic import BaseModel
from services.copilot_engine import ask

router = APIRouter(prefix="/copilot", tags=["AI Copilot"])


class Question(BaseModel):
    question: str


@router.post("/ask")
def copilot_ask(body: Question):
    return ask(body.question)


@router.get("/suggest")
def suggested_questions():
    return {
        "suggestions": [
            "Which equipment is at highest risk?",
            "Show asset health scores",
            "Which equipment failed the most?",
            "Show overdue work orders",
            "What is the PM compliance?",
            "Which planner has the most backlog?",
            "What is the MTTR?",
            "What should I do this week?",
            "Show me the MTTR trend",
            "Give me a dashboard summary",
        ]
    }
