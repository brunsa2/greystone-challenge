"""API handler for loan service"""

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel
from repositories import AuthorizedUserRepository, LoanRepository, UserRepository
from request_exception import RequestException
from services import AddAuthorizedUserService,\
    CreateAmortizationScheduleService,\
    CreateUserService,\
    CreateLoanService,\
    GetUserLoansService
from decimal import Decimal, InvalidOperation

app = FastAPI()

user_repository = UserRepository()
loan_repository = LoanRepository()
authorized_user_repository = AuthorizedUserRepository()


class UserRequest(BaseModel):
    """Incoming user request object"""
    username: str


class LoanRequest(BaseModel):
    """Incoming loan request object"""
    amount: str
    term_months: int
    interest_rate: str


class AuthorizedUserRequest(BaseModel):
    """Authorized user request object"""
    user_id: int


@app.post('/users')
async def create_user(user: UserRequest):
    """Handles creating new user

    @:param user: User creation request
    @:returns: JSON response with new user ID
    """
    user_id = CreateUserService.create_user(user_repository, user.username)
    return {
        'user_id': user_id
    }


@app.get('/user/{user_id}/loans')
async def get_user_loans(user_id: int):
    """Handles getting all loans belonging to user"""
    loans = GetUserLoansService.get_user_loans(
        loan_repository,
        user_repository,
        authorized_user_repository,
        user_id)
    return [{
        'amount': str(loan.amount),
        'term_months': loan.term_months,
        'interest_rate': str(loan.interest_rate),
        'authorized_users': loan.authorized_user_ids
    } for loan in loans]


@app.post('/user/{user_id}/loans')
async def create_loan(user_id: int, loan: LoanRequest):
    """Handles creating new loan for given user

    @:param user_id: User ID to create loan for
    @:param loan: Loan parameters to issue loan with
    @:returns: JSON response with new loan ID
    """
    try:
        amount = Decimal(loan.amount)
    except InvalidOperation as e:
        raise RequestException('Invalid amount')

    try:
        interest_rate = Decimal(loan.interest_rate)
    except InvalidOperation as e:
        raise RequestException('Invalid interest rate')

    loan_id = CreateLoanService.create_loan(
        loan_repository,
        user_repository,
        user_id=user_id,
        amount=amount,
        term_months=loan.term_months,
        interest_rate=interest_rate)
    return {
        'loan_id': loan_id
    }


@app.get('/user/{user_id}/loan/{loan_id}/schedule')
async def get_loan_schedule(user_id: int, loan_id: int):
    """Handles getting loan schedule for given loan

    @:param user_id: User ID of loan (currently not checked; only for URL)
    @:param loan_id: Loan ID of loan
    @:returns: JSON array of monthly balance schedules
    """
    loan = loan_repository.read(loan_id)
    if loan is None:
        raise RequestException('missing loan {}'.format(loan_id))

    schedule = CreateAmortizationScheduleService.generate_amortization_schedule(
        amount=loan.amount,
        term_months=loan.term_months,
        interest_rate=loan.interest_rate)

    return [
        {
            'month': month,
            'remaining_balance': str(month_balances['balance']),
            'monthly_payment': str(month_balances['payment'])
        }
        for month, month_balances in enumerate(schedule)
    ]


@app.get('/user/{user_id}/loan/{loan_id}/month/{month}')
async def get_loan_month(user_id: int, loan_id: int, month: int):
    """Handles getting loan balance and payment information for given month

    @:param user_id: User ID of loan (currently not checked; only for URL)
    @:param loan_id: Loan ID of loan
    @:param month: Month number to retrieve balances for (0 is beginning of loan)
    @:returns: JSON summary of loan balances at given month
    """
    loan = loan_repository.read(loan_id)
    if loan is None:
        raise RequestException('missing loan {}'.format(loan_id))

    if month < 0 or month > loan.term_months:
        raise RequestException('invalid month {}'.format(month))

    schedule = CreateAmortizationScheduleService.generate_amortization_schedule(
        amount=loan.amount,
        term_months=loan.term_months,
        interest_rate=loan.interest_rate)

    return {
        'principal_balance': str(schedule[month]['balance']),
        'principal_paid': str(schedule[month]['total_principal_paid']),
        'interest_paid': str(schedule[month]['total_interest_paid'])
    }


@app.post('/user/{user_id}/loan/{loan_id}/authorized_users')
async def add_loan_authorized_user(user_id: int, loan_id: int, authorized_user: AuthorizedUserRequest):
    """Handles adding authorized (shared) user to a given loan

    @:param user_id: User ID of loan (currently not checked; only for URL)
    @:param loan_id: Loan ID to add authorized user to
    @:param authorized_user: Authorized user request to add
    """
    AddAuthorizedUserService.add_authorized_user(
        authorized_user_repository,
        user_repository,
        loan_repository,
        authorized_user_id=authorized_user.user_id,
        loan_id=loan_id)
    return {}


@app.exception_handler(RequestException)
async def request_exception_handler(request: Request, e: RequestException):
    """Handles request exceptions

    @:param request: Request
    @:param e: Exception thrown
    @:returns: Error response
    """
    return PlainTextResponse('Invalid request: {}'.format(e), status_code=422)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, e: RequestValidationError):
    """Handles validation exceptions

    @:param request: Request
    @:param e: Exception thrown
    @:returns: Error response
    """
    return PlainTextResponse('Invalid request: {}'.format(e), status_code=400)
