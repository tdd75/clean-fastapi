from pydantic import BaseModel, ConfigDict, Field


class RegisterDTO(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            'examples': [
                {
                    'email': 'tranducduy7520@gmail.com',
                    'password': 'duytd123',
                    'first_name': 'Duy',
                    'last_name': 'Tran',
                },
            ],
        },
    )

    email: str = Field(...)
    password: str = Field(...)
    first_name: str = Field(...)
    last_name: str = Field(...)


class LoginDTO(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            'examples': [
                {
                    'email': 'tranducduy7520@gmail.com',
                    'password': 'duytd123',
                },
            ],
        },
    )

    email: str = Field(...)
    password: str = Field(...)


class ForgotPasswordDTO(BaseModel):
    email: str = Field(...)


class ResetPasswordDTO(BaseModel):
    otp_code: str = Field(...)
    email: str = Field(...)
    new_password: str = Field(...)


class TokenPairDTO(BaseModel):
    access: str = Field(...)
    refresh: str = Field(...)
