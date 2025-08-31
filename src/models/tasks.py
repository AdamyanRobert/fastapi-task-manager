
from typing import Optional
import uuid
from sqlalchemy.dialects.postgresql import UUID
from src.database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, CheckConstraint


class TaskModel(Base):
    __tablename__ = "tasks"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(1000), nullable=True)
    status: Mapped[str] = mapped_column(String(20), nullable=False)

    __table_args__ = (
        CheckConstraint("status IN ('created', 'in_progress', 'completed')", name="check_status"),
    )
