from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    env: str
    judge0_base_url: str
    judge0_api_key: str
    
    class Config:
        env_file = "/Users/harishgokul/CodeRefineAI/core/executor/.env"

settings = Settings()