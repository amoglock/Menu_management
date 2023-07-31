from sqlalchemy import Select, func
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Submenu, Dish


async def submenus_counter(menu_id: str, session: AsyncSession) -> int:
    query = Select(func.count()).select_from(Submenu).where(Submenu.menu_group == menu_id)
    result = await session.scalar(query)
    return result


async def dishes_counter(session: AsyncSession, menu_id: str = None, submenu_id: str = None) -> int:
    if menu_id:
        query = Select(func.count()).select_from(Dish).filter(Dish.submenu_group == Select(Submenu.id).
                                                              where(Submenu.menu_group == menu_id).scalar_subquery())
        result = await session.scalar(query)
        return result
    if submenu_id:
        query = Select(func.count()).select_from(Dish).where(Dish.submenu_group == submenu_id)
        result = await session.scalar(query)
        return result
