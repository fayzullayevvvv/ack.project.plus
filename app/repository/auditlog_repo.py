from sqlalchemy.orm import Session

from app.models.auditlog import AuditLog


class AuditLogRepo:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return (
            self.db.query(AuditLog)
            .order_by(AuditLog.created_at.desc())
            .all()
        )

    def get_by_id(self, log_id: int):
        return (
            self.db.query(AuditLog)
            .filter(AuditLog.id == log_id)
            .first()
        )