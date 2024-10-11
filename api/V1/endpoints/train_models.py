from fastapi import APIRouter, Depends, Query
from api.utils.fetch_S3_to_ml_functions import trat_parquet_from_s3
from api.utils.train_models import train
from api.utils.predicts import predict
from core.auth import get_current_user
from models.usuario_model import UsuarioModel

router = APIRouter()

@router.get("/train")
async def treinar_modelo(file_key: str, usuario_logado: UsuarioModel = Depends(get_current_user)):
    # Valida se usuario_logado atributo é admin true
    if not usuario_logado.admin:
        return {"status": "Usuário não autorizado"}
    data = trat_parquet_from_s3(file_key)       
    if not data.empty:
        # extrair dados e fazer o download no data lake
        result = train(data, file_key)
        return result          
    else:
        return {"status": "Falha ao extrair dados de produção"}

@router.get("/predict")
async def prever_modelo(file_key: str, anos_futuros: list[str] = Query(...), usuario_logado: UsuarioModel = Depends(get_current_user)):
    # Valida se usuario_logado atributo é admin true
    if not usuario_logado.admin:
        return {"status": "Usuário não autorizado"}
    data = trat_parquet_from_s3(file_key)
    if not data.empty:
        # extrair dados e fazer o download no data lake
        result = predict(data, file_key, anos_futuros)
        return result
    else:
        return {"status": "Falha ao extrair dados de produção"}