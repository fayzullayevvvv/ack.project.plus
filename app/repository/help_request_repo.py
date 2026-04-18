from sqlalchemy.orm import Session

from app.models.help_request import HelpRequest


class HelpRequestRepo:
    def __init__(self, db: Session):
        self.db = db

    def create(self, obj: HelpRequest):
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def get_all(self):
        return self.db.query(HelpRequest).all()

    def get_by_id(self, id: int):
        return self.db.query(HelpRequest).filter(HelpRequest.id == id).first()

    def update(self, obj: HelpRequest):
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj