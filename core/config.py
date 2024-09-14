from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Configurations
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Web Scraping API"
    # Security
    JWT_SECRET: str = 'SYbwx85IxCd5TAA5vmopAR3_jKx9AbErgiIxIWZab8A'
    ALGORITHM: str = 'HS256'
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7 # 60 minutos * 24 horas * 7 dias => 1 semana
    # Database
    DATABASE_URL: str = "sqlite:///./authDB.db"
    # Web Scraping
    URL_DOWNLOAD: str = "http://vitibrasil.cnpuv.embrapa.br/download"
    # Logging
    LOG_LEVEL: str = "info"
    # DataLake Bucket name
    BUCKET_NAME: str = 'datalake-bucket-techchallenge1'
    
    
settings = Settings()


#  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJSZW5hdG9tIiwiZXhwIjoxNzI2NTk3Nzk1fQ.wB_Ad0KDciQSx72b0OOy5widRle_uEEuKj5wC4gvJjQ",
#  "token_type": "bearer"