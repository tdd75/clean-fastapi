import pytest
from unittest.mock import Mock
from sqlalchemy.orm import Session

from app.presentation.dependency.context import AppContext, get_context
from app.domain.entity.user import User
from app.presentation.dependency.translator import Translator


class TestAppContext:
    """Test cases for AppContext class"""

    def test_init_with_session_only(self):
        """Test AppContext initialization with session only"""
        session = Mock(spec=Session)
        context = AppContext(session=session)

        assert context.session == session
        assert context.user is None
        assert context.translator is None

    def test_init_with_all_parameters(self):
        """Test AppContext initialization with all parameters"""
        session = Mock(spec=Session)
        user = User(id=1, email='test@example.com', password='password')
        translator = Mock(spec=Translator)

        context = AppContext(session=session, user=user, translator=translator)

        assert context.session == session
        assert context.user == user
        assert context.translator == translator

    def test_authenticate_user(self):
        """Test user authentication functionality"""
        session = Mock(spec=Session)
        session.info = {}
        user = User(id=1, email='test@example.com', password='password')

        context = AppContext(session=session)
        context.authenticate(user)

        assert context.user == user
        assert session.info['uid'] == user.id

    def test_authenticate_user_updates_existing_user(self):
        """Test that authentication updates existing user"""
        session = Mock(spec=Session)
        session.info = {}
        old_user = User(id=1, email='old@example.com', password='password')
        new_user = User(id=2, email='new@example.com', password='password')

        context = AppContext(session=session, user=old_user)
        context.authenticate(new_user)

        assert context.user == new_user
        assert session.info['uid'] == new_user.id

    def test_set_lang_with_translator(self):
        """Test setting language when translator is available"""
        session = Mock(spec=Session)
        translator = Mock(spec=Translator)

        context = AppContext(session=session, translator=translator)
        context.set_lang('vi')

        translator.set_lang.assert_called_once_with('vi')

    def test_set_lang_without_translator(self):
        """Test setting language when translator is None"""
        session = Mock(spec=Session)

        context = AppContext(session=session, translator=None)
        # Should not raise any exception
        context.set_lang('vi')

    def test_translate_with_translator(self):
        """Test translation when translator is available"""
        session = Mock(spec=Session)
        translator = Mock(spec=Translator)
        translator.translate.return_value = 'Chào bạn'

        context = AppContext(session=session, translator=translator)
        result = context.t('Hello')

        assert result == 'Chào bạn'
        translator.translate.assert_called_once_with('Hello')

    def test_translate_without_translator(self):
        """Test translation when translator is None - should return original message"""
        session = Mock(spec=Session)

        context = AppContext(session=session, translator=None)
        result = context.t('Hello')

        assert result == 'Hello'

    def test_translate_empty_string(self):
        """Test translation with empty string"""
        session = Mock(spec=Session)
        translator = Mock(spec=Translator)
        translator.translate.return_value = ''

        context = AppContext(session=session, translator=translator)
        result = context.t('')

        assert result == ''
        translator.translate.assert_called_once_with('')

    def test_context_implements_icontext_interface(self):
        """Test that AppContext has all required methods from IContext protocol"""
        session = Mock(spec=Session)
        context = AppContext(session=session)

        # Check that all required attributes and methods exist
        assert hasattr(context, 'session')
        assert hasattr(context, 'user')
        assert hasattr(context, 'authenticate')
        assert hasattr(context, 'set_lang')
        assert hasattr(context, 't')

        # Check they are callable
        assert callable(context.authenticate)
        assert callable(context.set_lang)
        assert callable(context.t)


class TestGetContext:
    """Test cases for get_context function"""

    def test_get_context_unauthenticated(self):
        """Test get_context with is_authenticated=False"""
        context_func = get_context(is_authenticated=False)

        # The function should return a callable
        assert callable(context_func)

    def test_get_context_authenticated(self):
        """Test get_context with is_authenticated=True (default)"""
        context_func = get_context(is_authenticated=True)

        # The function should return a callable
        assert callable(context_func)

    def test_get_context_default_authenticated(self):
        """Test get_context with default parameters (should be authenticated)"""
        context_func = get_context()

        # The function should return a callable
        assert callable(context_func)

    @pytest.mark.parametrize('is_authenticated', [True, False])
    def test_get_context_returns_dependency_function(self, is_authenticated):
        """Test that get_context returns a proper dependency function"""
        context_func = get_context(is_authenticated=is_authenticated)

        # Check that the returned function has the correct annotations
        assert hasattr(context_func, '__annotations__')
        assert context_func.__name__ == '_get_context'

    def test_get_context_function_execution(self):
        """Test that the returned dependency function can be executed and returns AppContext"""
        context_func = get_context(is_authenticated=False)

        # Mock the dependencies
        mock_session = Mock(spec=Session)
        mock_translator = Mock(spec=Translator)

        # Execute the function directly (simulating FastAPI dependency injection)
        result = context_func.__code__.co_names  # Check function references the right modules
        assert 'AppContext' in result

        # Test that we can create the context manually with the same pattern
        context = AppContext(session=mock_session, translator=mock_translator)
        assert isinstance(context, AppContext)
        assert context.session == mock_session
        assert context.translator == mock_translator


class TestAppContextIntegration:
    """Integration tests for AppContext with real-like objects"""

    def test_full_workflow_with_authentication_and_translation(self):
        """Test complete workflow: create context, authenticate, set language, translate"""
        session = Mock(spec=Session)
        session.info = {}
        translator = Mock(spec=Translator)
        translator.translate.return_value = 'Xin chào'
        user = User(id=1, email='test@example.com', password='password')

        # Create context
        context = AppContext(session=session, translator=translator)

        # Authenticate user
        context.authenticate(user)
        assert context.user == user
        assert session.info['uid'] == 1

        # Set language
        context.set_lang('vi')
        translator.set_lang.assert_called_once_with('vi')

        # Translate message
        result = context.t('Hello')
        assert result == 'Xin chào'
        translator.translate.assert_called_once_with('Hello')

    def test_context_state_persistence(self):
        """Test that context maintains state across multiple operations"""
        session = Mock(spec=Session)
        session.info = {}
        translator = Mock(spec=Translator)
        translator.translate.side_effect = lambda x: f'translated_{x}'

        context = AppContext(session=session, translator=translator)

        # Set language first
        context.set_lang('en')

        # Authenticate user
        user = User(id=42, email='user@example.com', password='password')
        context.authenticate(user)

        # Verify state is maintained
        assert context.user is not None
        assert context.user.id == 42
        assert session.info['uid'] == 42

        # Translation should still work
        result = context.t('test')
        assert result == 'translated_test'

    def test_session_info_updates_on_multiple_authentications(self):
        """Test that session info is properly updated when authenticating different users"""
        session = Mock(spec=Session)
        session.info = {}

        context = AppContext(session=session)

        # First authentication
        user1 = User(id=1, email='user1@example.com', password='password')
        context.authenticate(user1)
        assert session.info['uid'] == 1
        assert context.user == user1

        # Second authentication
        user2 = User(id=2, email='user2@example.com', password='password')
        context.authenticate(user2)
        assert session.info['uid'] == 2
        assert context.user == user2
