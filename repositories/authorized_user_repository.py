"""Memory-based authorized user repository"""
from models import AuthorizedUser


class AuthorizedUserRepository:
    """Memory-based authorized user repository"""
    def __init__(self):
        self.authorized_users = {}
        self.authorized_users_by_loan_id = {}
        self.authorized_users_by_user_id = {}
        self.next_id = 1

    def create(self, authorized_user: AuthorizedUser):
        """Create a new authorized

        Autoincrement ID will be assigned to the authorized user object.

        @:param authorized_user: Authorized user object to create
        """
        next_id = self.next_id
        self.next_id += 1
        authorized_user.authorized_user_id = next_id
        self.authorized_users[next_id] = authorized_user
        self.authorized_users_by_loan_id.setdefault(authorized_user.loan_id, []).append(authorized_user)
        self.authorized_users_by_user_id.setdefault(authorized_user.user_id, []).append(authorized_user)

    def read(self, authorized_user_id: int):
        """Read authorized user from the repository.
        @:param authorized_user_id: ID of authorized user to read
        @:returns: Authorized user object
        """
        return self.authorized_users.get(authorized_user_id)

    def read_authorized_user_ids(self, loan_id: int):
        """Read authorized user IDs from the repository for a given loan.
        @:param loan: ID of loan to read authorized user IDs from
        @:returns: Array of authorized user IDs
        """
        return [authorized_user.user_id
                for authorized_user in self.authorized_users_by_loan_id.setdefault(loan_id, [])]

    def read_loan_ids_by_user_id(self, user_id: int):
        """Read loan IDs from the repository for a authorized user ID.
        @:param loan: ID of user to read authorized user IDs from
        @:returns: Array of loan IDs
        """
        return [authorized_user.loan_id for authorized_user in self.authorized_users_by_user_id.setdefault(user_id, [])]
