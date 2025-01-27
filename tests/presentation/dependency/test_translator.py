import gettext
from unittest.mock import patch, MagicMock

from app.presentation.dependency.translator import Translator


class TestTranslator:
    """Test cases for the Translator class."""

    def test_init_with_valid_language(self):
        """Test Translator initialization with a valid language."""
        translator = Translator('en')
        assert translator.accept_language == 'en'
        assert hasattr(translator, 'translation')

    def test_init_with_vietnamese_language(self):
        """Test Translator initialization with Vietnamese language."""
        translator = Translator('vi')
        assert translator.accept_language == 'vi'
        assert hasattr(translator, 'translation')

    def test_init_with_invalid_language(self):
        """Test Translator initialization with an invalid language."""
        translator = Translator('invalid-lang')
        assert translator.accept_language == 'invalid-lang'
        assert hasattr(translator, 'translation')

    @patch('gettext.translation')
    def test_set_lang_success(self, mock_translation):
        """Test successful language setting."""
        mock_trans = MagicMock()
        mock_translation.return_value = mock_trans

        translator = Translator('en')
        translator.set_lang('vi')

        mock_translation.assert_called_with(
            'messages',
            localedir='app/infrastructure/locale',
            languages=['vi'],
            fallback=True,
        )
        assert translator.translation == mock_trans

    @patch('gettext.translation')
    @patch('app.presentation.dependency.translator.logger')
    def test_set_lang_with_exception(self, mock_logger, mock_translation):
        """Test language setting when an exception occurs."""
        # First call succeeds (during __init__), second call fails
        mock_translation.side_effect = [MagicMock(), Exception('Translation error')]

        translator = Translator('en')
        translator.set_lang('invalid')

        # Should handle the exception gracefully
        mock_logger.warning.assert_called_with("Translation error for language 'invalid': Translation error")

    def test_translate_message(self):
        """Test message translation."""
        translator = Translator('en')

        # Mock the translation object
        mock_translation = MagicMock()
        mock_translation.gettext.return_value = 'Translated message'
        translator.translation = mock_translation

        result = translator.translate('original message')

        assert result == 'Translated message'
        mock_translation.gettext.assert_called_once_with('original message')

    def test_translate_with_empty_message(self):
        """Test translation with empty message."""
        translator = Translator('en')

        mock_translation = MagicMock()
        mock_translation.gettext.return_value = ''
        translator.translation = mock_translation

        result = translator.translate('')

        assert result == ''
        mock_translation.gettext.assert_called_once_with('')

    @patch('gettext.translation')
    def test_translate_with_fallback(self, mock_translation):
        """Test translation with fallback behavior."""
        # Create a real fallback translation that just returns the original message
        fallback_translation = gettext.NullTranslations()
        mock_translation.return_value = fallback_translation

        translator = Translator('nonexistent-lang')

        # With fallback, should return the original message
        result = translator.translate('Hello World')
        assert result == 'Hello World'


class TestTranslatorDependency:
    """Test cases for the Translator dependency class with Header support."""

    def test_translator_dependency_class_signature(self):
        """Test that Translator class exists and has correct signature."""
        import inspect
        from app.presentation.dependency.translator import Translator

        # Check class exists
        assert inspect.isclass(Translator)

        # Check constructor signature
        sig = inspect.signature(Translator.__init__)
        assert 'accept_language' in sig.parameters

        # Check parameter default and annotation
        param = sig.parameters['accept_language']
        assert param.annotation is str

    def test_translator_with_default_parameter(self):
        """Test Translator when called with default language."""
        # In testing context, we need to provide a language since Header dependency won't work
        # but we can test the default behavior by checking the parameter structure
        import inspect
        from app import setting

        sig = inspect.signature(Translator.__init__)
        param = sig.parameters['accept_language']

        # Test that default value exists (will be the Header object in production)
        assert param.default is not param.empty

        # Test creating translator with setting default
        translator = Translator(accept_language=setting.DEFAULT_LOCALE)
        assert isinstance(translator, Translator)
        assert hasattr(translator, 'accept_language')
        assert hasattr(translator, 'translation')

    def test_translator_with_custom_language(self):
        """Test Translator with custom Accept-Language header."""
        translator = Translator(accept_language='vi')
        assert isinstance(translator, Translator)
        assert translator.accept_language == 'vi'

    def test_translator_with_multiple_languages(self):
        """Test Translator with multiple languages in Accept-Language header."""
        # Simulate browser Accept-Language header with multiple languages
        accept_lang = 'vi-VN,vi;q=0.9,en;q=0.8'
        translator = Translator(accept_language=accept_lang)
        assert isinstance(translator, Translator)
        assert translator.accept_language == accept_lang

    def test_translator_with_empty_language(self):
        """Test Translator with empty Accept-Language header."""
        translator = Translator(accept_language='')
        assert isinstance(translator, Translator)
        assert translator.accept_language == ''


class TestTranslatorIntegration:
    """Integration tests for the Translator class."""

    def test_real_translation_fallback(self):
        """Test actual translation with fallback to English."""
        translator = Translator('nonexistent-language')

        # Should use fallback (identity translation)
        test_message = 'Test message'
        result = translator.translate(test_message)
        assert result == test_message

    def test_language_switching(self):
        """Test switching between languages."""
        translator = Translator('en')

        # Switch to Vietnamese
        translator.set_lang('vi')
        assert hasattr(translator, 'translation')

        # Switch back to English
        translator.set_lang('en')
        assert hasattr(translator, 'translation')

    @patch('app.presentation.dependency.translator.logger')
    def test_logging_on_translation_error(self, mock_logger):
        """Test that errors are properly logged."""
        with patch('gettext.translation') as mock_translation:
            mock_translation.side_effect = FileNotFoundError('No translation file')

            Translator('invalid-lang')

            # Should log the warning
            mock_logger.warning.assert_called_once()
            call_args = mock_logger.warning.call_args[0][0]
            assert 'Translation error' in call_args
            assert 'invalid-lang' in call_args


class TestTranslatorEdgeCases:
    """Test edge cases and error conditions."""

    def test_special_characters_in_language(self):
        """Test with special characters in language code."""
        translator = Translator('zh-Hans-CN')
        assert translator.accept_language == 'zh-Hans-CN'

    def test_very_long_language_string(self):
        """Test with very long language string."""
        long_lang = 'a' * 1000
        translator = Translator(long_lang)
        assert translator.accept_language == long_lang

    def test_translate_special_characters(self):
        """Test translation with special characters."""
        translator = Translator('en')

        mock_translation = MagicMock()
        mock_translation.gettext.return_value = 'Café & 日本語'
        translator.translation = mock_translation

        result = translator.translate('Cafe & Japanese')
        assert result == 'Café & 日本語'

    def test_translate_very_long_message(self):
        """Test translation with very long message."""
        translator = Translator('en')

        long_message = 'This is a very long message. ' * 100
        mock_translation = MagicMock()
        mock_translation.gettext.return_value = long_message
        translator.translation = mock_translation

        result = translator.translate(long_message)
        assert result == long_message
