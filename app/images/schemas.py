from pydantic import BaseModel, Field
import datetime


class Image(BaseModel):
    url: str = Field(title="Image url")
    date: datetime.datetime = Field(title="Image last modified")
