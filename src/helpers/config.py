from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    
    # API Keys
    OPENAI_API_KEY: str
    
    # Google Cloud (existing)
    GEMINI_API_KEY: str
    
    class Config:
        env_file = ".env"
        case_sensitive = True

def get_settings():

    return Settings()