from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from flask_cors import CORS
from pydantic import BaseModel
from typing import Optional

from blueprints import customer_bp, car_bp
from tests import seed_database


class QuerySeedDB(BaseModel):
    seed: Optional[str] = None


# Set info for documentation
info = Info(
    title="AdviceHealth_teste_tecnico",
    version="1.0.0",
    description="Teste técnico para AdviceHealth realizado por Lucas Rodrigues de Castro",
    contact={"name": "Lucas Rodrigues de Castro", "email": "lucas.movimento@gmail.com"},
)

# set tag for routes documentation
home_tag = Tag(
    name="Home",
    description="Initial routes",
)

app = OpenAPI(__name__, info=info)
CORS(app)


@app.get("/docs", tags=[home_tag])
def get_documentation():
    """Redirect to documentaion provide by flask-openapi"""
    return redirect("/openapi")


@app.get("/", tags=[home_tag])
def login():
    """TODO Login"""
    return {"message": "HOME"}


@app.get("/seed", tags=[home_tag])
def seed_db():
    """Seed database for development"""
    seed_database()
    return {"message": "DB seeded"}


# Register Blueprints
app.register_api(customer_bp)
app.register_api(car_bp)
