from auth.auth import router as login_router
from .users import router as user_router
from .server import router as server_router
from .admins import router as admin_router

all_routers = [
    login_router,
    user_router,
    server_router,
    admin_router,
]
