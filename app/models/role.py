from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import String

from app.db.base import Base


class Role(Base):
    __tablename__ = "roles"

    id: Mapped[int] =  mapped_column(primary_key=True, nullable=False)
    code: Mapped[str] = mapped_column(String(50), unique=True)

    users: Mapped[list["UserRole"]] = relationship("UserRole", uselist=True, back_populates="role")