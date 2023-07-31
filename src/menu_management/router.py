from typing import List, Optional

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from .crud_operations import Crud
from .schemas import MenuCreate, MenuResponse, SubmenuResponse, SubmenuCreate, DishResponse, DishCreate
from database import get_async_session

menu_router = APIRouter(
    prefix="/api/v1/menus",
    tags=["menu management"]
)


@menu_router.get("/", response_model=List[Optional[MenuResponse]])
async def get_all_menus(session: AsyncSession = Depends(get_async_session)):
    return await Crud.get_all_menu(session)


@menu_router.post("/", status_code=201)
async def post_menu(new_menu: MenuCreate, session: AsyncSession = Depends(get_async_session)):
    return await Crud.post_new_menu(new_menu, session)


@menu_router.get("/{menu_id}", response_model=MenuResponse)
async def get_specific_menu(menu_id: str, session: AsyncSession = Depends(get_async_session)):
    return await Crud.get_menu_by_id(menu_id, session)


@menu_router.patch("/{menu_id}", response_model=MenuResponse)
async def patch_menu(menu_id: str, new_menu: MenuCreate, session: AsyncSession = Depends(get_async_session)):
    return await Crud.patch_menu_by_id(menu_id, new_menu, session)


@menu_router.delete("/{menu_id}", response_model=dict[str, str | bool])
async def delete_menu(menu_id: str, session: AsyncSession = Depends(get_async_session)):
    return await Crud.delete_menu(menu_id, session)


@menu_router.get("/{menu_id}/submenus", response_model=List[SubmenuResponse])
async def get_all_submenus(menu_id: str, session: AsyncSession = Depends(get_async_session)):
    return await Crud.get_all_submenus(menu_id, session)


@menu_router.get("/{menu_id}/submenus/{submenu_id}", response_model=SubmenuResponse)
async def get_specific_submenu(menu_id: str, submenu_id: str, session: AsyncSession = Depends(get_async_session)):
    return await Crud.get_specific_submenu(menu_id, submenu_id, session)


@menu_router.post("/{menu_id}/submenus", status_code=201, response_model=SubmenuResponse,)
async def post_new_submenu(
        menu_id: str, new_submenu: SubmenuCreate, session: AsyncSession = Depends(get_async_session)):
    return await Crud.post_new_submenu(menu_id, new_submenu, session)


@menu_router.patch("/{menu_id}/submenus/{submenu_id}", response_model=SubmenuResponse)
async def patch_submenu(
        menu_id: str, submenu_id: str, new_submenu: SubmenuCreate, session: AsyncSession = Depends(get_async_session)):
    return await Crud.patch_submenu(menu_id, submenu_id, new_submenu, session)


@menu_router.delete("/{menu_id}/submenus/{submenu_id}", response_model=dict[str, str | bool])
async def delete_submenu(
        menu_id: str, submenu_id: str, session: AsyncSession = Depends(get_async_session)):
    return await Crud.delete_submenu(menu_id, submenu_id, session)


@menu_router.get("/{menu_id}/submenus/{submenu_id}/dishes", response_model=List[DishResponse])
async def get_dishes_from_submenu(submenu_id: str, session: AsyncSession = Depends(get_async_session)):
    return await Crud.get_dishes_from_submenu(submenu_id, session)


@menu_router.get("/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}", response_model=DishResponse)
async def get_specific_dish(dish_id: str, session: AsyncSession = Depends(get_async_session)):
    return await Crud.get_specific_dish(dish_id, session)


@menu_router.post("/{menu_id}/submenus/{submenu_id}/dishes", status_code=201, response_model=DishResponse)
async def post_new_dish(
        menu_id: str, submenu_id: str, new_dish: DishCreate, session: AsyncSession = Depends(get_async_session)
):
    return await Crud.post_new_dish(submenu_id, new_dish, session)


@menu_router.patch(
    "/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}", response_model=DishResponse)
async def patch_dish(dish_id: str, new_dish: DishCreate, session: AsyncSession = Depends(get_async_session)):
    return await Crud.patch_dish(dish_id, new_dish, session)


@menu_router.delete("/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}", response_model=dict[str, str | bool])
async def delete_dish(dish_id: str, session: AsyncSession = Depends(get_async_session)):
    return await Crud.delete_dish(dish_id, session)
