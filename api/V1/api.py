from fastapi import APIRouter

from api.V1.endpoints import producao
from api.V1.endpoints import processamento
from api.V1.endpoints import comercializacao
from api.V1.endpoints import importacao
from api.V1.endpoints import exportacao
from api.V1.endpoints import usuarios
from api.V1.endpoints import fetch_data_S3


api_router = APIRouter()

api_router.include_router(producao.router, prefix="/producao", tags=["producao"])
api_router.include_router(processamento.router, prefix="/processamento", tags=["processamento"])
api_router.include_router(comercializacao.router, prefix="/comercializacao", tags=["comercializacao"])
api_router.include_router(importacao.router, prefix="/importacao", tags=["importacao"])
api_router.include_router(exportacao.router, prefix="/exportacao", tags=["exportacao"])
api_router.include_router(usuarios.router, prefix="/usuarios", tags=["usuarios"])
api_router.include_router(fetch_data_S3.router, prefix="/fetch-data", tags=["fetch-data"])
