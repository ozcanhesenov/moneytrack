from sqlalchemy import Column, Integer, String, Enum, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from ..database import Base


class CategoryType(str, enum.Enum):
    """
    Enum class - Category növləri
    Polymorphism nümunəsi - eyni interface, fərqli davranış
    """
    INCOME = "income"      # Gəlir
    EXPENSE = "expense"    # Xərc


class Category(Base):
    """
    Category modeli
    
    OOP: 
    - Inheritance: Base-dən gəlir
    - Composition: User ilə əlaqəlidir (has-a relationship)
    """
    __tablename__ = "categories"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    type = Column(Enum(CategoryType), nullable=False)
    color = Column(String, default="#808080")  # Hex color code
    icon = Column(String, nullable=True)
    description = Column(String, nullable=True)
    
    # Foreign Key - hansı user-ə aiddir
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="categories")
    transactions = relationship("Transaction", back_populates="category")
    
    def __repr__(self):
        return f"<Category(id={self.id}, name={self.name}, type={self.type.value})>"
    
    def is_income(self) -> bool:
        """Polymorphism nümunəsi - metod behaviour"""
        return self.type == CategoryType.INCOME
    
    def is_expense(self) -> bool:
        """Polymorphism nümunəsi"""
        return self.type == CategoryType.EXPENSE