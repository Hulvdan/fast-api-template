import datetime
from uuid import uuid4

from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from core.db import Base


class App(Base):
    id = Column(Integer, primary_key=True)
    name = Column(String(254))
    created = Column(DateTime, default=datetime.datetime.utcnow)
    modified = Column(DateTime, default=datetime.datetime.utcnow)
    client_id = Column(UUID(as_uuid=True), default=uuid4)
    client_secret = Column(UUID(as_uuid=True), default=uuid4)

    access_tokens = relationship("AccessToken")
