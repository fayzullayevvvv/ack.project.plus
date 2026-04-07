from sqlalchemy import create_engine, URL
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

engine = create_engine(
    url=URL.create(
        drivername="postgresql+psycopg2",
        host=settings.PGHOST,
        username=settings.PGUSER,
        password=settings.PGPASSWORD,
        database=settings.PGDATABASE,
    )
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
