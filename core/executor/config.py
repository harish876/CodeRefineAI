from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import Field, ValidationError

class Settings(BaseSettings):
    env: str = Field(..., env="ENV", description="The environment (e.g., development, production)")
    self_hosted: bool = Field(..., env="SELF_HOSTED", description="Flag indicating if the service is self-hosted")
    judge0_base_url: str = Field(..., env="JUDGE0_BASE_URL", description="Base URL for the Judge0 API")
    judge0_api_key: str = Field(..., env="JUDGE0_API_KEY", description="API key for the Judge0 API")
    google_gemini_api_key: str = Field(..., env="GOOGLE_GEMINI_API_KEY", description="API key for Google Gemini")
    num_runs: int = Field(..., env="NUM_RUNS", description="Number of runs for the code execution")

    class Config:
        env_file: Optional[str] = None
        env_file_encoding = 'utf-8'

def load_settings(env_file_path: str) -> Settings:
    class DynamicSettings(Settings):
        class Config(Settings.Config):
            env_file = env_file_path

    try:
        settings = DynamicSettings()
        return settings
    except ValidationError as e:
        print("Error loading settings. Please pass full path to .env file", e)
        raise

# Example usage
if __name__ == "__main__":
    env_file_path = "/Users/harishgokul/CodeRefineAI/.env"  # Replace with your dynamic path
    settings = load_settings(env_file_path)
    print(settings)