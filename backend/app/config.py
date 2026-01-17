from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """
    Aplikasiya konfiqurasiyası
    Environment variables-dan oxuyur
    """
    # API Settings
    app_name: str = "MoneyTrack API"
    app_version: str = "1.0.0"
    debug: bool = True
    
    # Database Settings (SQLite istifadə edəcəyik - sadədir)
    database_url: str = "sqlite:///./moneytrack.db"
    
    # Security
    secret_key: str = "your-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    """Settings singleton - yalnız 1 dəfə yaranır"""
    return Settings()