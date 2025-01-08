from pydantic import BaseModel
from uuid import UUID

from sqlalchemy import Date

from sqlalchemy import Column, String, Float, Text, Date, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import uuid

Base = declarative_base()

class Debt(Base):
    __tablename__ = 'Debts'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('Users.id'), nullable=False)
    description = Column(String(255), nullable=False)
    amount = Column(Float, nullable=False)
    debtor_name = Column(String(100), nullable=False)
    creditor_name = Column(String(100), nullable=False)
    due_date = Column(Date, nullable=True)
    debt_closing_date = Column(Date, nullable=True)
    status_id = Column(UUID(as_uuid=True), ForeignKey('Status.id'), nullable=False)
    notes = Column(Text, nullable=True)

    user = relationship("User", back_populates="debts")

    status = relationship("Status")

    def to_dict(self) -> dict:
        """
        Converts the Debt instance to a dictionary.

        Returns:
            dict: Dictionary representation of the Debt instance.
        """
        return {
            "id": self.id,
            "description": self.description,
            "amount": self.amount,
            "debtor_name": self.debtor_name,
            "creditor_name": self.creditor_name,
            "status": self.status,
        }

class DebtCreate(BaseModel):
    description: str
    amount: float
    debtor_name: str
    creditor_name: str
    status: str 

class DebtRequest(BaseModel):
    description: str
    amount: float
    debtor_name: str
    creditor_name: str
    status: str

class DebtUpdate(BaseModel):
    id: int
    description: str
    amount: float
    debtor_name: str
    creditor_name: str
    status: str

    def is_valid_status(self, status: str) -> bool:
        """
        Validates the status.

        Args:
            status (str): Status to validate.

        Returns:
            bool: True if valid, False otherwise.
        """
        valid_statuses = {"Pending", "Paid", "Overdue"}
        return status in valid_statuses

class DebtResponse(BaseModel):
    id: str  # Unique identifier for the debt
    description: str
    amount: float
    debtor_name: str
    creditor_name: str
    status: str

    def to_dict(self) -> dict:
        """
        Converts the DebtResponse instance to a dictionary.

        Returns:
            dict: Dictionary representation of the DebtResponse instance.
        """
        return {
            "id": str(self.id),  # Convert UUID to string for serialization
            "description": self.description,
            "amount": self.amount,
            "debtor_name": self.debtor_name,
            "creditor_name": self.creditor_name,
            "status": self.status,
        }
