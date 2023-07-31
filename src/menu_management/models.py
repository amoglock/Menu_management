import uuid

from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from sqlalchemy import ForeignKey


class Base(DeclarativeBase):
    pass


class Menu(Base):
    __tablename__ = "menu"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(nullable=False, unique=True)
    description: Mapped[str] = mapped_column(nullable=False)

    def as_dict(self):
        return {"id": self.id, "title": self.title, "description": self.description}


class Submenu(Base):
    __tablename__ = "submenu"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(nullable=False, unique=True)
    description: Mapped[str] = mapped_column(nullable=False)
    menu_group: Mapped[uuid.UUID] = mapped_column(ForeignKey("menu.id", ondelete='CASCADE'))

    def as_dict(self):
        return {"id": self.id, "title": self.title, "description": self.description, "menu_group": self.menu_group}


class Dish(Base):
    __tablename__ = "dish"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(nullable=False, unique=True)
    description: Mapped[str] = mapped_column(nullable=False)
    price: Mapped[str] = mapped_column(nullable=False)
    submenu_group: Mapped[uuid.UUID] = mapped_column(ForeignKey("submenu.id", ondelete='CASCADE'))

    def as_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "price": self.price,
            "submenu_group": self.submenu_group
        }
