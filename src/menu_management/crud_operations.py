from typing import List, Optional

from fastapi import HTTPException
from sqlalchemy import Select, update, delete
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Menu, Submenu, Dish
from .schemas import MenuResponse, MenuCreate, SubmenuResponse, SubmenuCreate, DishResponse, DishCreate
from .utils import submenus_counter, dishes_counter


class Crud:
    @staticmethod
    async def get_all_menu(session: AsyncSession) -> List[Optional[MenuResponse]]:
        query = Select(Menu)
        result = await session.scalars(query)
        return [MenuResponse(**r.as_dict(), submenus_count=await submenus_counter(r.id, session),
                             dishes_count=await dishes_counter(session, menu_id=r.id)) for r in result]

    @staticmethod
    async def post_new_menu(new_menu: MenuCreate, session: AsyncSession) -> MenuResponse:
        stmt = insert(Menu).values(new_menu.model_dump())
        await session.execute(stmt)
        await session.commit()

        query = Select(Menu).where(Menu.title == new_menu.title)
        result = await session.scalar(query)

        return MenuResponse(**result.as_dict(), submenus_count=0, dishes_count=0)

    @staticmethod
    async def get_menu_by_id(menu_id: str, session: AsyncSession) -> MenuResponse:
        query = Select(Menu).where(Menu.id == menu_id)
        result = await session.scalar(query)

        if not result:
            raise HTTPException(status_code=404, detail="menu not found")

        return MenuResponse(**result.as_dict(), submenus_count=await submenus_counter(result.id, session),
                            dishes_count=await dishes_counter(session, menu_id=result.id))

    @staticmethod
    async def patch_menu_by_id(menu_id: str, new_menu: MenuCreate, session: AsyncSession) -> MenuResponse:
        query = Select(Menu).where(Menu.id == menu_id)
        result = await session.scalar(query)
        if not result:
            raise HTTPException(status_code=404, detail="menu not found")

        stmt = update(Menu).where(Menu.id == menu_id).values(new_menu.model_dump())
        await session.execute(stmt)
        await session.commit()

        query = Select(Menu).where(Menu.id == menu_id)
        result = await session.scalar(query)

        return MenuResponse(**result.as_dict(), submenus_count=await submenus_counter(result.id, session),
                            dishes_count=await dishes_counter(session, menu_id=result.id))

    @staticmethod
    async def delete_menu(menu_id: str, session: AsyncSession) -> dict[str, str | bool]:
        query = Select(Menu).where(Menu.id == menu_id)
        result = await session.execute(query)
        if not result.all():
            raise HTTPException(status_code=404, detail="menu not found")

        stmt = delete(Menu).where(Menu.id == menu_id)
        await session.execute(stmt)
        await session.commit()

        return {"satus": True, "message": "The menu has been deleted"}

    @staticmethod
    async def get_all_submenus(menu_id: str, session: AsyncSession) -> List[SubmenuResponse]:
        query = Select(Submenu).where(Submenu.menu_group == menu_id)
        result = await session.scalars(query)

        return [SubmenuResponse(**r.as_dict(),
                                dishes_count=await dishes_counter(session, submenu_id=r.id)) for r in result]

    @staticmethod
    async def get_specific_submenu(menu_id: str, submenu_id: str, session: AsyncSession) -> SubmenuResponse:
        query = Select(Submenu).where(Submenu.id == submenu_id).where(Submenu.menu_group == menu_id)
        result = await session.scalar(query)

        if not result:
            raise HTTPException(status_code=404, detail="submenu not found")

        return SubmenuResponse(**result.as_dict(), dishes_count=await dishes_counter(session, submenu_id=result.id))

    @staticmethod
    async def post_new_submenu(menu_id: str, new_submenu: SubmenuCreate, session: AsyncSession) -> SubmenuResponse:
        query = Select(Menu).where(Menu.id == menu_id)
        result = await session.execute(query)
        if not result.all():
            raise HTTPException(status_code=404, detail="menu not found")

        stmt = insert(Submenu).values(**new_submenu.model_dump(), menu_group=menu_id)
        await session.execute(stmt)
        await session.commit()

        query = Select(Submenu).where(Submenu.title == new_submenu.title)
        result = await session.scalar(query)

        return SubmenuResponse(**result.as_dict(), dishes_count=0)

    @staticmethod
    async def patch_submenu(
            menu_id: str, submenu_id: str, new_submenu: SubmenuCreate, session: AsyncSession) -> SubmenuResponse:
        query = Select(Submenu).where(Submenu.id == submenu_id).where(Submenu.menu_group == menu_id)
        result = await session.scalar(query)
        if not result:
            raise HTTPException(status_code=404, detail="submenu not found")

        stmt = update(Submenu).where(Submenu.id == submenu_id).values(new_submenu.model_dump())
        await session.execute(stmt)
        await session.commit()

        query = Select(Submenu).where(Submenu.id == submenu_id)
        result = await session.scalar(query)

        return SubmenuResponse(**result.as_dict(), dishes_count=await dishes_counter(session, submenu_id=result.id))

    @staticmethod
    async def delete_submenu(menu_id: str, submenu_id: str, session: AsyncSession) -> dict[str, str | bool]:
        query = Select(Submenu).where(Submenu.id == submenu_id).where(Submenu.menu_group == menu_id)
        result = await session.scalar(query)
        if not result:
            raise HTTPException(status_code=404, detail="submenu not found")

        stmt = delete(Submenu).where(Submenu.id == submenu_id)
        await session.execute(stmt)
        await session.commit()

        return {"satus": True, "message": "The submenu has been deleted"}

    @staticmethod
    async def get_dishes_from_submenu(submenu_id: str, session: AsyncSession) -> List[DishResponse]:
        query = Select(Dish).where(Dish.submenu_group == submenu_id)
        result = await session.scalars(query)

        return [DishResponse(**r.as_dict()) for r in result]

    @staticmethod
    async def get_specific_dish(dish_id: str, session: AsyncSession) -> DishResponse:
        query = Select(Dish).where(Dish.id == dish_id)
        result = await session.scalar(query)

        if not result:
            raise HTTPException(status_code=404, detail="dish not found")

        return DishResponse(**result.as_dict())

    @staticmethod
    async def post_new_dish(submenu_id: str, new_dish: DishCreate, session: AsyncSession) -> DishResponse:
        query = Select(Submenu).where(Submenu.id == submenu_id)
        result = await session.scalar(query)

        if not result:
            raise HTTPException(status_code=404, detail="submenu not found")

        new_dish.price = str("{:.2f}".format(float(new_dish.price)))

        stmt = insert(Dish).values(**new_dish.model_dump(), submenu_group=submenu_id)
        await session.execute(stmt)
        await session.commit()

        query = Select(Dish).where(Dish.price == new_dish.price)
        result = await session.scalar(query)

        return DishResponse(**result.as_dict())

    @staticmethod
    async def patch_dish(dish_id: str, new_dish: DishCreate, session: AsyncSession) -> DishResponse:
        query = Select(Dish).where(Dish.id == dish_id)
        result = await session.scalar(query)

        if not result:
            raise HTTPException(status_code=404, detail="dish not found")

        stmt = update(Dish).where(Dish.id == dish_id).values(new_dish.model_dump())
        await session.execute(stmt)
        await session.commit()

        query = Select(Dish).where(Dish.title == new_dish.title)
        result = await session.scalar(query)

        return DishResponse(**result.as_dict())

    @staticmethod
    async def delete_dish(dish_id: str, session: AsyncSession) -> dict[str, str | bool]:
        query = Select(Dish).where(Dish.id == dish_id)
        result = await session.scalar(query)

        if not result:
            raise HTTPException(status_code=404, detail="dish not found")

        stmt = delete(Dish).where(Dish.id == dish_id)
        await session.execute(stmt)
        await session.commit()

        return {"satus": True, "message": "The dish has been deleted"}
