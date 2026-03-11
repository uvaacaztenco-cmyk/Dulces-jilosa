from app.models.product import Product
from app.models.inventory_movement import InventoryMovement
from sqlalchemy.orm import Session

def decrease_stock(db: Session, product_id: int, quantity: int):

    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        raise Exception("Producto no encontrado")

    if product.stock < quantity:
        raise Exception("Stock insuficiente")

    product.stock -= quantity

    movement = InventoryMovement(
        product_id=product_id,
        type="SALE",
        quantity=quantity
    )

    db.add(movement)

    return product