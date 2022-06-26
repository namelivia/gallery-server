from pydantic import BaseModel, Field
from typing import List
import datetime


class Image(BaseModel):
    url: str = Field(title="Image url")
    date: datetime.datetime = Field(title="Image last modified")
    labels: List[str] = Field(title="Labels for the image")
