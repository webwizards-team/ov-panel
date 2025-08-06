from pydantic import BaseModel, Field
from datetime import date
from typing import Optional


class CreateUser(BaseModel):
    name: str = Field( min_length=3, max_length=10)
    traffic: int = Field(default=0, ge=0, le=999)
    expiry_date: date


class UpdateUser(BaseModel):
    traffic: Optional[int] = Field(None, ge=0, le=999)
    expiry_date: date