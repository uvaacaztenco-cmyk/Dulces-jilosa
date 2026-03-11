from pydantic import BaseModel
from typing import List

class SaleItemSchema(BaseModel):
    product_id: int
    quantity: int

class SaleCreateSchema(BaseModel):
    items: List[SaleItemSchema]