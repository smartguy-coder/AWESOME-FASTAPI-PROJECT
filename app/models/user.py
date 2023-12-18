import datetime as dt
import uuid

from sqlalchemy import (UUID, Boolean, Column, DateTime, ForeignKey, Integer,
                        String)
from sqlalchemy.orm import mapped_column, relationship, Mapper

from app.database import Base
from app.settings import settings


class BaseInfoMixin:
    id = Column(Integer, primary_key=True, autoincrement=True)
    # id: Mapper[int] = mapped_column(primary_key=True)
    created_at = Column(DateTime, default=dt.datetime.utcnow, nullable=False)
    # from sqlalchemy import func
    # created_at = Column(DateTime, nullable=False, server_default=func.now())

    def to_dict(self):
        return self.__dict__


class User(BaseInfoMixin, Base):
    __tablename__ = "users"

    name = Column(String(settings.DB_MAX_TEXT_LENGTH), nullable=False)
    # name: Mapper[str] = mapped_column(unique=False)
    email = Column(String(settings.DB_MAX_TEXT_LENGTH), unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    last_login = Column(DateTime, nullable=False, default=dt.datetime.utcnow)
    updated_at = Column(DateTime, nullable=True, default=None, onupdate=dt.datetime.utcnow())
    user_uuid = Column(UUID(as_uuid=True), nullable=False, default=uuid.uuid4())
    is_staff = Column(Boolean, default=False)
    is_active = Column(Boolean, default=False)
    verified_at = Column(DateTime, nullable=True, default=None)

    def get_context_string(self, context: str):
        return f"{context}{self.hashed_password[-6:]}{self.updated_at.strftime('%m%d%Y%H%M%S')}".strip()


    tokens = relationship("UserToken", back_populates="user")

    def __repr__(self) -> str:
        return ""


class UserToken(BaseInfoMixin, Base):
    __tablename__ = "user_tokens"

    user_id = mapped_column(ForeignKey("users.id"))
    access_key = Column(String(250), nullable=True, index=True, default=None)
    refresh_key = Column(String(250), nullable=True, index=True, default=None)
    expires_at = Column(DateTime, nullable=False)

    user = relationship("User", back_populates="tokens")
