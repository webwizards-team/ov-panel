from pydantic import BaseModel, Field
from datetime import date
from typing import Optional


class Users(BaseModel):
    name: str
    is_active: bool
    expiry_date: date
    owner: str

    class Config:
        orm_mode = True
