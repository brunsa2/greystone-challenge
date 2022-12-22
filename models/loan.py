"""Loan model"""
from pydantic import BaseModel
from decimal import Decimal


class Loan(BaseModel):
    """Loan model"""
    loan_id: int
    user_id: int
    amount: Decimal
    term_months: int
    interest_rate: Decimal
