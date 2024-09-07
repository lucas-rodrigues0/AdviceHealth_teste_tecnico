from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from flask_cors import CORS

from sqlalchemy.exc import IntegrityError

from blueprints import customer_bp, car_bp
from logger import logger
from models import User, Session
from schemas import *
from utils import jwt_encode
from tests import seed_database


# Set info for documentation
info = Info(
    title="AdviceHealth_teste_tecnico",
    version="1.0.0",
    description="Teste técnico para AdviceHealth realizado por Lucas Rodrigues de Castro",
    contact={"name": "Lucas Rodrigues de Castro", "email": "lucas.movimento@gmail.com"},
)

jwt_schema = {"type": "http", "scheme": "bearer", "bearerFormat": "JWT"}
security_schemes = {"jwt": jwt_schema}

# Instantiate app
app = OpenAPI(__name__, info=info, security_schemes=security_schemes)
CORS(app)

# Set tags for routes
doc_tag = Tag(
    name="Documentation",
    description="Route for Home, documentation (swagger, redoc and rapidoc), and to seed database for development",
)

login_tag = Tag(
    name="Login",
    description="Routes for login and user registration",
)


@app.get("/docs", tags=[doc_tag])
def get_documentation():
    """Redirect to documentation provide by flask-openapi"""
    return redirect("/openapi")


@app.get("/", tags=[doc_tag])
def login():
    """Home"""
    return {"CARFOLD Car Shop": "by Lucas Rodrigues", "Info": info.model_dump_json()}


@app.post(
    "/login/register",
    tags=[login_tag],
    responses={"200": LoginResponseSchema, "409": ErrorSchema, "400": ErrorSchema},
)
def register_user(body: RegisterBodySchema):
    """Register a new user in database. Returns an autentication token"""

    username = body.username
    email = body.email
    password = body.password

    if not username or not password:
        error_msg = "Username, email and password required."
        logger.warning(f"Error to register new user. {error_msg}")
        return {"error": error_msg}, 409

    user = User(username=username, email=email, password=password)
    logger.debug(f"Adding user: '{user.username}'")

    try:
        session = Session()
        session.add(user)
        session.commit()
        data = {"user_id": str(user.id), "username": user.username, "email": user.email}

        # Use the user data to generate a token JWT
        token = jwt_encode(data)

        return {"data": {"token": token, "user_id": str(user.id)}}, 200

    except IntegrityError as e:
        error_msg = "User email already exists."
        logger.warning(f"Error to add user with email '{user.email}', {error_msg}")
        return {"error": error_msg}, 409

    except Exception as e:
        error_msg = "User not register"
        logger.warning(f"Error to add user '{user.username}', {error_msg}")
        return {"error": error_msg}, 400


@app.post(
    "/login",
    tags=[login_tag],
    responses={"200": LoginResponseSchema, "403": ErrorSchema, "404": ErrorSchema},
)
def login_user(body: LoginBodySchema):
    """Authenticate user password and return a token"""

    email = body.email
    password = body.password

    session = Session()
    user = session.query(User).filter(User.email == email).first()

    if not user:
        return {"error": "User not found"}, 404
    elif password != user.password:
        return {"error": "Invalid password"}, 403
    else:
        # Encode token JWT with user data
        encode_data = {
            "user_id": str(user.id),
            "username": user.username,
            "email": user.email,
        }
        token = jwt_encode(encode_data)

        return {"data": {"token": token, "user_id": str(user.id)}}, 200


@app.get("/seed", tags=[doc_tag])
def seed_db():
    """Seed database for development"""
    seed_database()
    return {"message": "DB seeded"}


# Register Blueprints
app.register_api(customer_bp)
app.register_api(car_bp)
