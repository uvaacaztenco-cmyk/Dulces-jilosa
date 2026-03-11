from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.core.database import Base

class InventoryMovement(Base):
    __tablename__ = "inventory_movements"

    id = Column(Integer, primary_key=True)
    product_id = Column(Integer)
    type = Column(String)  # SALE, ENTRY, ADJUSTMENT, LOSS
    quantity = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)