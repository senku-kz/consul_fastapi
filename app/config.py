from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    """Application settings."""
    # Environment
    ENVIRONMENT: str = "development"
    
    # Application settings
    APP_NAME: str = "fastapi-service"
    DEBUG: bool = False
    
    # Server settings
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # Consul settings
    CONSUL_HOST: str = "localhost"
    CONSUL_PORT: int = 8500
    SERVICE_NAME: str = "fastapi-service"
    SERVICE_PORT: int = 8000
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True
        extra = "ignore"  # Ignore any extra env variables

@lru_cache
def get_settings() -> Settings:
    """Get cached settings."""
    return Settings() 