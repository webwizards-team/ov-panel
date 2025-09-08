from fastapi import APIRouter, Depends


from schema.output import ServerInfo
from operations.server_info import get_server_info
from auth.auth import get_current_user


router = APIRouter(prefix="/server", tags=["Server info"])


@router.get("/info", response_model=ServerInfo)
async def get_server_information(user: dict = Depends(get_current_user)):
    result = await get_server_info()
    return result
