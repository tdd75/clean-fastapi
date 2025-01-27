from sqlalchemy.orm import Session

from app.domain.repository import user_repository
from app.presentation.dto.user_dto import UserListDTO


def execute(
    session: Session,
    keyword: str | None,
    email: str | None,
    limit: int,
    offset: int,
) -> UserListDTO:
    users, total = user_repository.search(
        session,
        keyword=keyword,
        email=email,
        eager=True,
        limit=limit,
        offset=offset,
    )
    return UserListDTO(items=users, total=total)
