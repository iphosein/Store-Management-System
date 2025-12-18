from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..database import get_db

from .. import database, schemas, models, utils , oauth2

router = APIRouter(prefix="/login",tags=['Authentication'])

@router.post('' , response_model=schemas.Token , status_code=status.HTTP_200_OK)
async def login(user_credentials: schemas.UserLogin , db: Session = Depends(database.get_db)):

    user = db.query(models.Admin).filter(
        models.Admin.email == user_credentials.email).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    if not utils.verify(user_credentials.password, user.password):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    # create a token
    # return token

    access_token = oauth2.create_access_token(data={"user_id": user.id})

    return {"access_token": access_token, "token_type": "bearer","name": user.first_name}



@router.post("/forget" )
async def create_user( payload: schemas.Forget , db: Session = Depends(get_db) ):

    email = payload.email.strip().lower()

    user = db.query(models.Admin).filter(models.Admin.email == email).first()


    if not user:
        raise HTTPException(status_code=404, detail="Email not found")

    return {"message": "OK"}



@router.put("/reset")
async def create_user(info: schemas.ResetPassword, db: Session = Depends(get_db)):
    user_query = db.query(models.Admin).filter(models.Admin.email == info.email)

    hashed_password = utils.hash(info.password)
    info.password = hashed_password

    user_query.update(info.model_dump(exclude_unset=True), synchronize_session=False)
    db.commit()
    return {"message": "OK"}
