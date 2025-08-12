from pydantic import BaseModel, ConfigDict, constr


class HeroBase(BaseModel):
    name: str
    intelligence: int
    strength: int
    speed: int
    power: int


class HeroCreate(BaseModel):
    name: constr(min_length=1)


class HeroOut(HeroBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class FilterInfo(BaseModel):
    field: str
    op: str
    value: str


class HeroesResponse(BaseModel):
    heroes: list[HeroOut] | None = None
    filters_no_results: list[FilterInfo] | None = None
