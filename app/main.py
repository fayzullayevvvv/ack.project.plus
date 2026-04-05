from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.dependencies import get_db
from app.db.init_db import init_db


app = FastAPI()

init_db()



@app.get("/")
def root(db: Session = Depends(get_db)):
    return {"status": "ok", "db_connected": str(db is not None)}