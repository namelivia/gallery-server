from fastapi import APIRouter, Depends
from app.dependencies import get_db
from . import schemas
from typing import List
from sqlalchemy.orm import Session

router = APIRouter(prefix="/images", dependencies=[Depends(get_db)])


@router.get("", response_model=List[schemas.Image])
def images(db: Session = Depends(get_db), skip: int = 0, limit: int = 10):
    return [schemas.Image(url='http://foo.bar')]
