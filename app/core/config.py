from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "FastAPI event_system_App"
    API_V1_STR: str = "/api/v1"
  
    # DB
    DATABASE_URL: str

   
    class Config:
        env_file = ".env"
        env_file_ending = "utf-8"


settings = Settings()