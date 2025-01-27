from pydantic import BaseModel


class RegisterDTO(BaseModel):
    email: str
    password: str
    first_name: str
    last_name: str


class LoginDTO(BaseModel):
    email: str
    password: str


class ForgotPasswordDTO(BaseModel):
    email: str


class ResetPasswordDTO(BaseModel):
    otp_code: str
    email: str
    new_password: str


class TokenPairDTO(BaseModel):
    access: str
    refresh: str
