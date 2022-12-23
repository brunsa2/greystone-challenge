"""Service for getting all loans from a user"""
from request_exception import RequestException


class GetUserLoansService:
    """Service for getting all loans from a user"""
    @staticmethod
    def get_user_loans(loan_repository, user_repository, user_id: int):
        """Get all loans from a user
        @:param loan_repository: Repository to read loans from
        @:param user_id: User ID to get loans from
        @:returns: list of loans belonging to user
        @:raises: RequestException if request is invalid
        """
        if not user_repository.exists(user_id):
            raise RequestException("missing user {}".format(user_id))
        return loan_repository.read_loans_for_user_id(user_id)
