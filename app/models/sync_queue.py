from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from app.core.database import Base

class SyncQueue(Base):
    __tablename__ = "sync_queue"

    id = Column(Integer, primary_key=True)
    entity = Column(String, nullable=False)
    entity_id = Column(Integer, nullable=False)
    operation = Column(String, nullable=False)
    payload = Column(Text, nullable=False)
    synced = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)