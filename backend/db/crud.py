from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import datetime

from logger import logger
from schema.output import Users as ShowUsers
from schema._input import CreateUser, UpdateUser
from .models import User, Admin


def get_all_users(db: Session):
    users = db.query(User).all()
    return users


def create_user(db: Session, request: CreateUser, owner: str):
    if db.query(User).filter(User.name == request.name).first():
        raise HTTPException(
            status_code=400, detail="user with this name already exists"
        )

    new_user = User(
        name=request.name,
        expiry_date=request.expiry_date,
        owner=owner,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    logger.info(f"user created successfully: {request.name}")
    return new_user


def update_user(db: Session, request: UpdateUser):
    user = db.query(User).filter(User.name == request.name).first()
    if not user:
        raise HTTPException(status_code=404, detail="user not found on database")

    user.expiry_date = request.expiry_date
    db.commit()
    db.refresh(user)
    return {"detail": "User updated successfully"}


def change_user_status(db: Session, name: str, status: bool) -> bool:
    try:
        user = db.query(User).filter(User.name == name).first()
        user.is_active == status
        db.commit()
        db.refresh(user)
        return True
    except Exception as e:
        logger.error(f"Error when change status for user:{name} on db: {e}")
        return False


def get_expired_users(db: Session):
    return (
        db.query(User)
        .filter(User.expiry_date < datetime.now(), User.is_active == True)
        .all()
    )


def delete_user(db: Session, name: str):
    user = db.query(User).filter(User.name == name).first()
    if not user:
        raise HTTPException(status_code=404, detail="user not found on database")

    db.delete(user)
    db.commit()
    return {"detail": "User deleted successfully"}


# admins crud
def get_all_admins(db: Session):
    admins = db.query(Admin).all()
    return admins


def it_is_admin(db: Session, username: str):
    admin = db.query(Admin).filter(Admin.username == username).first()
    if not admin:
        return False
    return admin
