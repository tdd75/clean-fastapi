from app.application.context import IContext
from app.domain.repository import user_repository
from app.application.service import user_service
from app.application.dto.user_dto import UpdateUserDTO, UserDTO


def execute(ctx: IContext, user_id: int, dto: UpdateUserDTO) -> UserDTO:
    user = user_service.read(ctx, user_id)
    update_data = dto.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(user, key, value)
    updated_user = user_repository.update(ctx.session, user)
    return UserDTO.model_validate(updated_user)
