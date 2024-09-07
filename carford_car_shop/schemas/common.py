from pydantic import BaseModel
from typing import Optional


class ErrorSchema(BaseModel):
    """Schema representation for the error response"""

    error: str


class MessageSchema(BaseModel):
    """Schema representation for the message response"""

    message: str


class IdPathSchema(BaseModel):
    """Schema representation for the request path ID"""

    id: str
