"""
Configuration management for Rayeva AI Systems.
Loads environment variables and provides application settings.
"""
from pydantic_settings import BaseSettings
from pydantic import ConfigDict
from typing import List


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    model_config = ConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="ignore"  # Ignore extra fields from .env
    )
    
    # AI Configuration
    ai_provider: str = "groq"  # groq | gemini
    groq_api_key: str = ""
    groq_model: str = "llama-3.1-8b-instant"
    google_api_key: str = ""
    gemini_model: str = "gemini-pro-latest"
    gemini_max_tokens: int = 1500
    gemini_temperature: float = 0.7
    google_project_name: str = ""
    google_project_number: str = ""
    
    # Database Configuration
    database_url: str = "sqlite:///./rayeva.db"
    
    # API Configuration
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_key: str = "rayeva_dev_key"
    cors_origins: str = "http://localhost:3000,http://localhost:8000"
    
    # Logging Configuration
    log_level: str = "INFO"
    log_retention_days: int = 30
    log_dir: str = "logs"
    
    # Application Settings
    app_name: str = "Rayeva AI Systems"
    app_version: str = "1.0.0"
    debug: bool = True
    
    # Rate Limiting
    rate_limit_per_minute: int = 100
    
    # WhatsApp (Module 4 - Future)
    whatsapp_api_token: str = ""
    whatsapp_phone_number_id: str = ""
    whatsapp_verify_token: str = ""

    @property
    def ai_model(self) -> str:
        """Return active AI model based on provider."""
        if self.ai_provider.lower() == "groq":
            return self.groq_model
        return self.gemini_model
    
    @property
    def cors_origins_list(self) -> List[str]:
        """Parse CORS origins from comma-separated string."""
        return [origin.strip() for origin in self.cors_origins.split(",")]


# Global settings instance
settings = Settings()
