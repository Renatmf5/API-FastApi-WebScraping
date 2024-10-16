from pydantic_settings import BaseSettings
from core.services.parameterServiceAws import ParameterServiceAws

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

if os.getenv('ENV') == 'production':
    settings = Settings(
        JWT_SECRET=ParameterServiceAws.get_ssm_parameter("JWT_SECRET"),
        DATABASE_URL=ParameterServiceAws.get_ssm_parameter("DATABASE_URL"),
        BUCKET_NAME=ParameterServiceAws.get_ssm_parameter("BUCKET_NAME")
    )
else:
    settings = Settings()