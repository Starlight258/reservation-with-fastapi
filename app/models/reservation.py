from typing import Optional
from pydantic import BaseModel
from sqlmodel import Field, SQLModel


class Reservation(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    date: str = Field(index=True)
    time: str = Field(index=True)


class ReservationCreateDto(BaseModel):
    name: str
    date: str
    time: str 