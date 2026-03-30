from sqlalchemy import DateTime, String, Boolean, text
from sqlalchemy.orm import Mapped, mapped_column
from models.base import Base
from datetime import datetime
import uuid


class Chat(Base):
    __tablename__ = "chats"

    chat_id: Mapped[str] = mapped_column(
        String,
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )
    chat_name: Mapped[str | None] = mapped_column(
        String,
        nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=text("now()")
    )
    is_group: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False
    )
    dm_key: Mapped[str | None] = mapped_column(
        String,
        unique=True,
        nullable=True
    )
