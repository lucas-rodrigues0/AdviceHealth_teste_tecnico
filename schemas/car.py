from pydantic import BaseModel
from typing import List


class CarBodySchema(BaseModel):
    """Schema representation for the request body for Car"""

    model: str
    color: str
    owner_id: int


class CarSchema(BaseModel):
    """Schema representation for the Car data"""

    id: int
    model: str
    color: str
    owner_id: int


class CarResponseSchema(BaseModel):
    """Schema representation for the Car response"""

    cars: List[CarSchema]
