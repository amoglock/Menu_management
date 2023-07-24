from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session
from menu_management.models import menu, submenu, dish
from menu_management.schemas import MenuCreate, MenuResponse, SubmenuResponse, SubmenuCreate, DishResponse, DishCreate
from menu_management.utils import submenus_counter, dishes_counter, new_dish_price_validator, get_result_from_base

menu_router = APIRouter(
    prefix="/api/v1/menus",
    tags=["Menu management"]
)


@menu_router.get("/", response_model=List[MenuResponse], tags=["Menu part"])
async def get_all_menus(session: AsyncSession = Depends(get_async_session)):
    query = select(menu)

    result = await get_result_from_base(query, session)
    return [MenuResponse(**r, submenus_count=await submenus_counter(r.get("id"), session),
                         dishes_count=await dishes_counter(session, menu_id=r.get("id"))) for r in result]


@menu_router.get("/{menu_id}", response_model=MenuResponse, tags=["Menu part"])
async def get_specific_menu(menu_id: str, session: AsyncSession = Depends(get_async_session)):
    query = select(menu).where(menu.c.id == menu_id)
    result = await get_result_from_base(query, session)

    if not result:
        raise HTTPException(status_code=404, detail="menu not found")

    return [MenuResponse(**r, submenus_count=await submenus_counter(r.get("id"), session),
                         dishes_count=await dishes_counter(session, menu_id=r.get("id"))) for r in result][0]


@menu_router.post("/", status_code=201, response_model=MenuResponse, tags=["Menu part"])
async def post_new_menu(new_menu: MenuCreate, session: AsyncSession = Depends(get_async_session)):
    stmt = insert(menu).values(new_menu.model_dump())
    await session.execute(stmt)
    await session.commit()

    query = select(menu).where(menu.c.title == new_menu.title)
    result = await get_result_from_base(query, session)
    return [MenuResponse(**r, submenus_count=await submenus_counter(r.get("id"), session),
                         dishes_count=await dishes_counter(session, menu_id=r.get("id"))) for r in result][0]


@menu_router.patch("/{menu_id}", response_model=MenuResponse, tags=["Menu part"])
async def patch_menu(menu_id: str, new_menu: MenuCreate, session: AsyncSession = Depends(get_async_session)):
    query = select(menu).where(menu.c.id == menu_id)
    result = await session.execute(query)
    if not result.all():
        raise HTTPException(status_code=404, detail="menu not found")

    stmt = update(menu).where(menu.c.id == menu_id).values(new_menu.model_dump())
    await session.execute(stmt)
    await session.commit()

    query = select(menu).where(menu.c.id == menu_id)
    result = await get_result_from_base(query, session)

    return [MenuResponse(**r, submenus_count=await submenus_counter(r.get("id"), session),
                         dishes_count=await dishes_counter(session, menu_id=r.get("id"))) for r in result][0]


@menu_router.delete("/{menu_id}", tags=["Menu part"])
async def delete_menu(menu_id: str, session: AsyncSession = Depends(get_async_session)):
    query = select(menu).where(menu.c.id == menu_id)
    result = await session.execute(query)
    if not result.all():
        raise HTTPException(status_code=404, detail="menu not found")

    stmt = delete(menu).where(menu.c.id == menu_id)
    await session.execute(stmt)
    await session.commit()

    return {"satus": True, "message": "The menu has been deleted"}


@menu_router.get("/{menu_id}/submenus", response_model=List[SubmenuResponse], tags=["Submenu part"])
async def get_all_submenus(menu_id: str, session: AsyncSession = Depends(get_async_session)):
    query = select(submenu).where(submenu.c.menu_group == menu_id)
    result = await get_result_from_base(query, session)

    return [SubmenuResponse(**r, dishes_count=await dishes_counter(session, submenu_id=r.get("id"))) for r in result]


@menu_router.get("/{menu_id}/submenus/{submenu_id}", response_model=SubmenuResponse, tags=["Submenu part"])
async def get_specific_submenu(menu_id: str, submenu_id: str, session: AsyncSession = Depends(get_async_session)):
    query = select(submenu).where(submenu.c.id == submenu_id).where(submenu.c.menu_group == menu_id)
    result = await get_result_from_base(query, session)

    if not result:
        raise HTTPException(status_code=404, detail="submenu not found")

    return [SubmenuResponse(**r, dishes_count=await dishes_counter(session, submenu_id=r.get("id"))) for r in result][0]


@menu_router.post("/{menu_id}/submenus", status_code=201, response_model=SubmenuResponse, tags=["Submenu part"])
async def post_new_submenu(
        menu_id: str, new_submenu: SubmenuCreate, session: AsyncSession = Depends(get_async_session)
):
    query = select(menu).where(menu.c.id == menu_id)
    result = await session.execute(query)
    if not result.all():
        raise HTTPException(status_code=404, detail="menu not found")

    stmt = insert(submenu).values(**new_submenu.model_dump(), menu_group=menu_id)
    await session.execute(stmt)
    await session.commit()

    query = select(submenu).where(submenu.c.title == new_submenu.title)
    result = await get_result_from_base(query, session)

    return [SubmenuResponse(**r, dishes_count=await dishes_counter(session, submenu_id=r.get("id"))) for r in result][0]


