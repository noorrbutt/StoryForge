from typing import List, Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
import os

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra='allow' 
    )
    
    API_PREFIX: str = "/api"
    DEBUG: bool = True
    DATABASE_URL: Optional[str] = None
    
    allowed_origins_str: str = Field(default="", validation_alias="ALLOWED_ORIGINS")
    OPENAI_API_KEY: Optional[str] = None
    GROQ_API_KEY: Optional[str] = None
    
    def __init__(self, **values):
        super().__init__(**values)
        
        # Priority 1: Check for Vercel Postgres
        vercel_postgres = os.getenv("POSTGRES_URL")
        if vercel_postgres:
            self.DATABASE_URL = vercel_postgres
            print("✅ Using Vercel Postgres")
            return
        
        # Priority 2: Check for custom PostgreSQL config
        db_user = os.getenv("DB_USER")
        db_password = os.getenv("DB_PASSWORD")
        db_host = os.getenv("DB_HOST")
        db_port = os.getenv("DB_PORT")
        db_name = os.getenv("DB_NAME")
        
        if all([db_user, db_password, db_host, db_port, db_name]):
            self.DATABASE_URL = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
            print("✅ Using custom PostgreSQL")
            return
        
        # Fallback: In-memory SQLite (for local dev)
        self.DATABASE_URL = "sqlite:///:memory:"
        print("⚠️ WARNING: Using in-memory SQLite")
    
    @property
    def ALLOWED_ORIGINS(self) -> List[str]:
        """Parse comma-separated origins from env"""
        if self.allowed_origins_str:
            return [origin.strip() for origin in self.allowed_origins_str.split(",")]
        if self.DEBUG:
            return [
                "http://localhost:3000",
                "http://localhost:5173",
                "http://127.0.0.1:3000",
                "http://127.0.0.1:5173",
                "http://localhost:5174",
                "https://*.vercel.app",
            ]
        return []

settings = Settings()