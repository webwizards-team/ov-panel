from sqlalchemy.orm import Mapped, mapped_column
from .engine import Base
from datetime import date

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(unique=True)
    expiry_date: Mapped[date]
    is_active: Mapped[bool] = mapped_column(default=True)
    owner: Mapped[str] = mapped_column(nullable=False)
    