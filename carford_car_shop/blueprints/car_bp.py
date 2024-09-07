from flask_openapi3 import APIBlueprint, Tag
from flask import request

from logger import logger
from models import Car, Customer, ModelEnum, ColorEnum, Session
from schemas import *
from utils import jwt_decode

tag = Tag(name="Cars API", description="Routes to insert, read and remove cars.")

car_bp = APIBlueprint(
    "car",
    __name__,
    url_prefix="/api",
    abp_tags=[tag],
    doc_ui=True,
)

security = [{"jwt": []}]


@car_bp.get("/cars", responses={"200": CarResponseSchema})
def get_all_cars():
    """Get all cars from the database"""
    session = Session()

    cars = session.query(Car).all()
    result = []

    if cars:
        for car in cars:
            car_data = {
                "id": car.id,
                "model": car.model,
                "color": car.color,
                "owner_id": car.owner_id,
            }
            result.append(car_data)

    return {"cars": result}, 200


@car_bp.get("/cars/<id>", responses={"200": CarResponseSchema})
def get_car_by_id(path: IdPathSchema):
    """Get car by the ID from the database"""
    session = Session()
    car_id = path.id

    car = session.query(Car).filter(Car.id == car_id).first()
    if car:
        car_data = {
            "id": car.id,
            "model": car.model,
            "color": car.color,
            "owner_id": car.owner_id,
        }
        return {"cars": car_data}, 200

    return {"message": f"Car of ID {car_id} not found."}, 404


@car_bp.post("/cars", responses={"200": MessageSchema}, security=security)
def add_car(body: CarBodySchema):
    """Add a new car to the database

    Car options:
    model = 'hatch', 'sedan' or 'convertible'
    color = 'yellow', 'blue' or 'gray'
    owner_id = <customer.id>
    """
    token = str(request.authorization).split(" ")[-1]
    token_check = jwt_decode(token)

    if not token_check:
        error_msg = "Login required for insert operation"
        return {"error": error_msg}, 403

    session = Session()

    if not hasattr(ModelEnum, body.model) or not hasattr(ColorEnum, body.color):
        error_msg = "Invalid car Model/Color. Check the input."
        return {"error": error_msg}, 400

    customer = session.query(Customer).filter(Customer.id == body.owner_id).first()
    if not customer.can_add_new_car():
        return {"message": "Customer own 3 cars and can not add a new one."}, 400

    car = Car(model=body.model, color=body.color, owner=customer)
    try:
        session.add(car)
        session.commit()
    except Exception as err:
        error_msg = f"error msg: {err}"
        logger.warning(f"Error to add new car. {error_msg}")
        return {"error": "Car not added"}, 500

    return {"message": f"Car added to customer {car.owner_id}."}, 200


@car_bp.delete("/cars/<id>", responses={"200": MessageSchema}, security=security)
def remove_car_by_id(path: IdPathSchema):
    """Remove car by the ID from the database"""
    token = str(request.authorization).split(" ")[-1]
    token_check = jwt_decode(token)

    if not token_check:
        error_msg = "Login required for insert operation"
        return {"error": error_msg}, 403

    session = Session()
    car_id = path.id
    response = session.query(Car).filter(Car.id == car_id).delete()
    session.commit()

    if not response:
        return {"message": f"Car of ID {car_id} not found."}, 404

    return {"message": "Car deleted"}, 200
