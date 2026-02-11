from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
import os

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )
    
    API_PREFIX: str = "/api"
    DEBUG: bool = False
    DATABASE_URL: str = None
    
    # Use Field with validation_alias to read from env, store as string internally
    allowed_origins_str: str = Field(default="", validation_alias="ALLOWED_ORIGINS")
    
    OPENAI_API_KEY: str

    def __init__(self, **values):
        super().__init__(**values)
        if not self.DEBUG:
            db_user = os.getenv("DB_USER")
            db_password = os.getenv("DB_PASSWORD")
            db_host = os.getenv("DB_HOST")
            db_port = os.getenv("DB_PORT")
            db_name = os.getenv("DB_NAME")
            self.DATABASE_URL = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

    @property
    def ALLOWED_ORIGINS(self) -> List[str]:
        """Parse comma-separated origins from env"""
        if self.allowed_origins_str:
            return [origin.strip() for origin in self.allowed_origins_str.split(",")]
        return []


settings = Settings()