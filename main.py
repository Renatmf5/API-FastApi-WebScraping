from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.V1.api import api_router
from core.config import settings
from sqlmodel import SQLModel
from core.database import engine
from models.usuario_model import UsuarioModel  # Importe todos os modelos que você deseja criar

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_application() -> FastAPI:
    app = FastAPI(title=settings.PROJECT_NAME)
    app.include_router(api_router, prefix=settings.API_V1_STR)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.on_event("startup")
    def on_startup():
        create_db_and_tables()

    return app

app = get_application()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level=settings.LOG_LEVEL, reload=settings.ENV == "development")