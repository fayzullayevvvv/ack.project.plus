from sqlalchemy import text
from app.db.base import Base
from app.db.session import engine

from app.models import *


def init_db():
    with engine.connect() as conn:
        conn.execute(text("DROP SCHEMA IF EXISTS public CASCADE"))
        conn.execute(text("CREATE SCHEMA public"))
        conn.execute(text("SET search_path TO public"))
        conn.commit()

    Base.metadata.create_all(bind=engine)
