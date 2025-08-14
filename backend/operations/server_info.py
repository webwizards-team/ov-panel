import psutil
import time
from fastapi import HTTPException
from logger import logger
from schema.output import ServerInfo


async def get_server_info() -> ServerInfo:
    try:
        return ServerInfo(
            cpu=psutil.cpu_percent(interval=0.5),
            memory_total=psutil.virtual_memory().total,
            memory_used=psutil.virtual_memory().used,
            memory_percent=psutil.virtual_memory().percent,
            disk_total=psutil.disk_usage("/").total,
            disk_used=psutil.disk_usage("/").used,
            disk_percent=psutil.disk_usage("/").percent,
            uptime=int(time.time() - psutil.boot_time()),
        )
    except Exception as e:
        logger.error(f"error when get server info: {e}")
        raise HTTPException(
            status_code=500, detail="error when get server info, please check the logs"
        )
