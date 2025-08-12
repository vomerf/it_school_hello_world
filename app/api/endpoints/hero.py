from typing import Literal, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.crud import create_hero, get_hero_by_name
from app.external_api import fetch_hero_by_name
from app.models.hero import Hero
from app.schemas.hero import FilterInfo, HeroCreate, HeroesResponse, HeroOut
from app.utils.hero import apply_filter

router = APIRouter()


@router.post("/", response_model=HeroOut)
async def add_hero(hero_in: HeroCreate, session: AsyncSession = Depends(get_session)):
    hero = await get_hero_by_name(session, hero_in.name)
    if hero:
        return hero

    ext_hero_name, powerstates = await fetch_hero_by_name(hero_in.name)
    if not ext_hero_name:
        raise HTTPException(
            status_code=404, detail=f"Герой с данным именем {hero_in.name} не может быть создан."
        )

    hero = await create_hero(session, ext_hero_name, powerstates)
    return hero


@router.get("/", response_model=HeroesResponse)
async def get_heroes(
    name: Optional[str] = Query(None, description="Имя героя для точного поиска"),
    intelligence: Optional[int] = Query(None),
    intelligence_op: Literal["gte", "lte", "eq"] = Query("eq"),
    strength: Optional[int] = Query(None),
    strength_op: Literal["gte", "lte", "eq"] = Query("eq"),
    speed: Optional[int] = Query(None),
    speed_op: Literal["gte", "lte", "eq"] = Query("eq"),
    power: Optional[int] = Query(None),
    power_op: Literal["gte", "lte", "eq"] = Query("eq"),
    session: AsyncSession = Depends(get_session)
):
    filters = []
    filters_info = []

    if name is not None:
        filters.append(Hero.name == name)
        filters_info.append(FilterInfo(field="name", op="eq", value=name))

    if intelligence is not None:
        filters.append(apply_filter(Hero.intelligence, intelligence_op, intelligence))
        filters_info.append(FilterInfo(field="intelligence", op=intelligence_op, value=str(intelligence)))

    if strength is not None:
        filters.append(apply_filter(Hero.strength, strength_op, strength))
        filters_info.append(FilterInfo(field="strength", op=strength_op, value=str(strength)))

    if speed is not None:
        filters.append(apply_filter(Hero.speed, speed_op, speed))
        filters_info.append(FilterInfo(field="speed", op=speed_op, value=str(speed)))

    if power is not None:
        filters.append(apply_filter(Hero.power, power_op, power))
        filters_info.append(FilterInfo(field="power", op=power_op, value=str(power)))

    query = select(Hero).where(*filters)
    result = await session.execute(query)
    heroes = result.scalars().all()

    if not heroes:
        return HeroesResponse(heroes=None, filters_no_results=filters_info)

    return HeroesResponse(heroes=heroes, filters_no_results=None)
