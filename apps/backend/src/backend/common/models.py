from datetime import datetime

from sqlalchemy import DateTime, MetaData, text
from sqlalchemy.orm import DeclarativeBase, Mapped, declared_attr, mapped_column

from ..core.config import db_config


class Base(DeclarativeBase):
    """Base class for all database models."""

    __prefix__: str

    metadata = MetaData(
        naming_convention=db_config.POSTGRES_INDEXES_NAMING_CONVENTION,
    )


class AuditBase(Base):
    """Base class for models that require audit fields."""

    __abstract__ = True

    @declared_attr
    def id(cls) -> Mapped[str]:
        prefix = getattr(cls, "__prefix__", "obj")
        return mapped_column(
            primary_key=True,
            server_default=text(
                f"gen_prefixed_id('{prefix}', {db_config.PREFIXED_ID_LENGTH})"
            ),
        )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=text("CURRENT_TIMESTAMP"),
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_onupdate=text("CURRENT_TIMESTAMP"),
        server_default=text("CURRENT_TIMESTAMP"),
    )
