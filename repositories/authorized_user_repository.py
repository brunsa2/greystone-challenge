"""Memory-based authorized user repository"""
from models import AuthorizedUser


class AuthorizedUserRepository:
    """Memory-based authorized user repository"""
    def __init__(self):
        self.authorized_users = {}
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

    def read(self, authorized_user_id: int):
        """Read authorized user from the repository.
        @:param authorized_user_id: ID of authorized user to read
        @:returns: Authorized user object
        """
        return self.authorized_users.get(authorized_user_id)
