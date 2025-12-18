from fastapi import status, HTTPException, Depends, APIRouter , Response
from sqlalchemy.orm import Session
from .. import models, schemas, utils , oauth2
from ..database import get_db
from typing import List , Optional
from sqlalchemy import cast, String


router = APIRouter(
    prefix="/admins",
    tags=["Admins"]
)



@router.get("/authenticate", response_model=List[schemas.AdminOut])
async def create_user( db: Session = Depends(get_db) , current_user: int = Depends(oauth2.get_current_user)):
    user = db.query(models.Admin).filter(models.Admin.id == current_user.id).first()

    if user.role != "manager":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    admins = db.query(models.Admin).order_by(models.Admin.id).limit(2).all()

    return admins





@router.post("/create" , status_code=status.HTTP_201_CREATED )
async def create_user(user : schemas.AdminCreate , db: Session = Depends(get_db)):

    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_user = models.Admin(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user



@router.put("/update/{id}" )
async def create_user(id : int , new_value : schemas.UpdateAdmin , db: Session = Depends(get_db)):
    user_query = db.query(models.Admin).filter(models.Admin.id == id)
    user = user_query.first()
    if not user:
        raise HTTPException(status_code=404, detail=f"Post {id} was not found")
    user_query.update(new_value.model_dump(exclude_unset=True), synchronize_session=False)
    db.commit()
    return {"message" : "OK"}





@router.delete("/delete/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(id : int , db: Session = Depends(get_db)):


    user = db.query(models.Admin).filter(
        models.Admin.id == id)
    if not user.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    user.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/count", status_code=status.HTTP_200_OK)
async def count_users(db: Session = Depends(get_db)):
    count = db.query(models.Admin).count()
    return {"count" : count}


@router.get("/filter" , response_model=List[schemas.AdminOut] , status_code=status.HTTP_200_OK )
async def get_user( db : Session = Depends(get_db) ,
                    limit: int = 2, skip: int = 0, id : Optional[int] = None , phone_number : Optional[int] = None ,
            first_name : Optional[str] = None , last_name : Optional[str] = None , email : Optional[str] = None ,
            password: Optional[str] = None , national_id: Optional[int] = None , city: Optional[str] = None ,
            state: Optional[str] = None , country: Optional[str] = None , education: Optional[str] = None , hire_date: Optional[str] = None ,
            role: Optional[str] = None , gender: Optional[str] = None , birth_date: Optional[str] = None , age: Optional[str] = None ,
                    salary: Optional[int] = None ,):
    query = db.query(models.Admin)

    if id:
        query = query.filter(cast(models.Admin.id, String).ilike(f"%{id}%"))

    if phone_number:
        query = query.filter(models.Admin.phone_number.ilike(f"%{phone_number}%"))

    if first_name:
        query = query.filter(models.Admin.first_name.ilike(f"%{first_name}%"))

    if last_name:
        query = query.filter(models.Admin.last_name.ilike(f"%{last_name}%"))

    if email:
        query = query.filter(models.Admin.email.ilike(f"%{email}%"))

    if national_id:
        query = query.filter(models.Admin.national_id.ilike(f"%{national_id}%"))

    if city:
        query = query.filter(models.Admin.city.ilike(f"%{city}%"))

    if state:
        query = query.filter(models.Admin.state.ilike(f"%{state}%"))

    if country:
        query = query.filter(models.Admin.country.ilike(f"%{country}%"))

    if education:
        query = query.filter(models.Admin.education.ilike(f"%{education}%"))

    if role:
        query = query.filter(models.Admin.role.ilike(f"%{role}%"))

    if gender:
        query = query.filter(models.Admin.gender.ilike(f"%{gender}%"))

    if birth_date :
        query = query.filter(cast(models.Admin.birth_date, String).ilike(f"%{birth_date}%"))

    if age:
        query = query.filter(cast(models.Admin.age, String).ilike(f"%{age}%"))

    if salary:
        query = query.filter(cast(models.Admin.salary, String).ilike(f"%{salary}%"))

    if hire_date:
        query = query.filter(cast(models.Admin.hire_date, String).ilike(f"%{hire_date}%"))


    admins = query.order_by(models.Admin.id).limit(limit).offset(skip).all()

    return admins