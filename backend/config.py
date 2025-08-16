import os
from pydantic_settings import BaseSettings


class Setting(BaseSettings):
    ADMIN_USERNAME: str
    ADMIN_PASSWORD: str
    URLPATH: str
    DEBUG: str

    class Config:
        env_file = os.path.join(os.path.dirname(__file__), "..", ".env")


config = Setting()
