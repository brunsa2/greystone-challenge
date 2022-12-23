"""Service for creating a loan"""
from decimal import Decimal

from models import Loan
from request_exception import RequestException


MAX_LOAN_AMOUNT = Decimal(100000)
MAX_TERM_MONTHS = 120
MIN_INTEREST_RATE = Decimal('0.06')
MAX_INTEREST_RATE = Decimal('0.36')


class CreateLoanService:
    """Service for creating a loan"""
    @staticmethod
    def create_loan(
            loan_repository,
            user_repository,
            user_id: int,
            amount: Decimal,
            term_months: int,
            interest_rate: Decimal):
        """Create a user in the repository
        @:param user_repository: Repository to create user in
        @:param username: Username of new user
        @:returns: user ID of newly-created user
        @:raises: RequestException if request is invalid
        """
        if not user_repository.exists(user_id):
            raise RequestException("user #{} doesn't exist".format(user_id))

        if not (0 <= amount <= MAX_LOAN_AMOUNT):
            raise RequestException("Invalid amount {}".format(amount))
        if not (0 <= term_months <= MAX_TERM_MONTHS):
            raise RequestException("Invalid term months {}".format(term_months))
        if not (MIN_INTEREST_RATE <= interest_rate <= MAX_INTEREST_RATE):
            raise RequestException("Invalid interest rate {}".format(interest_rate))

        loan = Loan(
            loan_id=0,
            user_id=user_id,
            amount=amount,
            term_months=term_months,
            interest_rate=interest_rate,
            authorized_user_ids=[])
        loan_repository.create(loan)
        return loan.loan_id
