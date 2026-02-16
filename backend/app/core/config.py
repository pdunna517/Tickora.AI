from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "Tickora"
    API_V1_STR: str = "/api/v1"
    
    # Database configuration - support both individual fields and DATABASE_URL
    POSTGRES_SERVER: Optional[str] = None
    POSTGRES_USER: Optional[str] = None
    POSTGRES_PASSWORD: Optional[str] = None
    POSTGRES_DB: Optional[str] = None
    SQLALCHEMY_DATABASE_URI: Optional[str] = None

    # JWT configuration
    SECRET_KEY: str = "YOUR_SUPER_SECRET_KEY_HERE_CHANGE_IN_PRODUCTION"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        case_sensitive = True
        env_file = ".env"
        env_file_encoding = 'utf-8'
        # Make .env optional - don't fail if it doesn't exist
        extra = 'ignore'

    def __init__(self, **values):
        super().__init__(**values)
        # Priority: SQLALCHEMY_DATABASE_URI > DATABASE_URL > individual fields
        if not self.SQLALCHEMY_DATABASE_URI:
            # Check for DATABASE_URL (common in Render/Heroku)
            import os
            database_url = os.getenv("DATABASE_URL")
            if database_url:
                self.SQLALCHEMY_DATABASE_URI = database_url
            elif all([self.POSTGRES_SERVER, self.POSTGRES_USER, self.POSTGRES_PASSWORD, self.POSTGRES_DB]):
                self.SQLALCHEMY_DATABASE_URI = f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}/{self.POSTGRES_DB}"
            else:
                raise ValueError("Database configuration missing. Provide either DATABASE_URL or individual POSTGRES_* variables.")

settings = Settings()
