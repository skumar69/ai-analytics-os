from fastapi import APIRouter
from services.data_service import has_data, get_column_map

router = APIRouter(
    prefix="",
    tags=["System"],
)


@router.get("/")
def root():
    return {
        "message": "VisionIQ AI Analytics API is running",
        "status": "Healthy",
    }


@router.get("/health")
def health():
    return {
        "status": "Healthy",
        "backend": "FastAPI",
        "version": "3.0.0",
    }


@router.get("/api/info")
def api_info():
    return {
        "application": "VisionIQ AI Analytics OS",
        "backend": "FastAPI",
        "frontend": "React + Material UI",
        "database": "SAP Excel / CSV",
        "version": "3.0.0",
        "status": "Running",
    }


@router.get("/data/schema")
def data_schema():
    """Show which SAP columns were detected and mapped after upload."""
    if not has_data():
        return {"uploaded": False, "message": "No data uploaded yet."}
    return {"uploaded": True, "column_map": get_column_map()}
