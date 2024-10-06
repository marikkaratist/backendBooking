from typing import Optional

from pydantic import BaseModel, Field


class Hotel(BaseModel):
    title: str
    name: str


class HotelPATCH(BaseModel):
    title: Optional[str] = Field(None)
    name: Optional[str] = Field(None)
