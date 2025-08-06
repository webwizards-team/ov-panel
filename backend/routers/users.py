from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from schema.output import Users as ShowUsers
from schema._input import CreateUser, UpdateUser
from db.engine import get_db
from db import crud

router = APIRouter(prefix="/user", tags=["Users"])


@router.get("/all", response_model=List[ShowUsers])
async def get_all_users(db: Session = Depends(get_db)):
    all_users = crud.get_all_users(db)
    return all_users


@router.post("/create", response_model=ShowUsers)
async def create_user(
    request: CreateUser,
    db: Session = Depends(get_db),
):
    result = crud.create_user(db, request, "test name")
    return result


@router.put("/update")
async def update_user(request: UpdateUser, db: Session = Depends(get_db)):
    result = crud.update_user(db, request)
    return result


@router.delete("/delete/{name}")
async def delete_user(name: str, db: Session = Depends(get_db)):
    result = crud.delete_user(db, name)
    return result
