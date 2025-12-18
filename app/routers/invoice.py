from fastapi import status, HTTPException, Depends, APIRouter , Response
from sqlalchemy.orm import Session
from .. import models, schemas , oauth2
from ..database import get_db
from typing import List , Optional
from sqlalchemy import cast, String
from datetime import date

from . import buy_list , service_product  , service_invoice_item , service_customers
router = APIRouter(
    prefix="/invoices",
    tags=["Invoices"]
)



@router.get("/authenticate", response_model=List[schemas.InvoiceOut])
async def create_user( db: Session = Depends(get_db) , current_user: int = Depends(oauth2.get_current_user)):

    invoices = db.query(models.Invoice).order_by(models.Invoice.id).limit(2).all()

    return invoices





@router.post("/create" , status_code=status.HTTP_201_CREATED , response_model=schemas.InvoiceOut)
async def create_invoice(pr : schemas.CreateInvoice , db: Session = Depends(get_db)
                      , current_user: int = Depends(oauth2.get_current_user)):
    try :
        buy_ls = pr.b_list.split("-")

        new_invoice = models.Invoice(**pr.model_dump(exclude_unset=True))

        new_invoice.admin_id = current_user.id

        db.add(new_invoice)
        db.flush()

        in_id = new_invoice.id

        total = 0

        for item in buy_ls:
            pq = item.split("*")
            invoiceitem = schemas.CreateList(invoice_id = int(in_id), product_id = int(pq[0].strip()), quantity = int(pq[1].strip()))
            a = buy_list.create_list(db, invoiceitem)
            if a is True:
                price = service_product.get_price(db, int(pq[0].strip()) )
                total += int(price) * int(pq[1].strip())
            else :
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=a)

        discount = service_customers.get_discount_amount(db, pr.customer_id)
        total_p = total - total * discount
        discount_amount = total * discount

        service_customers.plus_total_purchases(db, pr.customer_id , total_p)

        new_invoice.total_paid = total_p
        new_invoice.discount_amount = discount_amount
        db.add(new_invoice)
        db.commit()
        db.refresh(new_invoice)

        return new_invoice

    except Exception as e:
            db.rollback()
            raise


@router.put("/update/{id}" )
async def update_invoice(id : int , new_value : schemas.InvoiceUpdate , db: Session = Depends(get_db)):
    invoices_query = db.query(models.Invoice).filter(models.Invoice.id == id)

    old_total_paid = invoices_query.first().total_paid
    customer_id = invoices_query.first().customer_id

    # ADD stock of products
    service_invoice_item.roll_back(db, id)

    #minus old total from customer history
    service_customers.minus_total_purchases(db, customer_id, old_total_paid)

    buy_ls = new_value.b_list.split("-")

    total = 0

    for item in buy_ls:
        pq = item.split("*")
        invoiceitem = {"invoice_id": int(id), "product_id": int(pq[0].strip()), "quantity": int(pq[1].strip())}
        a = buy_list.create_list(db, invoiceitem)
        if a is True:
            price = service_product.get_price(db, int(pq[0].strip()) )
            total += int(price) * int(pq[1].strip())
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=a)

    discount = service_customers.get_discount_amount(db, new_value.customer_id)
    total_p = total - total * discount

    service_customers.plus_total_purchases(db, new_value.customer_id, total_p)

    new_value.total_paid = total_p

    invoices_query.update(
        new_value.model_dump(exclude_unset=True),
        synchronize_session=False
    )
    db.commit()
    return {"message" : "OK"}





@router.delete("/delete/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_invoice(id : int , db: Session = Depends(get_db)):


    invoices_query = db.query(models.Invoice).filter(
        models.Invoice.id == id)
    invoice = invoices_query.first()




    if not invoice:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    #ADD stock of products
    service_invoice_item.roll_back(db, id )

    service_customers.minus_total_purchases(db, id, invoice.total_paid)


    invoices_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)




@router.get("/count", status_code=status.HTTP_200_OK)
async def count_users(db: Session = Depends(get_db)):
    count = db.query(models.Invoice).count()
    return {"count" : count}


@router.get("/filter" , response_model=List[schemas.InvoiceOut] , status_code=status.HTTP_200_OK )
async def get_user( db : Session = Depends(get_db) ,
                    limit: int = 2, skip: int = 0, id : Optional[int] = None ,admin_id : Optional[int] = None ,
                    customer_id : Optional[int] = None ,purchase_date : Optional[date] = None ,total_paid : Optional[float] = None ,
                    b_list : Optional[str] = None ,discount_amount : Optional[float] = None ):
    query = db.query(models.Invoice)

    if id:
        query = query.filter(cast(models.Invoice.id, String).ilike(f"%{id}%"))
    if admin_id:
        query = query.filter(cast(models.Invoice.admin_id, String).ilike(f"%{admin_id}%"))
    if customer_id:
        query = query.filter(cast(models.Invoice.customer_id, String).ilike(f"%{customer_id}%"))
    if purchase_date:
        query = query.filter(cast(models.Invoice.purchase_date, String).ilike(f"%{purchase_date}%"))
    if total_paid:
        query = query.filter(cast(models.Invoice.total_paid, String).ilike(f"%{total_paid}%"))
    if discount_amount:
        query = query.filter(cast(models.Invoice.discount_amount, String).ilike(f"%{discount_amount}%"))
    if b_list:
        query = query.filter(models.Invoice.b_list).ilike(f"%{b_list}%")

    invoices = query.order_by(models.Invoice.id).limit(limit).offset(skip).all()

    return invoices