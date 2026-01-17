from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Boolean, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from ..database import Base


class TransactionType(str, enum.Enum):
    """Transaction növləri - Polymorphism"""
    INCOME = "income"
    EXPENSE = "expense"
    TRANSFER = "transfer"


class PaymentMethod(str, enum.Enum):
    """Ödəniş metodları"""
    CASH = "cash"
    CARD = "card"
    BANK_TRANSFER = "bank_transfer"
    DIGITAL_WALLET = "digital_wallet"
    OTHER = "other"


class Transaction(Base):
    """
    Transaction modeli - əsas biznes məntiq
    
    OOP Konseptlər:
    - Multiple Inheritance: Base və mixin class-lardan
    - Encapsulation: məlumat və metodlar bir yerdə
    - Polymorphism: fərqli transaction növləri
    """
    __tablename__ = "transactions"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Transaction məlumatları
    amount = Column(Float, nullable=False)
    description = Column(String, nullable=True)
    type = Column(Enum(TransactionType), nullable=False)
    payment_method = Column(Enum(PaymentMethod), default=PaymentMethod.CASH)
    
    # Transaction tarixi
    date = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Recurring (təkrarlanan) transaction-mı?
    is_recurring = Column(Boolean, default=False)
    
    # Foreign Keys
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="transactions")
    category = relationship("Category", back_populates="transactions")
    
    def __repr__(self):
        return f"<Transaction(id={self.id}, type={self.type.value}, amount={self.amount})>"
    
    def __str__(self):
        sign = "+" if self.is_income() else "-"
        return f"{sign}${self.amount:.2f} - {self.description or 'No description'}"
    
    # Polymorphism - eyni interface, fərqli davranış
    def is_income(self) -> bool:
        """Gəlirdir?"""
        return self.type == TransactionType.INCOME
    
    def is_expense(self) -> bool:
        """Xərcdir?"""
        return self.type == TransactionType.EXPENSE
    
    def is_transfer(self) -> bool:
        """Transfer-dir?"""
        return self.type == TransactionType.TRANSFER
    
    def get_signed_amount(self) -> float:
        """
        İşarəli məbləğ qaytarır
        Income: +amount
        Expense: -amount
        """
        if self.is_income():
            return self.amount
        else:
            return -self.amount
    
    def formatted_amount(self) -> str:
        """Formatlanmış məbləğ: $123.45"""
        return f"${self.amount:.2f}"