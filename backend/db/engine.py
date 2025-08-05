from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


DATABASE_URL = "sqlite:///./ovpn.db"
engin = create_engine(url=DATABASE_URL, connect_args={"check_same_thrads":False})

Base = declarative_base()

sessionLocal = sessionmaker(
    bind=engin,
    autoflush=False
)

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()