from fastapi import APIRouter
from . import schemas
from typing import List
import logging
import boto3
from boto3.dynamodb.conditions import Key
import os

router = APIRouter(prefix="/images")

logger = logging.getLogger(__name__)


@router.get("", response_model=List[schemas.Image])
def images(page: int = 0):
    page_size = 9

    # Retrieve data
    client = boto3.client("s3", os.getenv("AWS_REGION"))
    dynamodb = boto3.resource("dynamodb", os.getenv("AWS_REGION"))
    table = dynamodb.Table(os.getenv("DYNAMO_TABLE"))
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

        # Retrieve labels from dynamodb
        labels_query = table.query(
            KeyConditionExpression=Key("image_key").eq(item["Key"])
        )
        labels = [label["name"] for label in labels_query]
        image = schemas.Image(url=signed_url, labels=labels, date=item["LastModified"])
        result.append(image)

    # Finally retrieve labels for the image

    return result
