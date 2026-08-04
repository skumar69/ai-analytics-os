from services.data_service import get_dataframe, has_data


def generate_ai_insights():
    if not has_data():
        return {
            "critical": 18,
            "overdue": 14,
            "high_risk": 9,
            "health": 98,
            "recommendations": [
                "Schedule PM for overdue equipment.",
                "Critical assets require immediate inspection.",
                "Reduce preventive maintenance backlog.",
                "Review recurring breakdown notifications.",
                "Inspect pumps in Plant 1000.",
            ],
        }

    df = get_dataframe()

    recommendations = [
        f"Inspect {equipment} during the next PM cycle."
        for equipment in df["Equipment"].dropna().unique()[:5]
    ] if "Equipment" in df.columns else ["No AI recommendations available."]

    return {
        "critical": 18,
        "overdue": 14,
        "high_risk": 9,
        "health": 98,
        "recommendations": recommendations,
    }