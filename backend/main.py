from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from utils.logger import get_logger

log = get_logger("visioniq")

# Upload API
from upload_api import router as upload_router
from api.charts_api import router as charts_router
from api.dashboard_api import router as dashboard_router
from api.assets_api import router as assets_router
from api.notifications_api import router as notifications_router
from api.ai_api import router as ai_router
from api.system_api import router as system_router
from api.analytics_api import router as analytics_router
from api.auth_api import router as auth_router
from api.sap_api import router as sap_router
from api.copilot_api import router as copilot_router

app = FastAPI(
    title="VisionIQ AI Analytics OS",
    version="3.0.0",
    description="Enterprise AI Analytics Platform for SAP PM / EAM",
)

# ==========================================================
# CORS
# ==========================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================================================
# Register Routers
# ==========================================================

app.include_router(upload_router)
app.include_router(charts_router)
app.include_router(dashboard_router)
app.include_router(assets_router)
app.include_router(notifications_router)
app.include_router(ai_router)
app.include_router(system_router)
app.include_router(analytics_router)
app.include_router(auth_router)
app.include_router(sap_router)
app.include_router(copilot_router)
