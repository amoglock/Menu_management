import uuid

from pydantic import BaseModel


class BaseResponse(BaseModel):
    id: uuid.UUID
    title: str
    description: str


class SubmenuResponse(BaseResponse):
    dishes_count: int


class MenuResponse(SubmenuResponse):
    submenus_count: int


class DishResponse(BaseResponse):
    price: str


class MenuCreate(BaseModel):
    title: str
    description: str


class SubmenuCreate(MenuCreate):
    pass


class DishCreate(MenuCreate):
    price: str
