"""Memory-based loan repository"""
from models.loan import Loan


class LoanRepository:
    """Memory-based loan repository"""
    def __init__(self):
        self.loans = {}
        self.next_id = 1

    def create(self, loan: Loan):
        """Create a new loan

        Autoincrement ID will be assigned to the loan object.

        @:param user: Loan object to create
        """
        next_id = self.next_id
        self.next_id += 1
        loan.loan_id = next_id
        self.loans[next_id] = loan

    def read(self, loan_id: int):
        """Read loan from the repository.
        @:param loan_id: ID of loan to read
        @:returns: Loan object
        """
        return self.loans.get(loan_id)
