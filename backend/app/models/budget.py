from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from ..database import Base


class BudgetPeriod(str, enum.Enum):
    """Büdcə dövrü"""
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    YEARLY = "yearly"


class Budget(Base):
    """
    Budget modeli - büdcə planlaması
    
    OOP:
    - Inheritance: Base class
    - Composition: User və Category ilə əlaqə
    - Methods: hesablama metodları
    """
    __tablename__ = "budgets"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Büdcə məlumatları
    name = Column(String, nullable=False)
    amount = Column(Float, nullable=False)  # Planlaşdırılan məbləğ
    spent = Column(Float, default=0.0)      # Xərclənən məbləğ
    period = Column(Enum(BudgetPeriod), default=BudgetPeriod.MONTHLY)
    
    # Tarixlər
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    
    # Foreign Keys
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="budgets")
    
    def __repr__(self):
        return f"<Budget(id={self.id}, name={self.name}, amount=${self.amount})>"
    
    # Business logic metodları
    def remaining_amount(self) -> float:
        """Qalan məbləğ"""
        return self.amount - self.spent
    
    def spent_percentage(self) -> float:
        """Xərcləmə faizi"""
        if self.amount == 0:
            return 0.0
        return (self.spent / self.amount) * 100
    
    def is_over_budget(self) -> bool:
        """Büdcə aşıldı?"""
        return self.spent > self.amount
    
    def is_warning_threshold(self, threshold: float = 80.0) -> bool:
        """Xəbərdarlıq həddindədir? (default 80%)"""
        return self.spent_percentage() >= threshold
    
    def status(self) -> str:
        """Büdcə statusu"""
        percentage = self.spent_percentage()
        if percentage >= 100:
            return "OVER_BUDGET"
        elif percentage >= 80:
            return "WARNING"
        elif percentage >= 50:
            return "MODERATE"
        else:
            return "SAFE"