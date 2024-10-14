from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Configurations
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Web Scraping API"
    # Security
    JWT_SECRET: str
    ALGORITHM: str = 'HS256'
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7 # 60 minutos * 24 horas * 7 dias => 1 semana
    # Database
    DATABASE_URL: str
    # Web Scraping
    URL_DOWNLOAD: str = "http://vitibrasil.cnpuv.embrapa.br/download"
    # Logging
    LOG_LEVEL: str = "info"
    # DataLake Bucket name
    BUCKET_NAME: str
    # Environment
    ENV: str = "development"

    class Config:
        env_file = ".env"

settings = Settings()