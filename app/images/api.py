from fastapi import APIRouter, Depends
from app.dependencies import get_db
from . import schemas
from typing import List
from sqlalchemy.orm import Session
import boto3
import os

router = APIRouter(prefix="/images", dependencies=[Depends(get_db)])


@router.get("", response_model=List[schemas.Image])
def images(db: Session = Depends(get_db), skip: int = 0, limit: int = 10):
    # WIP
    # client = boto3.client('s3', os.getenv('AWS_REGION'))
    # paginator = client.get_paginator('list_objects')
    # page_iterator = paginator.paginate(Bucket=os.getenv('AWS_BUCKET'))
    # for page in page_iterator:
    #    print(page['Contents'])
    return [schemas.Image(url='http://foo.bar')]
