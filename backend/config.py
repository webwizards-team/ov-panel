from pydantic_settings import BaseSettings


class Setting(BaseSettings):
    USERNAME: str
    PASSWORD: str
    URLPATH: str
    DEBUG: str

    class Config:
        env_file = "../.env"


config = Setting()
