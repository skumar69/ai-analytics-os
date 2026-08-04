from fastapi import APIRouter
from services.data_service import get_dataframe

router = APIRouter(
    prefix="",
    tags=["Notifications"],
)


@router.get("/notifications")
def notifications():
    if get_dataframe() is None:
        return [
            {"notification": "100245", "equipment": "Pump-101", "priority": "Critical", "status": "Open"},
            {"notification": "100246", "equipment": "Motor-204", "priority": "High", "status": "In Progress"},
            {"notification": "100247", "equipment": "Boiler-009", "priority": "Medium", "status": "Closed"},
        ]

    df = get_dataframe().copy()

    return [
        {
            "notification": str(row["Notification"] if "Notification" in df.columns else f"INC{i + 1:06d}"),
            "equipment": str(row["Equipment"] if "Equipment" in df.columns else "Unknown"),
            "priority": str(row["Priority"] if "Priority" in df.columns else "Medium"),
            "status": str(row["Status"] if "Status" in df.columns else "Open"),
        }
        for i, (_, row) in enumerate(df.head(20).iterrows())
    ]
