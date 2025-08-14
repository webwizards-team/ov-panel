from .users import router as user_router
from .server import router as server_router

all_routers = [
    user_router,
    server_router,
]
