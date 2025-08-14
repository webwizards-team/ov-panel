from fastapi import APIRouter
from schema.output import ServerInfo
from operations.server_info import get_server_info


router = APIRouter(prefix="/server", tags=["Server info"])


@router.get("/info", response_model=ServerInfo)
async def get_server_information():
    result = await get_server_info()
    return result
