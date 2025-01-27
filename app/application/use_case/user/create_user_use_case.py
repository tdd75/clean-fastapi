from app.application.context import IContext
from app.application.dto.user_dto import CreateUserDTO, UserDTO
from app.infrastructure.helper.password_helper import hash_password
from app.domain.entity.user import User
from app.domain.repository import user_repository
from app.application.service import user_service


def execute(ctx: IContext, dto: CreateUserDTO) -> UserDTO:
    user_service.validate_unique_email(ctx, dto.email)

    create_data = dto.model_dump(exclude_unset=True)
    user = User(**create_data)
    user.password = hash_password(dto.password)
    new_user = user_repository.create(ctx.session, user)
    return UserDTO.model_validate(new_user)
