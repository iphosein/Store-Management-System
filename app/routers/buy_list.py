from sqlalchemy.orm import Session
from .. import models, schemas


def get_list( db: Session , id : int ):
    items = db.query(models.InvoiceItem.product_id, models.InvoiceItem.quantity ).filter(models.InvoiceItem.invoice_id == id).all()
    return items




def create_list(  db: Session , pr : schemas.CreateList ):
    try:
        new_item = models.InvoiceItem(**pr.model_dump())

        product = db.query(models.Product).filter(models.Product.id == new_item.product_id).first()

        if not product:
            return "Product not found"


        if product.stock < pr.quantity :
            return f"Not enough stock of product {new_item.product_id}, We Have {product.stock}"
            # return False

        # stock update
        product.stock -= pr.quantity

        db.add(new_item)
        db.commit()
        db.refresh(new_item)
        # return new_item
        return True

    except Exception as e:
            db.rollback()
            return str(e)