from fastapi import APIRouter, Query
from typing import List, Optional
from api.utils.fetch_redshift import fetch_data_from_redshift, DataResponse

router = APIRouter()

@router.get("/", response_model=DataResponse)
def fetch_data(table: str = Query(..., description="Nome da tabela no Redshift"), 
               columns: Optional[str] = Query(None, description="Lista de colunas a serem retornadas"), 
               filters: Optional[str] = Query(None, description="Filtros da consulta SQL")):
    
    # Converter a string de colunas para uma lista e depois para uma tupla
    columns_tuple = tuple(columns.split(',')) if columns else None
    return fetch_data_from_redshift(table, columns_tuple, filters)