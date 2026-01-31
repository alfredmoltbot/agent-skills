from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Configuración de la aplicación."""
    
    # Database
    database_url: str = "mysql+pymysql://user:password@localhost/dbname"
    
    # Application
    app_name: str = "Mi API"
    debug: bool = False
    secret_key: str = "change-me-in-production"
    
    # JWT
    access_token_expire_minutes: int = 30
    algorithm: str = "HS256"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache
def get_settings() -> Settings:
    """Retorna instancia cacheada de Settings."""
    return Settings()
