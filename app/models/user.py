import datetime as dt
import uuid

from sqlalchemy import (UUID, Boolean, Column, DateTime, ForeignKey, Integer,
                        String)
# from sqlalchemy.orm import Mapper, mapped_column, relationship
from sqlalchemy.orm import relationship

from app.database import Base
from app.settings import settings

# from typing import Optional


#
# from typing import Optional
#
# from sqlalchemy import Integer, String, ForeignKey
# from sqlalchemy.orm import Mapped
# from sqlalchemy.orm import mapped_column
#
# from database import Base
#
#
# # https://docs.sqlalchemy.org/en/20/orm/mapping_styles.html
# class User(Base):
#     __tablename__ = "users"
#
#     id: Mapped[int] = mapped_column(primary_key=True)
#     name: Mapped[str]
#     login: Mapped[str] = mapped_column(String(30), unique=True, index=True)
#     password: Mapped[str]
#     nickname: Mapped[Optional[str]]
#     is_active: Mapped[bool] = mapped_column(default=True)
#     age: Mapped[int]
#     money: Mapped[int] = mapped_column(default=0)


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

    user_id = Column(Integer, ForeignKey("users.id"))
    access_key = Column(String(250), nullable=True, index=True, default=None)
    refresh_key = Column(String(250), nullable=True, index=True, default=None)
    expires_at = Column(DateTime, nullable=False)

    user = relationship("User", back_populates="tokens")
