from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    env: str
    self_hosted: bool
    judge0_base_url: str
    judge0_api_key: str
    google_gemini_api_key: str
    
    class Config:
        env_file = ".env"

settings = Settings()