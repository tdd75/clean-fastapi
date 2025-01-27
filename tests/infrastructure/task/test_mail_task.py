from unittest.mock import patch

from app.infrastructure.smtp.send_mail import Mail
from app.infrastructure.task.mail_task import send_mail_task


class TestMailTask:
    def test_send_mail_task_calls_send_mail(self):
        # Arrange
        fake_mail = [
            Mail(
                receivers=['test@example.com'],
                subject='Hello',
                html_content='<b>Hi</b>',
            ),
        ]

        # Act
        with patch('app.infrastructure.task.mail_task.send_mail') as mock_send:
            send_mail_task(fake_mail)

        # Assert
        mock_send.assert_called_once_with(fake_mail)
