from pydantic import BaseModel
from typing import Optional, List


class CustomerBodySchema(BaseModel):
    """Schema representation for the request body for Customer"""

    name: str
    email: Optional[str] = None


class CustomerQuerySchema(BaseModel):
    """Schema representation for the query param for Customer potential buyers"""

    buyers: Optional[str] = None


class CustomerCars(BaseModel):
    """Schema representation for the data in Customer cars field"""

    id: int
    model: str
    color: str
    owner_id: int


class CustomerSchema(BaseModel):
    """Schema representation for the Customer data"""

    id: int
    name: str
    email: str
    cars: List[CustomerCars]


class CustomerResponseSchema(BaseModel):
    """Schema representation for the Customer response"""

    customers: List[CustomerSchema]
