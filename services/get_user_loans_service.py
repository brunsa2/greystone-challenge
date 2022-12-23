"""Service for getting all loans from a user"""
from request_exception import RequestException


class GetUserLoansService:
    """Service for getting all loans from a user"""
    @staticmethod
    def get_user_loans(loan_repository, user_repository, authorized_user_repository, user_id: int):
        """Get all loans from a user
        @:param loan_repository: Repository to read loans from
        @:param user_repository: Repository to read users from
        @:param authorized_user_repository: Repository to read authorized users from
        @:param user_id: User ID to get loans from
        @:returns: list of loans belonging to user
        @:raises: RequestException if request is invalid
        """
        if not user_repository.exists(user_id):
            raise RequestException("missing user {}".format(user_id))
        loans = loan_repository.read_loans_for_user_id(user_id)

        authorized_loan_ids = authorized_user_repository.read_loan_ids_by_user_id(user_id)
        for authorized_loan_id in authorized_loan_ids:
            loans.append(loan_repository.read(authorized_loan_id))

        for loan in loans:
            loan.authorized_user_ids = authorized_user_repository.read_authorized_user_ids(loan.loan_id)

        return loans
