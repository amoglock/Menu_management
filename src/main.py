from fastapi import FastAPI

from menu_management.router import menu_router

app = FastAPI(
    title="Menu management"
)

app.include_router(menu_router)
