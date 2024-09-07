import enum
from sqlalchemy import Integer, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models import Base


class ModelEnum(str, enum.Enum):
    hatch = "hatch"
    sedan = "sedan"
    convertible = "convertible"


class ColorEnum(str, enum.Enum):
    yellow = "yellow"
    blue = "blue"
    gray = "gray"


class Car(Base):
    __tablename__ = "cars"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    model: Mapped[str] = mapped_column(Enum(ModelEnum))
    color: Mapped[str] = mapped_column(Enum(ColorEnum))
    owner_id: Mapped[int] = mapped_column(ForeignKey("customer.id"), nullable=False)

    owner: Mapped["Customer"] = relationship("Customer", back_populates="cars")  # type: ignore

    def __init__(self, model, color, owner):
        self.model = model
        self.color = color
        self.owner = owner
