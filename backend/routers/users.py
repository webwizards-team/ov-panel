from typing import List
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from schema.output import Users as ShowUsers
from schema._input import CreateUser, UpdateUser
from db.engine import get_db
from db import crud
from operations.user_management import (
    create_user_on_server,
    delete_user_on_server,
    download_ovpn_file,
)
from auth.auth import get_current_user

router = APIRouter(prefix="/user", tags=["Users"])


@router.get("/all", response_model=List[ShowUsers])
async def get_all_users(
    db: Session = Depends(get_db), user: dict = Depends(get_current_user)
):
    all_users = crud.get_all_users(db)
    return all_users


@router.get("/dwonload/ovpn/{name}", response_model=ShowUsers)
async def download_ovpn(
    name: str,
    user: dict = Depends(get_current_user),
):
    response = download_ovpn_file(name)
    if response:
        return FileResponse(
            path=response,
            filename=f"{name}.ovpn",
            media_type="application/x-openvpn-profile",
        )
    else:
        raise HTTPException(status_code=404, detail="OVPN file not found")


@router.post("/create", response_model=ShowUsers)
async def create_user(
    request: CreateUser,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    server_result = create_user_on_server(request.name, request.expiry_date)
    if server_result == "error":
        raise HTTPException(status_code=500, detail="Server error while creating user")

    db_result = crud.create_user(db, request, "test name")
    return db_result


@router.put("/update")
async def update_user(
    request: UpdateUser,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    result = crud.update_user(db, request)
    return result


@router.delete("/delete/{name}")
async def delete_user(
    name: str, db: Session = Depends(get_db), user: dict = Depends(get_current_user)
):
    server_result = await delete_user_on_server(name)
    if server_result == "not_found":
        raise HTTPException(status_code=404, detail="User not found on server")
    db_result = crud.delete_user(db, name)
    return db_result
