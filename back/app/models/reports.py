import uuid
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, DateTime, JSON, Text
from .base import Base

class TestReport(Base):
    __tablename__ = "test_reports"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    
    attack_id: Mapped[str] = mapped_column(String(36), unique=True, index=True, nullable=False)
    request_id: Mapped[str] = mapped_column(String(36), index=True, nullable=False)
    
    target_model: Mapped[str] = mapped_column(String(100), nullable=False)
    target_url: Mapped[str] = mapped_column(String(500), nullable=False)
    target_auth_token_encrypted: Mapped[str] = mapped_column(Text, nullable=False)
    
    test_settings: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="pending")
    result: Mapped[dict | None] = mapped_column(JSON, nullable=True)

    full_report: Mapped[dict | None] = mapped_column(JSON, nullable=True)

    error: Mapped[str | None] = mapped_column(Text, nullable=True)
    
    task_id: Mapped[str] = mapped_column(String(50), nullable=False, default=lambda: f"report-{uuid.uuid4().hex[:8]}")
    
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)