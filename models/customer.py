from typing import Optional, List
from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models import Base


class Customer(Base):
    __tablename__ = "customer"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(80), nullable=False)
    email: Mapped[Optional[str]] = mapped_column(String(120))
    cars: Mapped[Optional[List["Car"]]] = relationship("Car", back_populates="owner", uselist=True)  # type: ignore

    def __init__(self, name, email):
        self.name = name
        self.email = email

    def get_cars(self):
        if self.cars:
            cars = []
            for car in self.cars:
                cars.append(
                    {
                        "id": car.id,
                        "model": car.model,
                        "color": car.color,
                        "owner": car.owner_id,
                    }
                )
            return cars
        else:
            return []

    def can_add_new_car(self):
        return len(self.cars) < 3

    def is_potential_buyer(self):
        return len(self.cars) == 0
