from sqlalchemy.orm import Session
from .. import models
from . import service_product


def roll_back ( db : Session , id : int):
    items = db.query(models.InvoiceItem.product_id , models.InvoiceItem.quantity).filter(models.InvoiceItem.invoice_id == id).all()

    for pid , qu in items:
        service_product.subtract_stock(db , pid , qu)

    db.query(models.InvoiceItem) \
        .filter(models.InvoiceItem.invoice_id == id) \
        .delete()

    db.commit()
    return True






