"""Authorized user model"""
from pydantic import BaseModel


class AuthorizedUser(BaseModel):
    """Authorized user model"""
    authorized_user_id: int
    loan_id: int
    user_id: int
