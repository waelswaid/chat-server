from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    JWT_PUBLIC_KEY : str = ""
    DATABASE_URL : str = ""
    REDIS_URL : str = ""
    CHAT_DATABASE_URL : str = ""
    S3_BUCKET_NAME : str = ""
    AWS_REGION : str = "us-east-1"
    CDN_DOMAIN : str = ""


settings = Settings()