from collections import Counter
from services.data_service import get_dataframe, has_data


def get_workorder_trend():
    if not has_data():
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
            {"month": "Oct", "orders": 72},
            {"month": "Nov", "orders": 69},
            {"month": "Dec", "orders": 76},
        ]
    df = get_dataframe()
    if "Month" not in df.columns:
        return []
    counts = df["Month"].astype(str).value_counts()
    return [{"month": month, "orders": int(count)} for month, count in counts.items()]


def get_priority_chart():
    if not has_data():
        return [
            {"priority": "Critical", "count": 18},
            {"priority": "High", "count": 45},
            {"priority": "Medium", "count": 82},
            {"priority": "Low", "count": 26},
        ]
    df = get_dataframe()
    if "Priority" not in df.columns:
        return []
    counts = Counter(df["Priority"].astype(str))
    return [{"priority": k, "count": v} for k, v in counts.items()]


def get_status_chart():
    if not has_data():
        return [
            {"status": "Open", "count": 64},
            {"status": "In Progress", "count": 42},
            {"status": "Completed", "count": 131},
            {"status": "On Hold", "count": 18},
            {"status": "Rejected", "count": 6},
        ]
    df = get_dataframe()
    if "Status" not in df.columns:
        return []
    counts = Counter(df["Status"].astype(str))
    return [{"status": k, "count": v} for k, v in counts.items()]


def get_plant_chart():
    if not has_data():
        return [
            {"plant": "1000", "count": 35},
            {"plant": "1100", "count": 52},
            {"plant": "1200", "count": 24},
            {"plant": "1300", "count": 41},
            {"plant": "1400", "count": 27},
        ]
    df = get_dataframe()
    if "Plant" not in df.columns:
        return []
    counts = Counter(df["Plant"].astype(str))
    return [{"plant": k, "count": v} for k, v in counts.items()]