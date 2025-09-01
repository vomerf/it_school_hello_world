from fastapi import APIRouter

from .endpoints import hero_router, redis_router, health_router


main_router = APIRouter()

main_router.include_router(hero_router, prefix='/hero', tags=['hero'])
main_router.include_router(health_router, tags=['health_check'])
main_router.include_router(redis_router, tags=['redis_cache'])
