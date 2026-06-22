from sqlalchemy import Column, String, Float, Enum as SAEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from base import Base
import enum
import uuid

class LoanStatus(enum.Enum):
    DRAFT = "draft"
    SUBMITTED = "submitted"

class LoanApplication(Base):
    __tablename__ = "loan_applications"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    customer_id: Mapped[str] = mapped_column(String, nullable=False)
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    purpose: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[LoanStatus] = mapped_column(SAEnum(LoanStatus), default=LoanStatus.DRAFT)
