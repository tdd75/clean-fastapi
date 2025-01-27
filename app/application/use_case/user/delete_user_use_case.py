from app.application.context import IContext
from app.domain.repository import user_repository
from app.application.service import user_service


def execute(ctx: IContext, user_id: int) -> None:
    user = user_service.read(ctx, user_id)
    return user_repository.delete(ctx.session, user)
