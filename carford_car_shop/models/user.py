from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from models import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(80))
    email: Mapped[str] = mapped_column(String(80), unique=True)
    password: Mapped[str] = mapped_column(String(80))

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password
