from app.application.context import IContext
from app.application.service import user_service
from app.application.dto.user_dto import UserDTO


def execute(ctx: IContext, user_id: int) -> UserDTO:
    user = user_service.read(ctx, user_id)
    return UserDTO.model_validate(user)
