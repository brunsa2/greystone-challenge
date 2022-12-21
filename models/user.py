"""User model"""
from pydantic import BaseModel


class User(BaseModel):
    """User model"""
    user_id: int
    username: str
