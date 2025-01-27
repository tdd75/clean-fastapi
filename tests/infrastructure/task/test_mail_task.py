from faker import Faker

from app.infrastructure.task.mail_task import send_welcome_mail

fake = Faker()


class TestSendWelcomeMail:
    def test_send_welcome_mail(self, mocker):
        # Arrange
        email = fake.email()
        name = fake.first_name()
        mock_render_template = mocker.patch(
            'app.infrastructure.task.mail_task.render_template',
            return_value='<html>Welcome!</html>',
        )
        mock_send_mail = mocker.patch('app.infrastructure.task.mail_task.send_mail')
        mock_mail = mocker.patch('app.infrastructure.task.mail_task.Mail')
        mock_mail_instance = mocker.MagicMock()
        mock_mail.return_value = mock_mail_instance

        # Act
        send_welcome_mail(email, name)

        # Assert
        mock_render_template.assert_called_once_with('auth/welcome.html', {'name': name, 'app_name': 'FastAPI'})
        mock_mail.assert_called_once_with(
            receivers=[email],
            subject='Welcome to FastAPI',
            html_content='<html>Welcome!</html>',
        )
        mock_send_mail.assert_called_once_with([mock_mail_instance])
