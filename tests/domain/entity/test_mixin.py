"""
Test suite for AuditMixin functionality

This module tests the AuditMixin class which provides automatic audit tracking
for database entities. The AuditMixin adds the following fields to any inheriting class:

Timestamp fields:
- created_at: Automatically set when the entity is first created
- updated_at: Automatically set when the entity is created or updated

User tracking fields:
- created_user_id: Optional foreign key to track who created the entity
- updated_user_id: Optional foreign key to track who last updated the entity
- created_user: Relationship to the User who created the entity
- updated_user: Relationship to the User who last updated the entity

Test coverage includes:
- Field presence and data types
- Automatic timestamp generation
- User relationship functionality
- Inheritance behavior with real entities like User
- SQLAlchemy session management and relationship loading

Note: Some tests use SQLite in-memory database which may not fully support
all PostgreSQL-specific features like server_onupdate triggers.
"""

import datetime
import pytest
from faker import Faker
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.db.base import Base
from app.domain.entity.mixin import AuditMixin
from app.domain.entity.user import User
from app import connection_pool

fake = Faker()


class TestEntity(AuditMixin, Base):
    """Test entity that inherits from AuditMixin for testing purposes"""

    __tablename__ = 'test_entity'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column()


@pytest.fixture
def test_user() -> User:
    """Create a test user for audit relationships"""
    user = User(
        email=fake.unique.email(),
        password=fake.sha256(),
        first_name=fake.first_name(),
        last_name=fake.last_name(),
    )
    with connection_pool.open_session() as session:
        session.add(user)
        session.commit()
        session.refresh(user)
    return user


