from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database import Base


class User(Base):
    """
    User modeli - Inheritance nümunəsi
    Base class-dan inherit edir (SQLAlchemy-dən gəlir)
    
    OOP Konseptlər:
    - Encapsulation: password hash-lənir, açıq saxlanmır
    - Inheritance: Base class-dan metodlar alır
    """
    __tablename__ = "users"
    
    # Primary Key
    id = Column(Integer, primary_key=True, index=True)
    
    # User məlumatları
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=True)
    hashed_password = Column(String, nullable=False)
    
    # Status
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships (One-to-Many)
    # Bir user-in çoxlu transaction-ları ola bilər
    transactions = relationship("Transaction", back_populates="user", cascade="all, delete-orphan")
    categories = relationship("Category", back_populates="user", cascade="all, delete-orphan")
    budgets = relationship("Budget", back_populates="user", cascade="all, delete-orphan")
    
    def __repr__(self):
        """String representation - debug üçün"""
        return f"<User(id={self.id}, username={self.username}, email={self.email})>"
    
    def __str__(self):
        """User-friendly string"""
        return f"{self.username} ({self.email})"