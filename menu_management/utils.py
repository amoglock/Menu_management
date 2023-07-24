from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from menu_management.models import submenu, dish
from menu_management.schemas import DishCreate


async def submenus_counter(menu_id: str, session: AsyncSession) -> int:
    query = select(func.count()).select_from(submenu).where(submenu.c.menu_group == menu_id)
    result = await session.execute(query)
    return result.all()[0][0]


async def dishes_counter(session: AsyncSession, menu_id: str = None, submenu_id: str = None) -> int:
    if menu_id:
        query = select(func.count()).select_from(dish).filter(dish.c.submenu_group == select(submenu.c.id).
                                                              where(submenu.c.menu_group == menu_id).scalar_subquery())
        result = await session.execute(query)
        return result.all()[0][0]
    if submenu_id:
        query = select(func.count()).select_from(dish).where(dish.c.submenu_group == submenu_id)
        result = await session.execute(query)
        return result.all()[0][0]


async def new_dish_price_validator(dish_instance: DishCreate):
    dish_instance.price = str("{:.2f}".format(float(dish_instance.price)))
    return dish_instance


async def get_result_from_base(query, session: AsyncSession):
    result = await session.execute(query)
    mapped_result = [dict(r._mapping) for r in result.all()]
    return mapped_result
