from services.data_service import get_dataframe, has_data


def get_high_risk_assets():
    if not has_data():
        return [
            {"equipment": "Pump-101", "plant": "1000", "priority": "Critical", "health": 42, "status": "Running"},
            {"equipment": "Motor-204", "plant": "1100", "priority": "High", "health": 58, "status": "Maintenance"},
            {"equipment": "Boiler-009", "plant": "1200", "priority": "Critical", "health": 39, "status": "Stopped"},
        ]

    df = get_dataframe()

    return [
        {
            "equipment": str(row["Equipment"]) if "Equipment" in df.columns else "Unknown",
            "plant": str(row["Plant"]) if "Plant" in df.columns else "1000",
            "priority": str(row["Priority"]) if "Priority" in df.columns else "High",
            "health": 80,
            "status": str(row["Status"]) if "Status" in df.columns else "Running",
        }
        for _, row in df.head(10).iterrows()
    ]