from fastapi import APIRouter

from .endpoints import hero_router

main_router = APIRouter()

main_router.include_router(hero_router, prefix='/hero', tags=['hero'])
