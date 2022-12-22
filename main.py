"""API handler for loan service"""

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel
from repositories.user_repository import UserRepository
from repositories.loan_repository import LoanRepository
from request_exception import RequestException
from services import CreateUserService, CreateLoanService
from decimal import Decimal, InvalidOperation

app = FastAPI()

user_repository = UserRepository()
loan_repository = LoanRepository()


class UserRequest(BaseModel):
    """Incoming user request object"""
    username: str


class LoanRequest(BaseModel):
    """Incoming loan request object"""
    amount: str
    term_months: int
    interest_rate: str


@app.post("/users")
async def create_user(user: UserRequest):
    """Handles creating new user

    @:param user: User creation request
    @:returns: JSON response with new user ID
    """
    user_id = CreateUserService.create_user(user_repository, user.username)
    return {
        "user_id": user_id
    }


@app.get("/user/{user_id}/loans")
async def get_user_loans(user_id: int):
    """Handles getting all loans belonging to user"""
    return {
        "amount": "0.00",
        "term_months": 0,
        "interest_rate": "0.0",
        "authorized_users": []
    }


@app.post("/user/{user_id}/loans")
async def create_loan(user_id: int, loan: LoanRequest):
    """Handles creating new loan for given user

    @:param user_id: User ID to create loan for
    @:param loan: Loan parameters to issue loan with
    @:returns: JSON response with new loan ID
    """
    try:
        amount = Decimal(loan.amount)
    except InvalidOperation as e:
        raise RequestException("Invalid amount")

    try:
        interest_rate = Decimal(loan.interest_rate)
    except InvalidOperation as e:
        raise RequestException("Invalid interest rate")

    loan_id = CreateLoanService.create_loan(
        loan_repository,
        user_repository,
        user_id=user_id,
        amount=amount,
        term_months=loan.term_months,
        interest_rate=interest_rate)
    return {
        "loan_id": loan_id
    }


@app.get("/user/{user_id}/loan/{loan_id}/schedule")
async def get_loan_schedule(user_id: int, loan_id: int):
    """Handles getting loan schedule for given loan"""
    return [
        {
            "month_number": 0,
            "balance": "0.00",
            "payment": "0.00"
        }
    ]


@app.get("/user/{user_id}/loan/{loan_id}/month/{month_id}")
async def get_loan_month(user_id: int, loan_id: int, month_id: int):
    """Handles getting loan balance and payment information for given month"""
    return {
        "principal_balance": "0.00",
        "principal_paid": "0.00",
        "interest_paid": "0.00"
    }


@app.post("/user/{user_id}/loan/{loan_id}/authorized_users")
async def add_loan_authorized_user(user_id: int, loan_id: int):
    """Handles adding authorized (shared) user to a given loan"""
    return {}


@app.exception_handler(RequestException)
async def request_exception_handler(request: Request, e: RequestException):
    """Handles request exceptions

    @:param request: Request
    @:param e: Exception thrown
    @:returns: Error response
    """
    return PlainTextResponse("Invalid request: {}".format(e), status_code=422)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, e: RequestValidationError):
    """Handles validation exceptions

    @:param request: Request
    @:param e: Exception thrown
    @:returns: Error response
    """
    return PlainTextResponse("Invalid request: {}".format(e), status_code=400)
