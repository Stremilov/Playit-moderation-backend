from src.api.auth_users import router as auth_user_router
from src.api.tasks import router as tasks_router
from src.api.users import router as users_router
from src.api.websocket import router as websocket_router

users_router.include_router(auth_user_router)
all_routers = [tasks_router, users_router, websocket_router]
