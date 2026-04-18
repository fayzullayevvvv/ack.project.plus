from sqlalchemy.orm import Session
    
from app.models.notification import Notification


class NotificationRepo:
    def __init__(self, db: Session):
        self.db = db

    def get_user_notifications(self, user_id: int):
        return (
            self.db.query(Notification)
            .filter(Notification.user_id == user_id)
            .order_by(Notification.created_at.desc())
            .all()
        )

    def get_notification_by_id(self, notification_id: int):
        return (
            self.db.query(Notification)
            .filter(Notification.id == notification_id)
            .first()
        )

    def create_notification(self, notification: Notification):
        self.db.add(notification)
        self.db.commit()
        self.db.refresh(notification)
        return notification

    def mark_as_read(self, notification: Notification):
        notification.is_read = True
        self.db.add(notification)
        self.db.commit()
        self.db.refresh(notification)
        return notification

    def mark_all_as_read(self, user_id: int):
        self.db.query(Notification).filter(
            Notification.user_id == user_id,
            Notification.is_read == False
        ).update({"is_read": True})

        self.db.commit()

    def get_unread_count(self, user_id: int):
        return (
            self.db.query(Notification)
            .filter(
                Notification.user_id == user_id,
                Notification.is_read == False
            )
            .count()
        )