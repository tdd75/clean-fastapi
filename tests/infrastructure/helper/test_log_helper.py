from faker import Faker

from app.infrastructure.helper.log_helper import mask_sensitive_values

fake = Faker()


class TestMaskSensitiveValues:
    def test_mask_simple_dict(self):
        # Arrange
        data = {
            'password': fake.password(),
            'email': fake.email(),
            'name': fake.first_name(),
        }

        # Act
        result = mask_sensitive_values(data, keywords=['password', 'email'])

        # Assert
        assert result == {
            'password': '***',
            'email': '***',
            'name': data['name'],
        }

    def test_mask_nested_dict(self):
        # Arrange
        nested_password = fake.password()
        nested_email = fake.email()
        nickname = fake.first_name()

        data = {
            'user': {
                'email': nested_email,
                'profile': {
                    'password': nested_password,
                    'nickname': nickname,
                },
            }
        }

        # Act
        result = mask_sensitive_values(data, ['password', 'email'])

        # Assert
        assert result == {
            'user': {
                'email': '***',
                'profile': {
                    'password': '***',
                    'nickname': nickname,
                },
            }
        }

    def test_mask_list_of_dicts(self):
        # Arrange
        data = [
            {'email': fake.email(), 'name': fake.first_name()},
            {'email': fake.email(), 'name': fake.first_name()},
        ]

        # Act
        result = mask_sensitive_values(data, ['email'])

        # Assert
        for item in result:
            assert item['email'] == '***'

    def test_mask_case_insensitive(self):
        # Arrange
        data = {
            'PassWord': fake.password(),
            'Email': fake.email(),
        }

        # Act
        result = mask_sensitive_values(data, ['password', 'email'])

        # Assert
        assert result == {
            'PassWord': '***',
            'Email': '***',
        }

    def test_no_keywords_matched(self):
        # Arrange
        data = {
            'token': fake.sha256(),
            'id': fake.random_number(),
        }

        # Act
        result = mask_sensitive_values(data, ['password'])

        # Assert
        assert result == data

    def test_empty_input(self):
        # Arrange + Act + Assert
        assert mask_sensitive_values({}, ['password']) == {}
        assert mask_sensitive_values([], ['password']) == []
