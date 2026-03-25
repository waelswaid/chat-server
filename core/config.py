from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    JWT_PUBLIC_KEY : str = ""
    DATABASE_URL : str = ""
    REDIS_URL : str = ""



settings = Settings()