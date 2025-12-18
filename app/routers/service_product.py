from sqlalchemy.orm import Session
from .. import models




def get_price ( db : Session , id : int):
    product_price = db.query(models.Product.price).filter(models.Product.id == id).scalar()
    return product_price



def get_stock ( db : Session , id : int):
    product_stock = db.query(models.Product.stock).filter(models.Product.id == id).scalar()
    return product_stock


def minus_stock ( db : Session , id : int , stock : int ):
    product_stock = db.query(models.Product.stock).filter(models.Product.id == id).first()
    product_stock.stock -= stock
    if not product_stock.stock > 0 :
        product_stock.is_active = False
    db.commit()



def subtract_stock ( db : Session , id : int , stock : int ):
    product_stock = db.query(models.Product.stock).filter(models.Product.id == id).first()
    product_stock.stock += stock
    db.commit()