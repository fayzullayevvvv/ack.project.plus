from fastapi import APIRouter

from app.api.v1.endpoints.auth import router as auth_router
from app.api.v1.endpoints.users import router as user_router


router = APIRouter(prefix="/v1")

router.include_router(auth_router)
router.include_router(user_router)
