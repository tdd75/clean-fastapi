import datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship, declared_attr

if TYPE_CHECKING:
    from app.domain.entity.user import User


class AuditMixin:
    created_at: Mapped[datetime.datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime.datetime] = mapped_column(server_default=func.now(), server_onupdate=func.now())
    created_user_id: Mapped[int | None] = mapped_column(ForeignKey('user.id'))
    updated_user_id: Mapped[int | None] = mapped_column(ForeignKey('user.id'))

    @declared_attr
    def created_user(self) -> Mapped['User | None']:
        return relationship('User', foreign_keys=[self.created_user_id])

    @declared_attr
    def updated_user(self) -> Mapped['User | None']:
        return relationship('User', foreign_keys=[self.updated_user_id])
