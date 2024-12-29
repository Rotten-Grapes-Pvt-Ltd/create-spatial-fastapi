from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str

    
    class Config:
        env_file = ".env"
        case_sensitive = True # Ensure environment variables are case-sensitive
        extra = "ignore" # Ignore extra env vars not defined in model

settings = Settings(_env_file=".env") # Pass env file explicitly
