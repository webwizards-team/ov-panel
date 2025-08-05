from pydantic import BaseModel, Field
from datetime import date
from typing import Optional

class Users(BaseModel):
    name: str
    traffic: int
    date: date
