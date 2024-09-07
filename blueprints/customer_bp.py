from flask_openapi3 import APIBlueprint, Tag

from models import Customer, Car, Session
from schemas import *


tag = Tag(
    name="Customers API", description="Routes to insert, read and remove customers."
)

customer_bp = APIBlueprint(
    "customer",
    __name__,
    url_prefix="/api",
    abp_tags=[tag],
    doc_ui=True,
)


@customer_bp.get("/customers", responses={"200": CustomerResponseSchema})
def get_customers(query: CustomerQuerySchema):
    """Get all customers from the database

    Possible to query for potential buyer. Customers that do not have any car.
    Use query '?buyers=true'
    return list of customer data
    """
    session = Session()
    customers = session.query(Customer).all()

    if query.buyers:
        customers = [
            customer for customer in customers if customer.is_potential_buyer()
        ]

    result = []

    if customers:
        for customer in customers:
            customer_cars = customer.get_cars()
            customer_data = {
                "id": customer.id,
                "name": customer.name,
                "email": customer.email,
                "cars": customer_cars,
            }
            result.append(customer_data)

    return {"customers": result}, 200


@customer_bp.get("/customers/<id>", responses={"200": CustomerResponseSchema})
def get_customer_by_id(path: IdPathSchema):
    """Get customer by the ID from the database"""
    session = Session()
    customer_id = path.id

    customer = session.query(Customer).filter(Customer.id == customer_id).first()
    if customer:
        customer_data = {
            "id": customer.id,
            "name": customer.name,
            "email": customer.email,
            "cars": customer.get_cars(),
        }
        return {"customers": customer_data}, 200

    return {"message": f"Customer of ID {customer_id} not found."}, 404


@customer_bp.post("/customers", responses={"200": MessageSchema})
def add_customer(body: CustomerBodySchema):
    """Add a new customer to the database"""
    session = Session()

    customer = Customer(name=body.name, email=body.email)

    try:
        session.add(customer)
        session.commit()
    except Exception as err:
        print(err)
        return {"error": "Customer not added"}, 500
    return {"message": f"Customer added with ID {customer.id}."}, 200


@customer_bp.delete("/customers/<id>", responses={"200": MessageSchema})
def remove_customer_by_id(path: IdPathSchema):
    """Remove customer by the ID from the database"""
    session = Session()
    customer_id = path.id
    customer_query = session.query(Customer).filter(Customer.id == customer_id)
    customer = customer_query.first()

    if not customer:
        return {"message": f"Customer of ID {customer_id} not found."}, 404

    has_cars = customer.get_cars()
    if has_cars:
        cars_id = [car["id"] for car in has_cars]
        session.query(Car).filter(Car.id.in_(cars_id)).delete()

    customer_query.delete()
    session.commit()

    return {"message": "Customer deleted"}, 200
