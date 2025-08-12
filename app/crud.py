from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.hero import Hero


async def get_hero_by_name(session: AsyncSession, name: str) -> Hero | None:
    result = await session.execute(select(Hero).where(Hero.name == name))
    return result.scalars().first()


async def create_hero(session: AsyncSession, name: str, hero_powerstates: dict) -> Hero:
    hero_name = name.lower()
    hero = Hero(
        name=hero_name,
        intelligence=int(hero_powerstates.get("intelligence", 0)),
        strength=int(hero_powerstates.get("strength", 0)),
        speed=int(hero_powerstates.get("speed", 0)),
        power=int(hero_powerstates.get("power", 0)),
    )
    session.add(hero)
    await session.commit()
    await session.refresh(hero)
    return hero
