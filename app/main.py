from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.dependencies import get_db
from app.db.init_db import init_db
from app.api.v1.routers.admin import router as admin_router
from app.api.v1.routers.auth import router as auth_router


# init_db()
app = FastAPI()

app.include_router(admin_router)
app.include_router(auth_router)
