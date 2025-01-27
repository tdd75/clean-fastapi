import logging

from sqlalchemy.orm import Session

from app import connection_pool
from app.infrastructure.helper.password_helper import hash_password
from app.domain.entity.user import User
from app.domain.repository import user_repository

logger = logging.getLogger(__name__)


def create_user_if_not_exist(session: Session, user: User) -> None:
    if not user_repository.find_by_email(session, user.email):
        user.password = hash_password(user.password)
        user_repository.create(session, user)
        logger.info(f'User {user.email} created')


def init_data() -> None:
    with connection_pool.open_session() as session:
        normal_user = User(
            email='user@example.com',
            password='password',
            first_name='John',
            last_name='Doe',
        )
        admin_user = User(
            email='admin@example.com',
            password='password',
            first_name='Admin',
            last_name='User',
        )
        create_user_if_not_exist(session, normal_user)
        create_user_if_not_exist(session, admin_user)


if __name__ == '__main__':
    init_data()
