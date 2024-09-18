import boto3
from fastapi import HTTPException
from cachetools import TTLCache, cached
from typing import Optional, List, Tuple
import psycopg2
from pydantic import BaseModel
from core.services.parameterServiceAws import get_ssm_parameter

# Configurações do cache
cache = TTLCache(maxsize=100, ttl=300)  # Cache com tamanho máximo de 100 itens e TTL de 300 segundos (5 minutos)

# Modelo de dados para a resposta
class DataResponse(BaseModel):
    columns: List[str]
    data: List[List[str]]

# Função para buscar dados do Redshift
@cached(cache)
def fetch_data_from_redshift(table: str, columns: Optional[Tuple[str]], filters: Optional[str]) -> DataResponse:
    try:
        # Configurações do Redshift a partir do SSM Parameter Store
        redshift_cluster = get_ssm_parameter('/techchallenge_fase1/redshift/cluster-endpoint')
        redshift_database = get_ssm_parameter('/techchallenge_fase1/redshift/database')
        redshift_user = get_ssm_parameter('/techchallenge_fase1/redshift/user')
        redshift_password = get_ssm_parameter('/techchallenge_fase1/redshift/password')
        redshift_port = int(get_ssm_parameter('/techchallenge_fase1/redshift/port'))
        
        # Conectar ao Redshift
        conn = psycopg2.connect(
            dbname=redshift_database,
            user=redshift_user,
            password=redshift_password,
            port=redshift_port,
            host=redshift_cluster
        )
        cursor = conn.cursor()
        
        # Construir a consulta SQL
        columns_str = ', '.join(columns) if columns else '*'
        query = f"SELECT {columns_str} FROM {table}"
        if filters:
            query += f" WHERE {filters};"
        #query += " LIMIT 4000;"  # Limite opcional para evitar grandes volumes de dados
        
        # Executar a consulta SQL
        cursor.execute(query)
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        
        # Converter todos os valores para strings
        data = [[str(cell) for cell in row] for row in rows]
        
        # Fechar a conexão
        cursor.close()
        conn.close()
        
        # Retornar os dados em formato JSON
        return DataResponse(columns=columns, data=data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))