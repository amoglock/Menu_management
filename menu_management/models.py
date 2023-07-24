import uuid

from sqlalchemy import MetaData, String, ForeignKey, Table, Column, UUID

metadata = MetaData()

menu = Table(
    "menu",
    metadata,
    Column("id", UUID, primary_key=True, default=uuid.uuid4),
    Column("title", String, nullable=False, unique=True),
    Column("description", String, nullable=False),
)

submenu = Table(
    "submenu",
    metadata,
    Column("id", UUID, primary_key=True, default=uuid.uuid4),
    Column("title", String, nullable=False, unique=True),
    Column("description", String, nullable=False),
    Column("menu_group", UUID, ForeignKey("menu.id", ondelete='CASCADE')),
)

dish = Table(
    "dish",
    metadata,
    Column("id", UUID, primary_key=True, default=uuid.uuid4),
    Column("title", String, nullable=False, unique=True),
    Column("description", String, nullable=False),
    Column("price", String, nullable=False),
    Column("submenu_group", UUID, ForeignKey("submenu.id", ondelete='CASCADE')),
)