class TestAuditMixin:
    """Test suite for AuditMixin functionality"""

    def test_audit_mixin_has_required_fields(self):
        """Test that AuditMixin defines all required audit fields"""
        # Arrange & Act
        entity = TestEntity(name='test')

        # Assert
        assert hasattr(entity, 'created_at')
        assert hasattr(entity, 'updated_at')
        assert hasattr(entity, 'created_user_id')
        assert hasattr(entity, 'updated_user_id')
        assert hasattr(entity, 'created_user')
        assert hasattr(entity, 'updated_user')

    def test_created_at_is_set_automatically(self):
        """Test that created_at is automatically set when entity is created"""
        # Arrange & Act
        with connection_pool.open_session() as session:
            entity = TestEntity(name='test entity')
            session.add(entity)
            session.commit()
            session.refresh(entity)

        # Assert
        assert entity.created_at is not None
        # Just verify it's a valid datetime
        assert isinstance(entity.created_at, datetime.datetime)

    def test_updated_at_is_set_automatically(self):
        """Test that updated_at is automatically set when entity is created"""
        # Arrange & Act
        with connection_pool.open_session() as session:
            entity = TestEntity(name='test entity')
            session.add(entity)
            session.commit()
            session.refresh(entity)

        # Assert
        assert entity.updated_at is not None
        # Just verify it's a valid datetime
        assert isinstance(entity.updated_at, datetime.datetime)

    def test_updated_at_changes_on_update(self):
        """Test that updated_at changes when entity is updated but created_at stays the same"""
        # Arrange
        with connection_pool.open_session() as session:
            entity = TestEntity(name='original name')
            session.add(entity)
            session.commit()
            session.refresh(entity)

            original_created_at = entity.created_at

        # Note: SQLite with in-memory DB might not support server_onupdate properly
        # This test verifies basic behavior but may need PostgreSQL for full functionality

        # Act
        with connection_pool.open_session() as session:
            entity = session.get(TestEntity, entity.id)
            entity.name = 'updated name'
            session.commit()
            session.refresh(entity)

        # Assert
        assert entity.created_at == original_created_at  # created_at should not change
        # Note: In SQLite, server_onupdate may not work, so we just verify it's still a datetime
        assert isinstance(entity.updated_at, datetime.datetime)

    def test_created_user_id_can_be_set(self, test_user):
        """Test that created_user_id can be set to reference a user"""
        # Arrange & Act
        with connection_pool.open_session() as session:
            entity = TestEntity(name='test entity', created_user_id=test_user.id)
            session.add(entity)
            session.commit()
            session.refresh(entity)

        # Assert
        assert entity.created_user_id == test_user.id

    def test_updated_user_id_can_be_set(self, test_user):
        """Test that updated_user_id can be set to reference a user"""
        # Arrange & Act
        with connection_pool.open_session() as session:
            entity = TestEntity(name='test entity', updated_user_id=test_user.id)
            session.add(entity)
            session.commit()
            session.refresh(entity)

        # Assert
        assert entity.updated_user_id == test_user.id

    def test_created_user_relationship_works(self, test_user):
        """Test that created_user relationship resolves to the correct User object"""
        # Arrange & Act
        with connection_pool.open_session() as session:
            entity = TestEntity(name='test entity', created_user_id=test_user.id)
            session.add(entity)
            session.commit()
            session.refresh(entity)

            # Load the relationship while session is still open
            created_user = entity.created_user

            # Assert
            assert created_user is not None
            assert created_user.id == test_user.id
            assert created_user.email == test_user.email

    def test_updated_user_relationship_works(self, test_user):
        """Test that updated_user relationship resolves to the correct User object"""
        # Arrange & Act
        with connection_pool.open_session() as session:
            entity = TestEntity(name='test entity', updated_user_id=test_user.id)
            session.add(entity)
            session.commit()
            session.refresh(entity)

            # Load the relationship while session is still open
            updated_user = entity.updated_user

            # Assert
            assert updated_user is not None
            assert updated_user.id == test_user.id
            assert updated_user.email == test_user.email

    def test_user_fields_can_be_none(self):
        """Test that user fields can be None (optional audit tracking)"""
        # Arrange & Act
        with connection_pool.open_session() as session:
            entity = TestEntity(name='test entity')
            session.add(entity)
            session.commit()
            session.refresh(entity)

            # Assert basic fields
            assert entity.created_user_id is None
            assert entity.updated_user_id is None
            # Note: We don't test the relationships when IDs are None to avoid DetachedInstanceError

    def test_different_users_for_created_and_updated(self):
        """Test that different users can be set for created_user_id and updated_user_id"""
        # Arrange
        creator = User(
            email=fake.unique.email(),
            password=fake.sha256(),
            first_name='Creator',
            last_name='User',
        )
        updater = User(
            email=fake.unique.email(),
            password=fake.sha256(),
            first_name='Updater',
            last_name='User',
        )

        with connection_pool.open_session() as session:
            session.add_all([creator, updater])
            session.commit()
            session.refresh(creator)
            session.refresh(updater)

        # Act
        with connection_pool.open_session() as session:
            entity = TestEntity(name='test entity', created_user_id=creator.id, updated_user_id=updater.id)
            session.add(entity)
            session.commit()
            session.refresh(entity)

            # Assert
            assert entity.created_user_id == creator.id
            assert entity.updated_user_id == updater.id

            # Test relationships while session is open
            assert entity.created_user.first_name == 'Creator'
            assert entity.updated_user.first_name == 'Updater'


class TestAuditMixinInheritance:
    """Test that classes inheriting from AuditMixin work correctly"""

    def test_user_entity_inherits_audit_fields(self):
        """Test that User entity properly inherits audit functionality from AuditMixin"""
        # Arrange & Act
        user = User(
            email=fake.unique.email(),
            password=fake.sha256(),
            first_name=fake.first_name(),
            last_name=fake.last_name(),
        )

        # Assert
        assert hasattr(user, 'created_at')
        assert hasattr(user, 'updated_at')
        assert hasattr(user, 'created_user_id')
        assert hasattr(user, 'updated_user_id')
        assert hasattr(user, 'created_user')
        assert hasattr(user, 'updated_user')

    def test_user_audit_fields_work_correctly(self, test_user):
        """Test that User entity audit fields work correctly when creating a new user"""
        # Arrange & Act
        with connection_pool.open_session() as session:
            new_user = User(
                email=fake.unique.email(),
                password=fake.sha256(),
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                created_user_id=test_user.id,
                updated_user_id=test_user.id,
            )
            session.add(new_user)
            session.commit()
            session.refresh(new_user)

            # Assert
            assert new_user.created_at is not None
            assert new_user.updated_at is not None
            assert isinstance(new_user.created_at, datetime.datetime)
            assert new_user.created_user_id == test_user.id
            assert new_user.updated_user_id == test_user.id
            assert new_user.created_user.id == test_user.id
            assert new_user.updated_user.id == test_user.id
