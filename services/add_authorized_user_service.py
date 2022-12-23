"""Service for adding an authorized user to a loan"""
from models import AuthorizedUser
from request_exception import RequestException


class AddAuthorizedUserService:
    """Service for adding an authorized user to a loan"""
    @staticmethod
    def add_authorized_user(
            authorized_user_repository,
            user_repository,
            loan_repository,
            authorized_user_id: int,
            loan_id: int):
        loan = loan_repository.read(loan_id)
        if loan is None:
            raise RequestException("loan {} does not exist".format(loan_id))

        if not user_repository.exists(authorized_user_id):
            raise RequestException("user {} does not exist".format(authorized_user_id))

        authorized_user = AuthorizedUser(authorized_user_id=0, loan_id=loan_id, user_id=authorized_user_id)
        authorized_user_repository.create(authorized_user)