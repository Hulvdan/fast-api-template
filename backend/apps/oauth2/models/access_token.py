import datetime
from uuid import uuid4

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import ARRAY, UUID

from core.db import Base


class AccessToken(Base):
    id = Column(Integer, primary_key=True)
    created = Column(DateTime, default=datetime.datetime.utcnow)
    modified = Column(DateTime, default=datetime.datetime.utcnow)
    app = Column(Integer, ForeignKey("app.id"))
    scopes = Column(ARRAY(String), default=[])
    access_token = Column(UUID(as_uuid=True), default=uuid4)
