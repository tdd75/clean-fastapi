from app.application.context import IContext
from app.domain.repository import user_repository
from app.application.dto.user_dto import UserListDTO


def execute(
    ctx: IContext,
    keyword: str | None,
    email: str | None,
    limit: int,
    offset: int,
) -> UserListDTO:
    users, total = user_repository.search(
        ctx.session,
        keyword=keyword,
        email=email,
        eager=True,
        limit=limit,
        offset=offset,
    )
    return UserListDTO(results=users, count=total)
