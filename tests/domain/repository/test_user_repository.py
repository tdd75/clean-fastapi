import pytest
from faker import Faker

from app.domain.entity.user import User
from app import connection_pool
from app.domain.repository.user_repository import search

fake = Faker()


@pytest.fixture
def setup_users() -> list[User]:
    alice = User(
        email=fake.unique.email(),
        password=fake.sha256(),
        first_name=fake.unique.first_name(),
        last_name=fake.last_name(),
    )
    bobby = User(
        email=fake.unique.email(),
        password=fake.sha256(),
        first_name=fake.unique.first_name(),
        last_name=fake.last_name(),
    )
    charlie = User(
        email=fake.unique.email(),
        password=fake.sha256(),
        first_name=fake.unique.first_name(),
        last_name=fake.last_name(),
    )
    with connection_pool.open_session() as session:
        session.add_all([alice, bobby, charlie])
        session.commit()
    return [alice, bobby, charlie]


class TestSearchUser:
    def test_search_no_filter(self, setup_users):
        # Arrange

        # Act
        with connection_pool.open_session() as session:
            results, count = search(session)

        # Assert
        assert count == 3
        assert len(results) == 3

    def test_search_by_keyword(self, setup_users):
        # Arrange
        target_user = setup_users[0]
        keyword = target_user.first_name.lower()

        # Act
        with connection_pool.open_session() as session:
            results, count = search(session, keyword=keyword)

        # Assert
        assert count == 1
        assert results[0].id == target_user.id

    def test_search_by_email(self, setup_users):
        # Arrange
        target_user = setup_users[1]
        keyword = target_user.email.split('@')[0]

        # Act
        with connection_pool.open_session() as session:
            results, count = search(session, email=keyword)

        # Assert
        assert count == 1
        assert results[0].id == target_user.id

    def test_search_with_limit_offset(self, setup_users):
        # Arrange

        # Act
        with connection_pool.open_session() as session:
            results, count = search(session, limit=2, offset=1)

        # Assert
        assert len(results) == 2
        assert count == 2

    def test_search_eager_does_not_fail(self, setup_users):
        # Arrange

        # Act
        with connection_pool.open_session() as session:
            results, count = search(session, eager=True)

        # Assert
        assert count == 3
        assert all(isinstance(user, User) for user in results)
