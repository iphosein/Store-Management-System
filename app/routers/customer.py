from fastapi import status, HTTPException, Depends, APIRouter , Response
from sqlalchemy.orm import Session
from .. import models, schemas, utils , oauth2
from ..database import get_db
from typing import List , Optional
from sqlalchemy import cast, String
from datetime import date

router = APIRouter(
    prefix="/customers",
    tags=["Customers"]
)



@router.get("/authenticate", response_model=List[schemas.CustomerOut])
async def get_customers( db: Session = Depends(get_db) , current_user: int = Depends(oauth2.get_current_user)):

    customers = db.query(models.Customer).order_by(models.Customer.id).limit(2).all()
    return customers





@router.post("/create" , status_code=status.HTTP_201_CREATED )
async def create_customer(user : schemas.CreateCustomer , db: Session = Depends(get_db)):

    new_customer = models.Customer(**user.model_dump())
    if new_customer.total_purchases > 15000 :
        new_customer.level = 3
    elif 10000 < new_customer.total_purchases < 15000 :
        new_customer.level = 2
    elif 5000 < new_customer.total_purchases < 10000 :
        new_customer.level = 1
    else:
        new_customer.level = 0


    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)
    return new_customer



@router.put("/update/{id}" )
async def update_customer(id : int , new_value : schemas.CustomerUpdate , db: Session = Depends(get_db)):
    customer_query = db.query(models.Customer).filter(models.Customer.id == id)
    user = customer_query.first()
    if not user:
        raise HTTPException(status_code=404, detail=f"Post {id} was not found")

    if new_value.total_purchases > 15000 and new_value.total_purchases is not None :
        new_value.level = 3
    elif 10000 < new_value.total_purchases < 15000 and new_value.total_purchases is not None :
        new_value.level = 2
    elif 5000 < new_value.total_purchases < 10000 and new_value.total_purchases is not None :
        new_value.level = 1
    else:
        new_value.level = 0

    customer_query.update(new_value.model_dump(exclude_unset=True), synchronize_session=False)
    db.commit()
    return {"message" : "OK"}





@router.delete("/delete/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_customer(id : int , db: Session = Depends(get_db)):


    customer = db.query(models.Customer).filter(
        models.Customer.id == id)
    if not customer.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    customer.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/count", status_code=status.HTTP_200_OK)
async def count_customers(db: Session = Depends(get_db)):
    count = db.query(models.Customer).count()
    return {"count" : count}


@router.get("/filter" , response_model=List[schemas.CustomerOut] , status_code=status.HTTP_200_OK )
async def filter_customer( db : Session = Depends(get_db) ,
                    limit: int = 2, skip: int = 0, id : Optional[int] = None , phone_number : Optional[int] = None ,
            first_name : Optional[str] = None , last_name : Optional[str] = None ,
             city: Optional[str] = None ,
            state: Optional[str] = None , country: Optional[str] = None , level : Optional[int] = None , first_purchase_date : Optional[date] = None
                    , birth_day : Optional[date] = None , gender : Optional[str] = None , total_purchases : Optional[int] = None , ):
    query = db.query(models.Customer)

    if id:
        query = query.filter(cast(models.Customer.id, String).ilike(f"%{id}%"))

    if phone_number:
        query = query.filter(models.Customer.phone_number.ilike(f"%{phone_number}%"))

    if first_name:
        query = query.filter(models.Customer.first_name.ilike(f"%{first_name}%"))

    if last_name:
        query = query.filter(models.Customer.last_name.ilike(f"%{last_name}%"))

    if city:
        query = query.filter(models.Customer.city.ilike(f"%{city}%"))

    if state:
        query = query.filter(models.Customer.state.ilike(f"%{state}%"))

    if country:
        query = query.filter(models.Customer.country.ilike(f"%{country}%"))

    if gender:
        query = query.filter(models.Customer.gender.ilike(f"%{gender}%"))

    if birth_day:
        query = query.filter(cast(models.Customer.birth_date, String).ilike(f"%{birth_day}%"))

    if total_purchases :
        query = query.filter(cast(models.Customer.total_purchases, String).ilike(f"%{total_purchases}%"))

    if level :
        query = query.filter(cast(models.Customer.level, String).ilike(f"%{level}%"))

    if first_purchase_date :
        query = query.filter(cast(models.Customer.first_purchase_date, String).ilike(f"%{first_purchase_date}%"))


    customers = query.order_by(models.Customer.id).limit(limit).offset(skip).all()

    return customers



