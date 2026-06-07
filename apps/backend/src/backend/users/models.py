from sqlalchemy import false, true
from sqlalchemy.orm import Mapped, mapped_column

from ..common.models import AuditBase


class UserModel(AuditBase):
    __tablename__ = "users"
    __prefix__ = "usr"

    email: Mapped[str] = mapped_column(unique=True)
    username: Mapped[str] = mapped_column(unique=True)
    first_name: Mapped[str] = mapped_column()
    last_name: Mapped[str] = mapped_column()
    hashed_password: Mapped[str] = mapped_column()
    is_active: Mapped[bool] = mapped_column(default=True, server_default=true())
    is_admin: Mapped[bool] = mapped_column(default=False, server_default=false())
