from pydantic import BaseModel


class RegisterBodySchema(BaseModel):
    """Schema representation for the request for registration of User"""

    username: str
    email: str
    password: str


class LoginBodySchema(BaseModel):
    """Schema representation for the request for loging in User"""

    email: str
    password: str


class TokenSchema(BaseModel):
    """Schema represantation for an autentication token"""

    user_id: str
    token: str


class LoginResponseSchema(BaseModel):
    """Schema represantation for an autentication response"""

    data: TokenSchema
