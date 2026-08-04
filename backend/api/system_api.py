from fastapi import APIRouter

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
