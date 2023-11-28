import datetime
import uuid

from sqlalchemy import (
    Column, Integer, String, DateTime, Boolean,
    UUID
)

from database import Base


class BaseInfoMixin:
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)


class User(BaseInfoMixin, Base):
    __tablename__ = 'user'

    name = Column(String, nullable=False)
    login = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    last_login = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)
    user_uuid = Column(UUID(as_uuid=True), nullable=False, default=uuid.uuid4())
    is_staff = Column(Boolean, default=False)

    def __repr__(self) -> str:
        ddict = {'id': self.id,
                 'name': self.name,
                 'login': self.login,
                 'password': self.password,
                 'user_uuid': self.user_uuid,
                 'last_login': self.last_login,
                 'is_staff': self.is_staff,
                 'created_at': self.created_at}
        return str(ddict)
