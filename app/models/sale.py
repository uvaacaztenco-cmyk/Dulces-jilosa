from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base   # 👈 ESTA LÍNEA ES LA QUE FALTA
class Sale(Base):
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True)
    total = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    synced = Column(Integer, default=0)

    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User")