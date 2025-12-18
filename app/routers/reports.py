from fastapi import status, HTTPException, Depends, APIRouter , Response
from sqlalchemy.orm import Session
from .. import models, schemas, utils , oauth2
from ..database import get_db
from . import service_reports

router = APIRouter(
    prefix="/reports",
    tags=["Reports"]
)


@router.post("/get" , response_model=schemas.ReportOut)
async def get_report_endpoint( times : schemas.GetReport , db: Session = Depends(get_db) , current_user: int = Depends(oauth2.get_current_user)):

    a = service_reports.get_report(db , times.from_time , times.to_time)

    if a is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Report not found")


    return a
