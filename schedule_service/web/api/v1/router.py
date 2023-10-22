from fastapi.routing import APIRouter

from schedule_service.web.api.v1 import schedule, workbook

api_v1_router = APIRouter(prefix="/api/v1")
api_v1_router.include_router(schedule.router, prefix="/schedule", tags=["schedule"])
api_v1_router.include_router(workbook.router, prefix="/workbook", tags=["workbook"])
