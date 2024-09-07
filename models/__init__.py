from models.base import Base
from models.connection import Session, inspector, create_tables
from models.customer import Customer
from models.car import Car, ModelEnum, ColorEnum

if not inspector.get_table_names():
    create_tables()
