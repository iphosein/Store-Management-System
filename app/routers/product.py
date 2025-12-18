from fastapi import status, HTTPException, Depends, APIRouter , Response
from sqlalchemy.orm import Session
from .. import models, schemas, utils , oauth2
from ..database import get_db
from typing import List , Optional
from sqlalchemy import cast, String

router = APIRouter(
    prefix="/products",
    tags=["Products"]
)



@router.get("/authenticate", response_model=List[schemas.ProductOut])
async def create_user( db: Session = Depends(get_db) , current_user: int = Depends(oauth2.get_current_user)):

    Products = db.query(models.Product).order_by(models.Product.id).limit(2).all()

    return Products





@router.post("/create" , status_code=status.HTTP_201_CREATED )
async def create_user(pr : schemas.CreateProduct , db: Session = Depends(get_db)):

    new_product = models.Product(**pr.model_dump())

    if new_product.stock > 0 :
        new_product.is_active = True
    else :
        new_product.is_active = False

    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product



@router.put("/update/{id}")
async def update_product(id : int , new_value : schemas.ProductUpdate , db: Session = Depends(get_db)):
    product_query = db.query(models.Product).filter(models.Product.id == id)

    product = product_query.first()
    if not product:
        raise HTTPException(status_code=404, detail=f"Post {id} was not found")

    if new_value.stock > 0 :
        product.is_active = True
    else :
        product.is_active = False

    product_query.update(new_value.model_dump(exclude_unset=True), synchronize_session=False)
    db.commit()
    return {"message" : "OK"}





@router.delete("/delete/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(id : int , db: Session = Depends(get_db)):


    product = db.query(models.Product).filter(
        models.Product.id == id)
    if not product.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    product.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/count", status_code=status.HTTP_200_OK)
async def count_users(db: Session = Depends(get_db)):
    count = db.query(models.Product).count()
    return {"count" : count}


@router.get("/filter" , response_model=List[schemas.ProductOut] , status_code=status.HTTP_200_OK )
async def filter_product( db : Session = Depends(get_db) ,
                    limit: int = 2, skip: int = 0, id : Optional[int] = None , name : Optional[str] = None,
                    stock : Optional[int] = None , price : Optional[float] = None , description : Optional[str] = None,
                    is_active: Optional[bool] = True ):
    query = db.query(models.Product)

    if id:
        query = query.filter(cast(models.Product.id, String).ilike(f"%{id}%"))

    if name:
        query = query.filter(models.Product.name.ilike(f"%{name}%"))

    if stock:
        query = query.filter(cast(models.Product.stock , String).ilike(f"%{stock}%"))

    if price:
        query = query.filter(cast(models.Product.price, String).ilike(f"%{price}%"))

    if description:
        query = query.filter(models.Product.description.ilike(f"%{description}%"))

    if is_active is not None:
        query = query.filter(cast(models.Product.is_active, String).ilike(f"%{is_active}%"))


    products = query.order_by(models.Product.id).limit(limit).offset(skip).all()

    return products



