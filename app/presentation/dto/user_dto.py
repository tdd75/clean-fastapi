import datetime

from pydantic import BaseModel, Field, ConfigDict


class UserCreateDTO(BaseModel):
    email: str = Field(...)
    password: str = Field(...)
    first_name: str = Field(...)
    last_name: str = Field(...)
    phone: str | None = Field(None)


class UserUpdateDTO(BaseModel):
    first_name: str | None = Field(None)
    last_name: str | None = Field(None)
    phone: str | None = Field(None)


class SimpleUserDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(...)
    email: str = Field(...)
    full_name: str = Field(...)


class UserDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(...)
    email: str = Field(...)
    full_name: str = Field(...)
    first_name: str = Field(...)
    last_name: str = Field(...)
    phone: str | None = Field(...)
    created_at: datetime.datetime | None = Field(None)
    updated_at: datetime.datetime | None = Field(None)
    created_user: SimpleUserDTO | None = Field(None)
    updated_user: SimpleUserDTO | None = Field(None)


class UserListDTO(BaseModel):
    items: list[UserDTO] = Field(...)
    total: int = Field(...)
