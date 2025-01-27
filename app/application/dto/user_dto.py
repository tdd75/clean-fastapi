import datetime

from pydantic import BaseModel, Field, ConfigDict


class CreateUserDTO(BaseModel):
    email: str
    password: str
    first_name: str
    last_name: str
    phone: str | None = Field(None)


class UpdateUserDTO(BaseModel):
    first_name: str | None = Field(None)
    last_name: str | None = Field(None)
    phone: str | None = Field(None)


class SimpleUserDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: str
    full_name: str


class UserDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: str
    full_name: str
    first_name: str
    last_name: str
    phone: str | None = Field(None)
    created_at: datetime.datetime | None = Field(None)
    updated_at: datetime.datetime | None = Field(None)
    created_user: SimpleUserDTO | None = Field(None)
    updated_user: SimpleUserDTO | None = Field(None)


class UserListDTO(BaseModel):
    results: list[UserDTO]
    count: int
