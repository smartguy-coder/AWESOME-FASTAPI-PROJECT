import datetime
import uuid

from sqlalchemy import (
    Column, Integer, Float, String, DateTime, Boolean,
    ForeignKey,UUID
)
from sqlalchemy.orm import Mapper, mapped_column

from app.database import Base


class BaseInfoMixin:
    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)


class User(BaseInfoMixin, Base):
    __tablename__ = 'users'

    name = Column(String, nullable=False)
    login = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    last_login = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)
    user_uuid = Column(UUID(as_uuid=True), nullable=False, default=uuid.uuid4())
    is_staff = Column(Boolean, default=False)

    def __repr__(self) -> str:
        return


# class User(Base):
#     __tablename__ = 'users'
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     name = Column(String(150))
#     email = Column(String(255), unique=True, index=True)
#     password = Column(String(100))
#     is_active = Column(Boolean, default=False)
#     verified_at = Column(DateTime, nullable=True, default=None)
#     updated_at = Column(DateTime, nullable=True, default=None, onupdate=datetime.now)
#     created_at = Column(DateTime, nullable=False, server_default=func.now())
#
#     tokens = relationship("UserToken", back_populates="user")
#
#     def get_context_string(self, context: str):
#         return f"{context}{self.password[-6:]}{self.updated_at.strftime('%m%d%Y%H%M%S')}".strip()
#
#
# class UserToken(Base):
#     __tablename__ = "user_tokens"
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     user_id = mapped_column(ForeignKey('users.id'))
#     access_key = Column(String(250), nullable=True, index=True, default=None)
#     refresh_key = Column(String(250), nullable=True, index=True, default=None)
#     created_at = Column(DateTime, nullable=False, server_default=func.now())
#     expires_at = Column(DateTime, nullable=False)
#
#     user = relationship("User", back_populates="tokens")