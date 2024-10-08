from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List
from api.utils.fetch_S3_files import list_tables_from_s3, fetch_data_from_s3, DataResponse, TablesResponse
from core.auth import get_current_user
from models.usuario_model import UsuarioModel

router = APIRouter()

@router.get("/", response_model=DataResponse)
def fetch_data(year_filter: str, file_key: str = Query(..., description="Nome do arquivo no S3"), usuario_logado: UsuarioModel = Depends(get_current_user)):
    if not usuario_logado.admin:
        raise HTTPException(status_code=403, detail="Usuário não autorizado")
    return fetch_data_from_s3(file_key, year_filter)

@router.get("/tables", response_model=TablesResponse)
def list_tables(usuario_logado: UsuarioModel = Depends(get_current_user)):
    if not usuario_logado.admin:
        raise HTTPException(status_code=403, detail="Usuário não autorizado")
    return list_tables_from_s3()