from fastapi import APIRouter

from . import demo
from . import device
from . import message
from. import system

api_router = APIRouter(prefix="/api")
api_router.include_router(demo.router)
api_router.include_router(device.router)
api_router.include_router(message.router)
api_router.include_router(system.router)