from fastapi import APIRouter

from api.V1.endpoints import producao
from api.V1.endpoints import processamento
from api.V1.endpoints import comercializacao
from api.V1.endpoints import importacao
from api.V1.endpoints import exportacao


api_router = APIRouter()

api_router.include_router(producao.router, prefix="/producao", tags=["producao"])
api_router.include_router(processamento.router, prefix="/processamento", tags=["processamento"])
api_router.include_router(comercializacao.router, prefix="/comercializacao", tags=["comercializacao"])
api_router.include_router(importacao.router, prefix="/importacao", tags=["importacao"])
api_router.include_router(exportacao.router, prefix="/exportacao", tags=["exportacao"])
