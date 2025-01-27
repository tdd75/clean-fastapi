import builtins
from unittest.mock import patch, mock_open, MagicMock

import pytest

from app.infrastructure.smtp.send_mail import Mail, send_mail


@pytest.fixture
def fake_mail():
    return Mail(
        receivers=['test@example.com'],
        subject='Test Subject',
        text_content='This is a test',
        html_content='<p>This is a test</p>',
        attachment_paths=['/fake/path/to/file.txt'],
    )


class TestSendMail:
    @patch('app.infrastructure.smtp.send_mail.setting')
    @patch('app.infrastructure.smtp.send_mail.smtplib.SMTP')
    def test_send_mail_success(self, mock_smtp, mock_setting, fake_mail):
        # Arrange
        mock_server = MagicMock()
        mock_smtp.return_value = mock_server
        mock_setting.SMTP_USER = 'noreply@example.com'
        mock_setting.SMTP_PASSWORD = 'secret'
        mock_setting.SMTP_HOST = 'smtp.example.com'
        mock_setting.SMTP_PORT = 587
        mock_setting.SMTP_TLS = True
        m = mock_open(read_data=b'file content')

        # Act
        with patch.object(builtins, 'open', m):
            send_mail([fake_mail])

        # Assert
        mock_smtp.assert_called_once_with('smtp.example.com', 587)
        mock_server.starttls.assert_called_once()
        mock_server.login.assert_called_once_with('noreply@example.com', 'secret')
        mock_server.sendmail.assert_called_once()
        mock_server.quit.assert_called_once()

    @patch('app.infrastructure.smtp.send_mail.setting')
    @patch('app.infrastructure.smtp.send_mail.smtplib.SMTP')
    def test_send_mail_smtp_not_configured(self, mock_smtp, mock_setting, fake_mail, caplog):
        # Arrange
        mock_setting.SMTP_USER = ''
        mock_setting.SMTP_PASSWORD = ''
        caplog.set_level('INFO')

        # Act
        send_mail([fake_mail])

        # Assert
        assert 'SMTP is not configured' in caplog.text
        mock_smtp.assert_not_called()

    @patch('app.infrastructure.smtp.send_mail.setting')
    @patch('app.infrastructure.smtp.send_mail.smtplib.SMTP')
    def test_send_mail_without_attachments(self, mock_smtp, mock_setting):
        # Arrange
        mock_server = MagicMock()
        mock_smtp.return_value = mock_server
        mock_setting.SMTP_USER = 'noreply@example.com'
        mock_setting.SMTP_PASSWORD = 'secret'
        mock_setting.SMTP_HOST = 'smtp.example.com'
        mock_setting.SMTP_PORT = 587
        mock_setting.SMTP_TLS = False

        mail = Mail(
            receivers=['test@example.com'],
            subject='Test',
            text_content='Hello',
        )

        # Act
        send_mail([mail])

        # Assert
        mock_server.sendmail.assert_called_once()
        mock_server.quit.assert_called_once()

    @patch('app.infrastructure.smtp.send_mail.setting')
    @patch('app.infrastructure.smtp.send_mail.smtplib.SMTP')
    def test_send_mail_without_text_content(self, mock_smtp, mock_setting):
        # Arrange
        mock_server = MagicMock()
        mock_smtp.return_value = mock_server
        mock_setting.SMTP_USER = 'noreply@example.com'
        mock_setting.SMTP_PASSWORD = 'secret'
        mock_setting.SMTP_HOST = 'smtp.example.com'
        mock_setting.SMTP_PORT = 587
        mock_setting.SMTP_TLS = False

        mail = Mail(
            receivers=['test@example.com'],
            subject='No Text Content',
            html_content='<p>Only HTML</p>',
        )

        # Act
        send_mail([mail])

        # Assert
        args, kwargs = mock_server.sendmail.call_args
        message_str = args[2]
        assert 'Only HTML' in message_str
        assert 'No Text Content' in message_str
        assert 'This is a test' not in message_str
        mock_server.quit.assert_called_once()
