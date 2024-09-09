from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Configurations
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Web Scraping API"
    # Database
    DATABASE_URL: str = "sqlite:///./test.db"
    # Web Scraping
    URL_DOWNLOAD: str = "http://vitibrasil.cnpuv.embrapa.br/download"
    # Logging
    LOG_LEVEL: str = "info"
    
    
settings = Settings()