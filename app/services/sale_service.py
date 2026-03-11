import json
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.models.sale import Sale
from app.models.sale_item import SaleItem
from app.models.sync_queue import SyncQueue
from app.services.inventory_service import decrease_stock

def create_sale(db: Session, items: list):

    try:
        total = 0

        sale = Sale(total=0)
        db.add(sale)
        db.flush()  # No commit aún

        for item in items:
            product = decrease_stock(db, item["product_id"], item["quantity"])

            subtotal = product.price * item["quantity"]
            total += subtotal

            sale_item = SaleItem(
                sale_id=sale.id,
                product_id=product.id,
                quantity=item["quantity"],
                unit_price=product.price,
                subtotal=subtotal
            )

            db.add(sale_item)

        sale.total = total

        sync_event = SyncQueue(
            entity="sale",
            entity_id=sale.id,
            operation="CREATE",
            payload=json.dumps({
                "sale_id": sale.id,
                "total": sale.total
            })
        )

        db.add(sync_event)

        db.commit()
        return sale

    except SQLAlchemyError as e:
        db.rollback()
        raise Exception("Error al crear la venta: " + str(e))