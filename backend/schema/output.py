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


class ServerInfo(BaseModel):
    cpu: float
    memory_total: int
    memory_used: int
    memory_percent: float
    disk_total: int
    disk_used: int
    disk_percent: float
    uptime: int
