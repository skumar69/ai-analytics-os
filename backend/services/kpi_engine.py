from services.data_service import get_dataframe, has_data


def get_dashboard_kpis():
    if not has_data():
        return {
            "work_orders": 284,
            "notifications": 91,
            "equipment": 56,
            "plants": 8,
            "asset_health": 98,
            "ai_score": 96,
        }

    df = get_dataframe()

    work_orders = len(df)
    equipment = df["Equipment"].nunique() if "Equipment" in df.columns else 0
    plants = df["Plant"].nunique() if "Plant" in df.columns else 0
    notifications = df["Notification"].nunique() if "Notification" in df.columns else work_orders

    return {
        "work_orders": work_orders,
        "notifications": notifications,
        "equipment": equipment,
        "plants": plants,
        "asset_health": 98,
        "ai_score": 96,
    }