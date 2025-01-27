from sqlalchemy import or_

from sqlalchemy.orm import Session, joinedload

from app.domain.entity.user import User


def search(
    session: Session,
    keyword: str | None = None,
    email: str | None = None,
    eager: bool = False,
    limit: int | None = None,
    offset: int | None = None,
) -> tuple[list[User], int]:
    query = session.query(User)

    # eager loading
    if eager:
        query = query.options(
            joinedload(User.created_user),
            joinedload(User.updated_user),
        )

    # filter
    filters = []
    if keyword is not None:
        filters.append(
            or_(
                User.email.icontains(keyword),
                User.full_name.icontains(keyword),
            )
        )
    if email is not None:
        filters.append(User.email.icontains(email))
    query = query.filter(*filters)

    # pagination
    if limit is not None:
        query = query.limit(limit)
    if offset is not None:
        query = query.offset(offset)

    results = query.all()
    count = query.count()

    return results, count


def find_by_id(session: Session, user_id: int) -> User | None:
    return session.query(User).filter(User.id == user_id).first()


def find_by_email(session: Session, email: str) -> User | None:
    return session.query(User).filter(User.email == email).first()


def create(session: Session, user: User) -> User:
    user.created_user_id = session.info.get('uid')
    user.updated_user_id = session.info.get('uid')

    session.add(user)
    session.flush([user])
    session.refresh(user)

    return user


def update(session: Session, user: User) -> User:
    user.updated_user_id = session.info.get('uid')

    session.flush([user])
    session.refresh(user)

    return user


def delete(session: Session, user: User) -> None:
    session.delete(user)
    session.flush()
