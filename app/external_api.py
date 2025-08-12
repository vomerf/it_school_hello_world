import httpx
from app.core.config import settings


async def fetch_hero_by_name(name: str) -> tuple | None:
    url = f"{settings.BASE_URL_HERO}/{settings.TOKEN_HERO}/search/{name}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        try:
            data = response.json()
        except Exception as e:
            raise Exception(f"Ошибка парсинга JSON: {e}")
        if data["response"] == "success":
            for hero in data["results"]:
                if hero["name"].lower() == name.lower():
                    return hero["name"].lower(), hero["powerstats"]
    return None, None
