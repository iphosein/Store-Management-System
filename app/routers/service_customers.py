from sqlalchemy.orm import Session
from .. import models



def plus_total_purchases(db : Session ,  id : int , total : float) :

    customer = db.query(models.Customer).filter(models.Customer.id == id).first()
    customer.total_purchases += total
    db.commit()


def minus_total_purchases(db : Session ,  id : int , total : float) :

    customer = db.query(models.Customer).filter(models.Customer.id == id).first()
    customer.total_purchases -= total
    db.commit()


def get_discount_amount(db : Session , id : int ) :

    discount = db.query(models.Customer.level).filter(models.Customer.id == id).scalar()

    return discount * 0.021