@menu_router.patch("/{menu_id}/submenus/{submenu_id}", response_model=SubmenuResponse, tags=["Submenu part"])
async def patch_submenu(
        menu_id: str, submenu_id: str, new_submenu: SubmenuCreate, session: AsyncSession = Depends(get_async_session)):

    query = select(submenu).where(submenu.c.id == submenu_id).where(submenu.c.menu_group == menu_id)
    result = await session.execute(query)
    if not result.all():
        raise HTTPException(status_code=404, detail="submenu not found")

    stmt = update(submenu).where(submenu.c.id == submenu_id).values(new_submenu.model_dump())
    await session.execute(stmt)
    await session.commit()

    query = select(submenu).where(submenu.c.id == submenu_id)
    result = await get_result_from_base(query, session)

    return [SubmenuResponse(**r, dishes_count=await dishes_counter(session, submenu_id=r.get("id"))) for r in result][0]


@menu_router.delete("/{menu_id}/submenus/{submenu_id}", tags=["Submenu part"])
async def delete_submenu(menu_id: str, submenu_id: str, session: AsyncSession = Depends(get_async_session)):
    query = select(submenu).where(submenu.c.id == submenu_id).where(submenu.c.menu_group == menu_id)
    result = await session.execute(query)
    if not result.all():
        raise HTTPException(status_code=404, detail="submenu not found")

    stmt = delete(submenu).where(submenu.c.id == submenu_id)
    await session.execute(stmt)
    await session.commit()

    return {"satus": True, "message": "The menu has been deleted"}


@menu_router.get("/{menu_id}/submenus/{submenu_id}/dishes", response_model=List[DishResponse], tags=["Dishes part"])
async def get_dishes_from_submenu(submenu_id: str, session: AsyncSession = Depends(get_async_session)):

    # query = select(submenu).where(submenu.c.id == submenu_id).where(submenu.c.menu_group == menu_id)
    # result = await session.execute(query)
    # mapped_result = [dict(r._mapping) for r in result.all()]
    # if not mapped_result:
    #     return []

    query = select(dish).where(dish.c.submenu_group == submenu_id)
    result = await get_result_from_base(query, session)

    return [DishResponse(**r) for r in result]


@menu_router.get("/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}", response_model=DishResponse, tags=["Dishes part"])
async def get_specific_dish(dish_id: str, session: AsyncSession = Depends(get_async_session)):

    # query = select(submenu).where(submenu.c.id == submenu_id).where(submenu.c.menu_group == menu_id)
    # result = await session.execute(query)
    # mapped_result = [dict(r._mapping) for r in result.all()]
    # if not mapped_result:
    #     raise HTTPException(status_code=404, detail="submenu not found")

    query = select(dish).where(dish.c.id == dish_id)
    result = await get_result_from_base(query, session)

    if not result:
        raise HTTPException(status_code=404, detail="dish not found")

    return [DishResponse(**r) for r in result][0]


@menu_router.post("/{menu_id}/submenus/{submenu_id}/dishes",
                  status_code=201, tags=["Dishes part"])
async def post_new_dish(
        menu_id: str, submenu_id: str, new_dish: DishCreate, session: AsyncSession = Depends(get_async_session)
):
    query = select(submenu).where(submenu.c.id == submenu_id).where(submenu.c.menu_group == menu_id)
    result = await get_result_from_base(query, session)

    if not result:
        raise HTTPException(status_code=404, detail="submenu not found")

    new_dish: DishCreate = await new_dish_price_validator(new_dish)

    stmt = insert(dish).values(**new_dish.model_dump(), submenu_group=submenu_id)
    await session.execute(stmt)
    await session.commit()

    query = select(dish).where(dish.c.title == new_dish.title)
    result = await get_result_from_base(query, session)

    return [DishResponse(**r) for r in result][0]


@menu_router.patch(
    "/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}", response_model=DishResponse, tags=["Dishes part"])
async def patch_dish(dish_id: str, new_dish: DishCreate, session: AsyncSession = Depends(get_async_session)):

    # query = select(submenu).where(submenu.c.id == submenu_id).where(submenu.c.menu_group == menu_id)
    # result = await MenuActions.get_result_from_base(query, session)
    # # result = await session.execute(query)
    # # mapped_result = [dict(r._mapping) for r in result.all()]
    # if not result:
    #     raise HTTPException(status_code=404, detail="submenu not found")

    query = select(dish).where(dish.c.id == dish_id)
    result = await get_result_from_base(query, session)

    if not result:
        raise HTTPException(status_code=404, detail="dish not found")

    stmt = update(dish).where(dish.c.id == dish_id).values(new_dish.model_dump())
    await session.execute(stmt)
    await session.commit()

    query = select(dish).where(dish.c.title == new_dish.title)
    result = await get_result_from_base(query, session)

    return [DishResponse(**r) for r in result][0]


@menu_router.delete(
    "/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}", tags=["Dishes part"])
async def delete_dish(dish_id: str, session: AsyncSession = Depends(get_async_session)):

    # query = select(submenu).where(submenu.c.id == submenu_id).where(submenu.c.menu_group == menu_id)
    # result = await MenuActions.get_result_from_base(query, session)
    #
    # if not result:
    #     raise HTTPException(status_code=404, detail="submenu not found")

    query = select(dish).where(dish.c.id == dish_id)
    result = await get_result_from_base(query, session)

    if not result:
        raise HTTPException(status_code=404, detail="dish not found")

    stmt = delete(dish).where(dish.c.id == dish_id)
    await session.execute(stmt)
    await session.commit()

    return {"satus": True, "message": "The menu has been deleted"}
