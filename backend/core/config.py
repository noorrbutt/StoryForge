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
    DEBUG: bool = True  # Set to True by default for local dev
    DATABASE_URL: Optional[str] = None
    
    # Use Field with validation_alias to read from env, store as string internally
    allowed_origins_str: str = Field(default="", validation_alias="ALLOWED_ORIGINS")
    
    # Make OpenAI optional since we're using Groq
    OPENAI_API_KEY: Optional[str] = None
    
    # Add Groq support
    GROQ_API_KEY: Optional[str] = None
    
    def __init__(self, **values):
        super().__init__(**values)
        
        # Build database URL
        db_user = os.getenv("DB_USER")
        db_password = os.getenv("DB_PASSWORD")
        db_host = os.getenv("DB_HOST")
        db_port = os.getenv("DB_PORT")
        db_name = os.getenv("DB_NAME")
        
        if all([db_user, db_password, db_host, db_port, db_name]):
            # Production: Use PostgreSQL
            self.DATABASE_URL = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
        else:
            # Development: Use SQLite
            self.DATABASE_URL = "sqlite:///./test.db"
            if not self.DEBUG:
                print("⚠ WARNING: No PostgreSQL config, falling back to SQLite")
    
    @property
    def ALLOWED_ORIGINS(self) -> List[str]:
        """Parse comma-separated origins from env"""
        if self.allowed_origins_str:
            return [origin.strip() for origin in self.allowed_origins_str.split(",")]
        # Default to common localhost origins in development
        if self.DEBUG:
            return [
                "http://localhost:3000",
                "http://localhost:5173",
                "http://127.0.0.1:3000",
                "http://127.0.0.1:5173",
                "http://localhost:5174", 
            ]
        return []

settings = Settings()