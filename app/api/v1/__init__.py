from fastapi import APIRouter

from app.api.v1.endpoints.auth import router as auth_router
from app.api.v1.endpoints.users import router as user_router
from app.api.v1.endpoints.project import router as project_router
from app.api.v1.endpoints.profile import router as profile_router
from app.api.v1.endpoints.task import router as task_router

router = APIRouter(prefix="/v1")

router.include_router(auth_router)
router.include_router(user_router)
router.include_router(project_router)
router.include_router(profile_router)
router.include_router(task_router)
