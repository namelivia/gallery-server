from fastapi import APIRouter, Depends
from app.dependencies import get_db
from sqlalchemy.orm import Session
from . import schemas
from typing import List
import logging
import boto3
import os

router = APIRouter(prefix="/images", dependencies=[Depends(get_db)])

logger = logging.getLogger(__name__)


@router.get("", response_model=List[schemas.Image])
def images(db: Session = Depends(get_db), page: int = 0):
    page_size = 9

    # Retrieve data
    client = boto3.client("s3", os.getenv("AWS_REGION"))
    paginator = client.get_paginator("list_objects_v2")
    page_iterator = paginator.paginate(Bucket=os.getenv("AWS_BUCKET"))

    # Filter data
    all_items = []
    for s3_page in page_iterator:
        items = s3_page["Contents"]
        for item in items:
            if item["Key"].endswith(".jpg"):
                all_items.append(item)

    all_items = sorted(all_items, key=lambda i: i["LastModified"], reverse=True)

    # Get only needed items
    result = []
    start = page * page_size
    end = start + page_size
    for item in all_items[start:end]:
        try:
            signed_url = client.generate_presigned_url(
                "get_object",
                Params={"Bucket": os.getenv("AWS_BUCKET"), "Key": item["Key"]},
                ExpiresIn=3600,
            )
        except Exception:
            pass
        image = schemas.Image(url=signed_url, date=item["LastModified"])
        result.append(image)
    return result
