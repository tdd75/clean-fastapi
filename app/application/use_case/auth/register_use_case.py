from sqlalchemy.event import listen

from app.application.context import IContext
from app.application.dto.auth_dto import RegisterDTO, TokenPairDTO
from app.infrastructure.helper.jwt_helper import generate_token_pair
from app.infrastructure.helper.password_helper import hash_password
from app.domain.entity.user import User
from app.domain.repository import user_repository
from app.application.service import user_service
from app.infrastructure.task.mail_task import send_welcome_mail


def execute(ctx: IContext, dto: RegisterDTO) -> TokenPairDTO:
    user_service.validate_unique_email(ctx, dto.email)

    data = dto.model_dump(exclude_unset=True)
    user = User(**data)
    user.password = hash_password(dto.password)
    new_user = user_repository.create(ctx.session, user)
    listen(
        ctx.session,
        'after_commit',
        lambda s: send_welcome_mail.delay(new_user.email, new_user.first_name),
    )
    access, refresh = generate_token_pair(user.id)
    return TokenPairDTO(access=access, refresh=refresh)
